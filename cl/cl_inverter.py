"""逆变器原子操作（Common Layer）

用法：
    cl_inv = ClInverter({"inverter": inverter_driver})
    cl_inv.start()
    status = cl_inv.get_status()
    faults = cl_inv.read_faults()
"""
from cl.base_cl import BaseCL


class ClInverter(BaseCL):
    """逆变器原子操作层

    inst 插槽键: "inverter"
    """

    __slots__ = ()

    def start(self) -> None:
        """启动逆变器并网运行"""
        # TODO: self._driver("inverter").start()
        raise NotImplementedError("TODO: 实现逆变器启动")

    def stop(self) -> None:
        """停止逆变器运行"""
        # TODO: self._driver("inverter").stop()
        raise NotImplementedError("TODO: 实现逆变器停机")

    def get_status(self) -> str:
        """查询运行状态"""
        # TODO: return self._driver("inverter").get_status()
        raise NotImplementedError("TODO: 实现运行状态查询")

    def read_faults(self) -> list[str]:
        """读取故障码列表（空列表表示无故障）"""
        # TODO: return self._driver("inverter").read_faults()
        raise NotImplementedError("TODO: 实现故障码读取")

    def measure_all(self) -> dict:
        """读取逆变器全部运行参数"""
        # TODO: return self._driver("inverter").measure_all()
        raise NotImplementedError("TODO: 实现逆变器全量测量")
