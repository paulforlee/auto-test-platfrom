"""PBL 基类：持有各 CL 实例的 inst 插槽与公共组件（logger/recorder）"""
from abc import ABC
from logging import Logger

from cl.cl_ac import ClAC
from cl.cl_inverter import ClInverter
from cl.cl_meter import ClMeter
from cl.cl_pv import ClPV


class BasePBL(ABC):
    """PBL 基类

    通过 __slots__ 提供 inst 插槽（cl_ac / cl_pv / cl_meter / cl_inverter），
    并持有 logger 与 DataRecorder 用于日志与测试数据记录。
    """

    __slots__ = ("_inst", "logger", "recorder")  # inst 插槽 + 公共组件

    def __init__(self, *,
                 cl_ac: ClAC | None = None,
                 cl_pv: ClPV | None = None,
                 cl_meter: ClMeter | None = None,
                 cl_inverter: ClInverter | None = None,
                 logger: Logger | None = None,
                 recorder=None):
        """
        Args:
            cl_ac/cl_pv/cl_meter/cl_inverter: 各 CL 实例，按测试场景传入所需部分
            logger: 日志记录器（默认使用模块 logger）
            recorder: pml.DataRecorder 实例，用于记录测试数据
        """
        self._inst = {
            "cl_ac": cl_ac,
            "cl_pv": cl_pv,
            "cl_meter": cl_meter,
            "cl_inverter": cl_inverter,
        }
        import logging
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self.recorder = recorder

    @property
    def inst(self) -> dict:
        """inst 插槽：{"cl_ac": ..., "cl_pv": ..., "cl_meter": ..., "cl_inverter": ...}"""
        return self._inst

    def _cl(self, key: str):
        """按键获取 CL 实例，缺失时抛 ValueError（提示该 PBL 需要哪个 CL）"""
        cl = self._inst.get(key)
        if cl is None:
            raise ValueError(f"{self.__class__.__name__} 需要 '{key}'，但未传入对应 CL 实例")
        return cl

    def _record(self, **fields) -> None:
        """向 DataRecorder 记录一条数据（未配置 recorder 时忽略）"""
        if self.recorder is not None:
            self.recorder.record(**fields)
