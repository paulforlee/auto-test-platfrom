"""连接抽象基类与连接工厂"""
from abc import ABC, abstractmethod
from typing import ClassVar

from utils.exceptions import DeviceConnectionError

# 连接类型注册表：{类型名: 连接类}
_CONNECTION_REGISTRY: dict[str, type["BaseConnection"]] = {}


def register_connection(conn_type: str, conn_cls: type["BaseConnection"]) -> None:
    """注册连接类型（在 connection/__init__.py 中调用）"""
    _CONNECTION_REGISTRY[conn_type] = conn_cls


def create_connection(conn_type: str, **cfg) -> "BaseConnection":
    """连接工厂：按类型创建连接实例（不建立连接，需手动 open）

    Args:
        conn_type: scpi / modbus / visa / tcp
        **cfg: 连接参数（host/port/timeout/resource_name/unit/...）

    Raises:
        DeviceConnectionError: 未注册的连接类型
    """
    conn_cls = _CONNECTION_REGISTRY.get(conn_type)
    if conn_cls is None:
        raise DeviceConnectionError(
            f"未知连接类型 '{conn_type}'，已注册: {list(_CONNECTION_REGISTRY)}")
    return conn_cls(**cfg)


class BaseConnection(ABC):
    """连接抽象基类

    所有连接实现需提供：
    - open/close：建立与断开物理连接
    - send：发送指令（不等待响应）
    - query：发送指令并返回响应
    - is_connected：连接状态

    支持上下文管理器：
        with create_connection("scpi", host=..., port=...) as conn:
            conn.query("*IDN?")
    """

    def __init__(self, host: str | None = None, port: int | None = None,
                 timeout: float = 5.0, **kwargs):
        """
        Args:
            host: 目标主机 IP（visa 类型可为 None）
            port: 目标端口（visa 类型可为 None）
            timeout: 通信超时（秒）
            **kwargs: 各连接类型特有参数（如 modbus 的 unit、scpi 的 terminator）
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self._connected = False

    # ---------------- 抽象接口 ----------------

    @abstractmethod
    def open(self) -> None:
        """建立物理连接，成功后置 is_connected 为 True"""

    @abstractmethod
    def close(self) -> None:
        """断开连接并释放资源，置 is_connected 为 False"""

    @abstractmethod
    def send(self, data: str) -> None:
        """发送指令（不等待响应）"""

    @abstractmethod
    def query(self, data: str) -> str:
        """发送指令并返回响应（去掉终止符后的纯文本）"""

    # ---------------- 通用实现 ----------------

    @property
    def is_connected(self) -> bool:
        """是否已连接"""
        return self._connected

    def __enter__(self) -> "BaseConnection":
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.close()
        return False

    def __repr__(self) -> str:
        state = "connected" if self._connected else "disconnected"
        return f"<{self.__class__.__name__} {self.host}:{self.port} ({state})>"
