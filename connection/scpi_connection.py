"""SCPI over TCP 连接（适用于 PRE2020S / IT6000C / PV 模拟器等 SCPI 仪器）"""
import socket

from connection.base_connection import BaseConnection
from utils.exceptions import DeviceConnectionError, DeviceTimeoutError


class SCPIConnection(BaseConnection):
    """SCPI over TCP 连接

    命令以 terminator（默认换行符）结尾，响应读取到 terminator 为止。

    TODO:
    1. open: 建立 TCP socket，设置超时
    2. query: send 后循环 recv 直到读到 terminator，strip 后返回
    3. 处理设备启动未就绪的重试逻辑（配合 utils.retry）
    """

    def __init__(self, host: str, port: int = 5025, timeout: float = 5.0,
                 terminator: str = "\n", encoding: str = "ascii", **kwargs):
        super().__init__(host=host, port=port, timeout=timeout, **kwargs)
        self.terminator = terminator
        self.encoding = encoding
        self._sock: socket.socket | None = None

    def open(self) -> None:
        """建立 TCP 连接"""
        # TODO:
        #   self._sock = socket.create_connection((self.host, self.port),
        #                                         timeout=self.timeout)
        #   self._sock.settimeout(self.timeout)
        #   self._connected = True
        raise NotImplementedError("TODO: 实现 SCPI TCP 连接建立")

    def close(self) -> None:
        """关闭 TCP 连接"""
        # TODO: shutdown + close，置 self._connected = False
        raise NotImplementedError("TODO: 实现 SCPI TCP 连接关闭")

    def send(self, data: str) -> None:
        """发送指令（追加终止符）"""
        # TODO: self._sock.sendall((data + self.terminator).encode(self.encoding))
        raise NotImplementedError("TODO: 实现 SCPI 指令发送")

    def query(self, data: str) -> str:
        """发送查询指令并读取响应

        Returns:
            去除终止符后的响应字符串
        """
        # TODO:
        #   self.send(data)
        #   循环 recv 直到收到 self.terminator（注意超时抛 DeviceTimeoutError）
        #   连接异常抛 DeviceConnectionError
        raise NotImplementedError("TODO: 实现 SCPI 查询")
