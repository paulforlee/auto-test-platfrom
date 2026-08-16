"""功分仪原子操作（Common Layer）

用法：
    cl_meter = ClMeter({"meter": power_meter_driver})
    data = cl_meter.read_measurements()
"""
from cl.base_cl import BaseCL


class ClMeter(BaseCL):
    """功分仪原子操作层

    inst 插槽键: "meter"
    """

    __slots__ = ()

    def read_measurements(self) -> dict:
        """读取电压/电流/功率/频率/功率因数（单次快照）"""
        # TODO: return self._driver("meter").measure_all()
        raise NotImplementedError("TODO: 实现功分仪测量快照")

    def read_energy(self) -> float:
        """读取累计电能（kWh）"""
        # TODO: return self._driver("meter").measure_energy()
        raise NotImplementedError("TODO: 实现累计电能读取")

    def measure_all(self) -> dict:
        """别名：与 read_measurements 等价，统一 CL 层接口"""
        return self.read_measurements()
