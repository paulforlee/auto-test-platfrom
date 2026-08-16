"""PyVisa 连接（GPIB / USB / 串口等 VISA 资源）"""
from connection.base_connection import BaseConnection
from utils.exceptions import DeviceConnectionError


class VisaConnection(BaseConnection):
    """PyVisa 连接

    适用于 GPIB / USB / 串口等 VISA 资源（使用 pyvisa-py 纯 Python 后端，
    免装 NI-VISA；如有 NI-VISA 会自动优先使用）。

    TODO:
    1. open: pyvisa.ResourceManager 打开 resource_name
    2. query: 使用 resource.query，需注意设备终止符
    """

    def __init__(self, resource_name: str, timeout: float = 5.0,
                 terminator: str = "\n", **kwargs):
        """
        Args:
            resource_name: VISA 资源名，如 "GPIB0::5::INSTR" / "USB0::0x1234::0x5678::INSTR"
            terminator: 读写终止符
        """
        super().__init__(host=None, port=None, timeout=timeout, **kwargs)
        self.resource_name = resource_name
        self.terminator = terminator
        self._resource = None  # pyvisa Resource

    def open(self) -> None:
        """打开 VISA 资源"""
        # TODO:
        #   import pyvisa
        #   rm = pyvisa.ResourceManager()          # pyvisa-py 后端
        #   self._resource = rm.open_resource(self.resource_name)
        #   self._resource.timeout = self.timeout * 1000  # pyvisa 超时单位为 ms
        #   self._resource.write_termination = self.terminator
        #   self._resource.read_termination = self.terminator
        #   self._connected = True
        #   失败抛 DeviceConnectionError
        raise NotImplementedError("TODO: 实现 VISA 资源打开（pyvisa）")

    def close(self) -> None:
        """关闭 VISA 资源"""
        # TODO: self._resource.close()，置 self._connected = False
        raise NotImplementedError("TODO: 实现 VISA 资源关闭")

    def send(self, data: str) -> None:
        """发送指令"""
        # TODO: self._resource.write(data)
        raise NotImplementedError("TODO: 实现 VISA 指令发送")

    def query(self, data: str) -> str:
        """发送查询指令并读取响应"""
        # TODO: self._resource.query(data)（注意返回末尾终止符处理）
        raise NotImplementedError("TODO: 实现 VISA 查询")
