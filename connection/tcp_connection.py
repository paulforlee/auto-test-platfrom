"""自定义 TCP 协议连接（适用于逆变器等私有协议设备）"""
import socket

from connection.base_connection import BaseConnection
from utils.exceptions import DeviceConnectionError, DeviceTimeoutError


class TCPConnection(BaseConnection):
    """自定义 TCP 协议连接

    逆变器采用私有 TCP 协议（非标准 SCPI/Modbus），帧格式与心跳机制待确认。

    TODO:
    1. open: 建立 TCP socket，设置超时与 keepalive
    2. send: 按私有协议组帧（帧头/长度/校验/帧尾）
    3. query: 收帧并按协议解帧，校验和校验失败抛 DeviceResponseError
    4. 心跳保活线程（如协议要求）
    """

    def __init__(self, host: str, port: int = 8899, timeout: float = 5.0, **kwargs):
        super().__init__(host=host, port=port, timeout=timeout, **kwargs)
        self._sock: socket.socket | None = None

    def open(self) -> None:
        """建立 TCP 连接"""
        # TODO:
        #   self._sock = socket.create_connection((self.host, self.port),
        #                                         timeout=self.timeout)
        #   self._sock.settimeout(self.timeout)
        #   self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        #   self._connected = True
        raise NotImplementedError("TODO: 实现私有 TCP 连接建立")

    def close(self) -> None:
        """关闭 TCP 连接"""
        # TODO: shutdown + close，置 self._connected = False
        raise NotImplementedError("TODO: 实现私有 TCP 连接关闭")

    def send(self, data: str) -> None:
        """按私有协议组帧并发送"""
        # TODO: 组帧（帧头 + 长度 + 载荷 + 校验 + 帧尾）后发送
        raise NotImplementedError("TODO: 实现私有协议组帧与发送")

    def query(self, data: str) -> str:
        """发送并等待响应帧"""
        # TODO: 发送后按协议解帧，返回载荷内容；超时抛 DeviceTimeoutError
        raise NotImplementedError("TODO: 实现私有协议收帧与解析")
