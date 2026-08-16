"""AC源复合操作（Public Business Layer）

需要 CL: cl_ac
"""
from pbl.base_pbl import BasePBL


class PblAC(BasePBL):
    """AC源复合业务

    将 AC 源原子操作编排为测试序列：
    - soft_start: 缓启动（逐级升压，记录每步数据）
    - power_cycle: 电源循环（按次数通断）
    """

    __slots__ = ()

    @property
    def cl_ac(self):
        return self._cl("cl_ac")

    def soft_start(self, voltage: float, frequency: float,
                   steps: int = 10, interval: float = 0.5) -> list[dict]:
        """缓启动：输出电压从 0 分 steps 级升至目标值

        Args:
            voltage: 目标电压（V）
            frequency: 输出频率（Hz）
            steps: 升压级数
            interval: 每级间隔（秒）

        Returns:
            每步测量数据列表 [{step, set_voltage, meas_voltage, meas_current}, ...]

        TODO:
        1. 设置频率与目标电压（输出保持关闭）
        2. 开启输出
        3. 按 steps 级逐级升压，每级等待 interval 后测量并记录
        4. 校验超调量与稳态误差（容差见 global_config.yaml comparison 段）
        5. 异常时立即关闭输出
        """
        raise NotImplementedError("TODO: 实现 AC 缓启动测试序列")

    def power_cycle(self, times: int, on_time: float, off_time: float,
                    voltage: float = 230.0, frequency: float = 50.0) -> list[dict]:
        """电源循环：按指定次数反复通断 AC 输出

        Args:
            times: 循环次数
            on_time: 每次上电持续时间（秒）
            off_time: 每次断电间隔（秒）
            voltage/frequency: 输出参数

        Returns:
            每轮循环数据列表 [{cycle, result, meas_voltage, ...}]

        TODO:
        1. 设置输出参数
        2. 循环 times 次：开输出 → 等待 on_time → 测量 → 关输出 → 等待 off_time
        3. 记录每轮结果，异常时记录失败原因并中断
        """
        raise NotImplementedError("TODO: 实现 AC 电源循环测试序列")
