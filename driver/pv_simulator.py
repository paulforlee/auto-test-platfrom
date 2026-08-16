"""PV源模拟器驱动（SCPI）"""
from driver.base_driver import BaseDriver


class PvSimulatorDriver(BaseDriver):
    """PV源模拟器驱动

    命令映射表: config/command_maps/pv_simulator_cmds.json
    支持工作点设置与 IV 曲线表格模式（用于 IV 扫描 / MPPT 测试）。

    TODO: 各方法按映射表调用 self._send / self._query_float 实现
    """

    DEFAULT_CMD_MAP = "pv_simulator_cmds.json"

    # ---------------- 基础 ----------------

    def identify(self) -> str:
        # TODO: return self._query("identify")
        raise NotImplementedError("TODO: 实现 *IDN? 查询")

    def reset(self) -> None:
        # TODO: self._send("reset")
        raise NotImplementedError("TODO: 实现设备复位")

    # ---------------- 输出控制 ----------------

    def set_voltage(self, voltage: float) -> None:
        """设置工作点电压（V）"""
        # TODO: self._send("set_voltage", value=self._fmt("voltage", voltage))
        raise NotImplementedError("TODO: 实现工作点电压设置")

    def set_current(self, current: float) -> None:
        """设置工作点电流（A）"""
        # TODO: self._send("set_current", value=self._fmt("current", current))
        raise NotImplementedError("TODO: 实现工作点电流设置")

    def set_iv_curve(self, points: list[tuple[float, float]]) -> None:
        """加载 IV 曲线表格（points: [(电压V, 电流A), ...]）"""
        # TODO:
        #   1. 逐点下发 set_iv_curve_point（index, voltage, current）
        #   2. 发送 load_iv_curve 激活表格模式
        raise NotImplementedError("TODO: 实现 IV 曲线表格加载")

    def set_mppt_mode(self, mode: str) -> None:
        """设置 MPPT 跟踪模式（mode 取值按设备手册，如 'ENABLE'/'DISABLE'）"""
        # TODO: self._send("set_mppt_mode", mode=mode)
        raise NotImplementedError("TODO: 实现 MPPT 模式设置")

    def output_on(self) -> None:
        """开启输出"""
        # TODO: self._send("output_on")
        raise NotImplementedError("TODO: 实现输出开启")

    def output_off(self) -> None:
        """关闭输出"""
        # TODO: self._send("output_off")
        raise NotImplementedError("TODO: 实现输出关闭")

    # ---------------- 测量 ----------------

    def measure_voltage(self) -> float:
        """测量输出电压（V）"""
        # TODO: return self._query_float("measure_voltage")
        raise NotImplementedError("TODO: 实现电压测量")

    def measure_current(self) -> float:
        """测量输出电流（A）"""
        # TODO: return self._query_float("measure_current")
        raise NotImplementedError("TODO: 实现电流测量")

    def measure_power(self) -> float:
        """测量输出功率（W）"""
        # TODO: return self._query_float("measure_power")
        raise NotImplementedError("TODO: 实现功率测量")

    def measure_all(self) -> dict:
        """一次性读取电压/电流/功率"""
        # TODO: 依次调用三个 measure 方法组装 dict
        raise NotImplementedError("TODO: 实现全量测量")

    # ---------------- 内部工具 ----------------

    def _fmt(self, kind: str, value: float) -> str:
        """按映射表 value_formats 格式化数值"""
        fmt = self.cmd_map.get("value_formats", {}).get(kind, "{:.3f}")
        return fmt.format(value)
