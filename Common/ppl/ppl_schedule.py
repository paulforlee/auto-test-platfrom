"""PPL 公共流程调度层（Public Process Layer）

封装跨设备组合的通用测试流程，向下调用各 PBL 层复合操作，
供测试用例直接调度（分层位置：testcase -> PPL -> PBL -> CL -> driver -> connection）。

典型流程（电网过压保护）：
    逆变器并网 -> AC 源升压至过压阈值 -> 示波器记录波形
    -> 检测逆变器停机/故障 -> 计算保护动作时间 -> 恢复工况

方法索引（对应 testcase/逆变器 下的测试分类）：
    过欠压保护: grid_over_voltage_protection / grid_under_voltage_protection
    过欠频保护: grid_over_frequency_protection / grid_under_frequency_protection
    反复高低穿: voltage_ride_through
    最大无功运行: max_reactive_power_run
    波形记录: start_waveform_recording / save_waveform
    保护时间: get_protection_time

依赖说明：
    示波器（波形记录）暂不在设备架构内，需先补充：
    - driver/oscilloscope.py（示波器驱动，SCPI）
    - config/command_maps/oscilloscope_cmds.json（命令映射表）
    - config/env_config.yml / 功能测试 config/device_config.yaml（示波器连接参数）
"""
import logging
from pathlib import Path

from utils.exceptions import DeviceTimeoutError


