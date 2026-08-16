"""CL 基类：持有仪器（驱动）实例的 inst 插槽"""
from abc import ABC, abstractmethod

from driver.base_driver import BaseDriver


class BaseCL(ABC):
    """CL 基类

    通过 __slots__ 提供 inst 插槽：{设备键: 驱动实例}，
    各 CL 子类经由 _driver(key) 获取对应驱动，实现单步原子操作。
    """

    __slots__ = ("_inst",)  # inst 插槽

    def __init__(self, inst: dict[str, BaseDriver] | None = None):
        """
        Args:
            inst: 设备键 -> 驱动实例 的映射，如 {"ac": Pre2020sDriver, "meter": ...}
        """
        self._inst = inst or {}

    @property
    def inst(self) -> dict[str, BaseDriver]:
        """inst 插槽：{设备键: 驱动实例}"""
        return self._inst

    def _driver(self, key: str) -> BaseDriver:
        """按设备键获取驱动实例

        Raises:
            KeyError: 设备键不存在
        """
        if key not in self._inst:
            raise KeyError(f"CL 实例中不存在设备 '{key}'，可用设备: {list(self._inst)}")
        return self._inst[key]

    @abstractmethod
    def measure_all(self) -> dict:
        """一次性读取本设备全部测量量（原子操作）"""
