"""AC源原子操作（Common Layer）

用法：
    cl_ac = ClAC({"ac": pre2020s_driver})
    cl_ac.set_output(voltage=230.0, frequency=50.0)
    cl_ac.output_on()
    data = cl_ac.measure_all()
"""
from cl.base_cl import BaseCL


class ClAC(BaseCL):
    """AC源原子操作层

    inst 插槽键: "ac"（PRE2020S 或 IT6000C 驱动实例，两者接口对齐）
    """

    __slots__ = ()

    def set_output(self, voltage: float, frequency: float,
                   current_limit: float | None = None) -> None:
        """设置输出参数（电压/频率/可选电流限值）

        TODO: 依次调用驱动的 set_voltage / set_frequency / set_current_limit
        """
        raise NotImplementedError("TODO: 实现 AC 输出参数设置")

    def output_on(self) -> None:
        """开启输出"""
        # TODO: self._driver("ac").output_on()
        raise NotImplementedError("TODO: 实现 AC 输出开启")

    def output_off(self) -> None:
        """关闭输出"""
        # TODO: self._driver("ac").output_off()
        raise NotImplementedError("TODO: 实现 AC 输出关闭")

    def measure_all(self) -> dict:
        """读取 AC 输出电压/电流/功率/频率"""
        # TODO: return self._driver("ac").measure_all()
        raise NotImplementedError("TODO: 实现 AC 全量测量")