class PplSchedule:
    """公共流程调度器：编排跨设备通用测试流程

    组合以下组件（按场景传入所需部分）：
    - pbl_ac / pbl_pv / pbl_meter / pbl_inverter：PBL 层实例
    - scope：示波器驱动实例（TODO: 驱动尚未实现）
    - recorder：pml.DataRecorder 实例

    使用示例（用例脚本中）：
        ppl = PplSchedule(pbl_inverter=inverter_pbl, pbl_ac=ac_pbl,
                          scope=scope_driver, recorder=recorder)
        result = ppl.grid_over_voltage_protection(voltage=264.0)
        assert result["passed"]
    """

    __slots__ = ("_pbl", "scope", "logger", "recorder")

    def __init__(self, *,
                 pbl_ac=None,
                 pbl_pv=None,
                 pbl_meter=None,
                 pbl_inverter=None,
                 scope=None,
                 logger=None,
                 recorder=None):
        """
        Args:
            pbl_ac/pbl_pv/pbl_meter/pbl_inverter: 各 PBL 层实例，按流程需要传入
            scope: 示波器驱动实例（TODO: 驱动实现后接入）
            logger: 日志记录器（默认使用模块 logger）
            recorder: pml.DataRecorder 实例，用于记录流程数据
        """
        self._pbl = {
            "pbl_ac": pbl_ac,
            "pbl_pv": pbl_pv,
            "pbl_meter": pbl_meter,
            "pbl_inverter": pbl_inverter,
        }
        self.scope = scope
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self.recorder = recorder

    # ---------------- 内部工具 ----------------

    def _p(self, key: str):
        """按键获取 PBL 实例，缺失时抛 ValueError（提示该流程需要哪个 PBL）"""
        pbl = self._pbl.get(key)
        if pbl is None:
            raise ValueError(
                f"{self.__class__.__name__} 需要 '{key}'，但未传入对应 PBL 实例")
        return pbl

    def _record(self, **fields) -> None:
        """向 DataRecorder 记录一条数据（未配置 recorder 时忽略）"""
        if self.recorder is not None:
            self.recorder.record(**fields)

    def _require_scope(self):
        """获取示波器驱动，未配置时抛 ValueError"""
        if self.scope is None:
            raise ValueError("该流程需要示波器（scope 参数），但未传入示波器驱动实例")
        return self.scope

    # ---------------- 波形记录 ----------------

    def start_waveform_recording(self, *,
                                 channel: str = "CH1",
                                 trigger_source: str = "EXT",
                                 timeout: float = 10.0) -> None:
        """示波器单次触发记录：配置触发条件并等待波形采集完成

        Args:
            channel: 采集通道（如 CH1 电压、CH2 电流）
            trigger_source: 触发源（EXT 外部触发 / 通道触发，按场景选择）
            timeout: 等待采集完成超时（秒）

        TODO:
        1. 配置通道开关/量程/时基/触发电平（需示波器驱动）
        2. 发送单次触发（SINGLE）指令
        3. 轮询采集状态直至完成，超时抛 DeviceTimeoutError
        """
        self._require_scope()
        # TODO: 实现示波器触发采集
        raise NotImplementedError("TODO: 实现示波器触发记录（需示波器驱动）")

    def save_waveform(self, name: str) -> Path:
        """保存示波器波形数据到 testcase 原始数据目录

        Args:
            name: 波形文件名主体（建议含用例名 + 场景名）

        Returns:
            波形数据文件路径

        TODO:
        1. 从示波器读取波形数据（时间轴 + 各通道电压值）
        2. 保存为 CSV（复用 pml.DataExport.to_csv 或示波器原生格式）
        """
        self._require_scope()
        # TODO: 实现波形数据读取与保存
        raise NotImplementedError("TODO: 实现波形数据保存（需示波器驱动）")

    # ---------------- 保护时间 ----------------

    def get_protection_time(self, trigger_time: float, fault_time: float) -> float:
        """计算保护动作时间（秒）

        Args:
            trigger_time: 异常工况施加时刻（time.monotonic() 时间戳）
            fault_time: 检测到逆变器停机/故障时刻

        Returns:
            保护动作时间 = fault_time - trigger_time
        """
        return fault_time - trigger_time

    # ---------------- 电网过/欠压保护（过欠压保护） ----------------

    def _run_grid_voltage_protection(self, name: str, voltage: float,
                                     max_reaction_time: float,
                                     recover_voltage: float) -> dict:
        """电网过/欠压保护公共流程（内部复用，过压与欠压仅目标电压方向不同）

        TODO 流程步骤:
        1. 逆变器启动并网（pbl_inverter 的 cl_inverter），确认运行状态
        2. 示波器预触发 start_waveform_recording（记录异常瞬间波形）
        3. AC 源输出至目标电压（pbl_ac），记录施加时刻 trigger_time
        4. 轮询逆变器状态/故障码，检测到停机或对应故障时记录 fault_time
        5. reaction_time = get_protection_time(trigger_time, fault_time)
        6. 保存波形 save_waveform，AC 源恢复 recover_voltage
        7. 确认逆变器可恢复并网（必要时自动/手动复位）
        8. 判定: triggered 为 True 且 reaction_time ≤ max_reaction_time
        9. 结果记录到 recorder 并返回（流程务必 try/finally 恢复工况）
        """
        raise NotImplementedError("TODO: 实现电网过/欠压保护公共流程")

    def grid_over_voltage_protection(self, voltage: float,
                                     max_reaction_time: float = 2.0,
                                     recover_voltage: float = 230.0) -> dict:
        """电网过压保护：AC 源输出过压，验证逆变器过压保护动作

        Args:
            voltage: 过压触发值（V，按产品规格，如 264.0）
            max_reaction_time: 保护动作时间上限（s），超出判 FAIL
            recover_voltage: 测试结束后的恢复电压（V，回到正常并网电压）

        Returns:
            {name, triggered, reaction_time, faults, waveform_path, passed}
        """
        return self._run_grid_voltage_protection("电网过压保护", voltage,
                                                 max_reaction_time, recover_voltage)

    def grid_under_voltage_protection(self, voltage: float,
                                      max_reaction_time: float = 2.0,
                                      recover_voltage: float = 230.0) -> dict:
        """电网欠压保护：AC 源输出欠压，验证逆变器欠压保护动作

        Args:
            voltage: 欠压触发值（V，按产品规格，如 180.0）
            max_reaction_time: 保护动作时间上限（s），超出判 FAIL
            recover_voltage: 测试结束后的恢复电压（V，回到正常并网电压）

        Returns:
            {name, triggered, reaction_time, faults, waveform_path, passed}
        """
        return self._run_grid_voltage_protection("电网欠压保护", voltage,
                                                 max_reaction_time, recover_voltage)

    # ---------------- 电网过/欠频保护（过欠频保护） ----------------

    def grid_over_frequency_protection(self, frequency: float,
                                       max_reaction_time: float = 2.0,
                                       recover_frequency: float = 50.0) -> dict:
        """电网过频保护：AC 源输出过频，验证逆变器过频保护动作

        Args:
            frequency: 过频触发值（Hz，按产品规格，如 50.5 / 51.0）
            max_reaction_time: 保护动作时间上限（s）
            recover_frequency: 恢复频率（Hz）

        Returns:
            {name, triggered, reaction_time, faults, waveform_path, passed}

        TODO 流程步骤: 同过压保护，仅 AC 源目标量为频率（复用 _run_grid_voltage_protection
        思路，抽公共 _run_grid_frequency_protection 实现）
        """
        raise NotImplementedError("TODO: 实现电网过频保护流程")

    def grid_under_frequency_protection(self, frequency: float,
                                        max_reaction_time: float = 2.0,
                                        recover_frequency: float = 50.0) -> dict:
        """电网欠频保护：AC 源输出欠频，验证逆变器欠频保护动作

        Args:
            frequency: 欠频触发值（Hz，按产品规格，如 49.5 / 49.0）
            max_reaction_time: 保护动作时间上限（s）
            recover_frequency: 恢复频率（Hz）

        Returns:
            {name, triggered, reaction_time, faults, waveform_path, passed}
        """
        raise NotImplementedError("TODO: 实现电网欠频保护流程")

    # ---------------- 反复高低电压穿越（反复高低穿） ----------------

    def voltage_ride_through(self, voltage_levels: list[float],
                             hold_time: float, times: int,
                             recover_voltage: float = 230.0) -> list[dict]:
        """反复高低电压穿越：按电压序列反复切换电网电压，验证逆变器穿越能力

        Args:
            voltage_levels: 高低电压序列（V，如 [253, 196, 253, 196]，
                            对应标准规定的高低穿电压值）
            hold_time: 每个电压档位保持时间（s，按标准如 2s/10s）
            times: 整组序列重复次数
            recover_voltage: 结束后的恢复电压（V）

        Returns:
            每个穿越点结果列表
            [{cycle, level_index, voltage, connected, support_reactive, waveform_path}, ...]

        TODO 流程步骤:
        1. 逆变器启动并网，确认运行状态
        2. 按电压序列循环 times 次：AC 源切换电压 -> 保持 hold_time
           -> 期间持续测量并网状态/功率/无功（低穿要求不脱网并支撑无功）
        3. 每次切换用示波器记录波形（start_waveform_recording / save_waveform）
        4. 校验每点: 逆变器未脱网（或按标准允许脱网后规定时间内重连）
        5. 全部完成后恢复电压，结果记录到 recorder
        """
        raise NotImplementedError("TODO: 实现反复高低电压穿越流程")

    # ---------------- 长期最大无功运行 ----------------

    def max_reactive_power_run(self, duration: float,
                               reactive_setpoint: float | None = None,
                               monitor_interval: float = 10.0) -> dict:
        """长期最大无功运行：逆变器以最大无功功率持续运行，验证长期稳定性

        Args:
            duration: 运行时长（s）
            reactive_setpoint: 无功设定值（Var）；None 时取设备最大无功能力
            monitor_interval: 状态监测采样周期（s）

        Returns:
            {name, duration, passed, max_temp, faults,
             stats: {reactive_power: {...}, temperature: {...}}}

        TODO 流程步骤:
        1. 逆变器启动并网，设置无功运行模式与设定值
        2. 按 monitor_interval 周期采样：无功功率（功分仪）/ 逆变器温度与状态
        3. 监测期间出现故障/停机则记录并终止，判定 FAIL
        4. 到达 duration 后统计无功波动与温升（DataAnalyzer）
        5. 校验: 全程无故障、无功输出稳定在设定值容差内
        """
        raise NotImplementedError("TODO: 实现长期最大无功运行流程")

    # ---------------- 其他通用流程（按需扩展） ----------------

    # TODO: 可扩展的通用流程示例
    #   - pv_over_current_protection(current): PV 侧过流保护
    #   - islanding_detection(): 孤岛检测（防孤岛保护）
    #   - soft_start_waveform_capture(): 缓启动波形捕获（复用缓启动 + 波形记录）
