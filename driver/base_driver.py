"""驱动抽象基类：定义 set/get 统一接口与命令映射表机制"""
import json
from abc import ABC, abstractmethod
from pathlib import Path

from connection.base_connection import BaseConnection
from utils.exceptions import ConfigError, DeviceResponseError


class BaseDriver(ABC):
    """驱动抽象基类

    所有设备驱动继承本类，通过命令映射表（config/command_maps/*.json）解析
    具体协议命令，实现"协议变动只改配置"。

    子类需实现：
    - identify / reset
    - 设备专属的 set_xxx / measure_xxx 方法
    - measure_all：一次性读取全部测量量

    内置工具方法：
    - _cmd(name, **fmt): 取命令模板并格式化
    - _send(name, **fmt): 发送命令
    - _query(name, **fmt): 发送查询并返回响应
    - _query_float(name, **fmt): 查询并解析为 float
    """

    # 子类默认命令映射表文件名（相对 config/command_maps/）
    DEFAULT_CMD_MAP: str = ""

    def __init__(self, connection: BaseConnection,
                 cmd_map_path: str | None = None,
                 cmd_map: dict | None = None):
        """
        Args:
            connection: 已建立的设备连接（BaseConnection 子类实例）
            cmd_map_path: 命令映射表 JSON 路径；None 时按 DEFAULT_CMD_MAP 自动查找
            cmd_map: 直接传入映射表 dict（优先级最高，跳过文件加载）
        """
        self.connection = connection
        self.cmd_map = cmd_map or self.load_cmd_map(cmd_map_path)

    # ---------------- 命令映射表 ----------------

    def load_cmd_map(self, cmd_map_path: str | None = None) -> dict:
        """加载命令映射表 JSON

        Args:
            cmd_map_path: 映射表路径；None 时按 DEFAULT_CMD_MAP 在
                          config/command_maps/ 下查找
        """
        if cmd_map_path is None:
            if not self.DEFAULT_CMD_MAP:
                raise ConfigError(f"{self.__class__.__name__} 未定义 DEFAULT_CMD_MAP")
            cmd_map_path = str(
                Path(__file__).resolve().parent.parent
                / "config" / "command_maps" / self.DEFAULT_CMD_MAP)
        path = Path(cmd_map_path)
        if not path.exists():
            raise ConfigError(f"命令映射表不存在: {path}")
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    # ---------------- 命令工具方法 ----------------

    def _cmd(self, name: str, **fmt) -> str:
        """取命令模板并按参数格式化

        Args:
            name: 命令名（映射表 commands 段的键）
            **fmt: 模板占位参数，如 value=230.0
        """
        template = self.cmd_map.get("commands", {}).get(name)
        if template is None:
            raise ConfigError(f"命令映射表中不存在命令 '{name}'（设备: "
                              f"{self.cmd_map.get('device')}）")
        return template.format(**fmt) if fmt else template

    def _send(self, name: str, **fmt) -> None:
        """发送命令（不带响应）"""
        self.connection.send(self._cmd(name, **fmt))

    def _query(self, name: str, **fmt) -> str:
        """发送查询命令并返回原始响应"""
        return self.connection.query(self._cmd(name, **fmt))

    def _query_float(self, name: str, **fmt) -> float:
        """发送查询命令并解析为 float

        Raises:
            DeviceResponseError: 响应无法解析为数值
        """
        resp = self._query(name, **fmt)
        try:
            return float(resp)
        except (TypeError, ValueError) as exc:
            raise DeviceResponseError(
                f"命令 '{name}' 响应无法解析为数值: {resp!r}") from exc

    # ---------------- 抽象接口 ----------------

    @abstractmethod
    def identify(self) -> str:
        """查询设备标识（*IDN?），返回设备信息字符串"""

    @abstractmethod
    def reset(self) -> None:
        """设备复位（*RST）"""

    @abstractmethod
    def measure_all(self) -> dict:
        """一次性读取全部测量量

        Returns:
            {测量量名: {value, unit}}
        """

    def __repr__(self) -> str:
        return (f"<{self.__class__.__name__} "
                f"device={self.cmd_map.get('device', '?')} "
                f"conn={self.connection!r}>")
