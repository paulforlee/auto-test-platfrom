"""PV源原子操作（Common Layer）

用法：
    cl_pv = ClPV({"pv": pv_simulator_driver})
    cl_pv.set_operating_point(voltage=300.0, current=5.0)
    cl_pv.output_on()
"""
from cl.base_cl import BaseCL

class ClPV(BaseCL):
    """PV源模拟器原子操作层

    inst 插槽键: "pv"
    """

    __slots__ = ()

    def set_operating_point(self, voltage: float, current: float) -> None:
        """设置工作点（电压 + 电流）

        TODO: 依次调用驱动的 set_voltage / set_current
        """
        raise NotImplementedError("TODO: 实现 PV 工作点设置")

    def set_iv_curve(self, points: list[tuple[float, float]]) -> None:
        """加载 IV 曲线表格（points: [(电压V, 电流A), ...]）"""
        # TODO: self._driver("pv").set_iv_curve(points)
        raise NotImplementedError("TODO: 实现 PV IV 曲线加载")

    def set_mppt_mode(self, mode: str) -> None:
        """设置 MPPT 跟踪模式"""
        # TODO: self._driver("pv").set_mppt_mode(mode)
        raise NotImplementedError("TODO: 实现 PV MPPT 模式设置")

    def output_on(self) -> None:
        """开启输出"""
        # TODO: self._driver("pv").output_on()
        raise NotImplementedError("TODO: 实现 PV 输出开启")

    def output_off(self) -> None:
        """关闭输出"""
        # TODO: self._driver("pv").output_off()
        raise NotImplementedError("TODO: 实现 PV 输出关闭")

    def measure_all(self) -> dict:
        """读取 PV 输出电压/电流/功率"""
        # TODO: return self._driver("pv").measure_all()
        raise NotImplementedError("TODO: 实现 PV 全量测量")
