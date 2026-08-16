"""ModbusTCP 连接（适用于功分仪等 Modbus 设备）"""
from connection.base_connection import BaseConnection
from utils.exceptions import DeviceConnectionError, DeviceTimeoutError


class ModbusTCPConnection(BaseConnection):
    """ModbusTCP 连接

    基于 pymodbus 实现，支持保持寄存器读写（功分仪测量值均为保持寄存器）。

    TODO:
    1. open: 创建 pymodbus ModbusTcpClient 并 connect
    2. read_holding_registers / write_register: 调用 pymodbus，检查异常响应
    3. 按 command_maps/power_meter_cmds.json 的 data_type/byte_order 解析寄存器值
    """

    def __init__(self, host: str, port: int = 502, timeout: float = 5.0,
                 unit: int = 1, **kwargs):
        """
        Args:
            unit: Modbus 从站地址
        """
        super().__init__(host=host, port=port, timeout=timeout, **kwargs)
        self.unit = unit
        self._client = None  # pymodbus ModbusTcpClient

    def open(self) -> None:
        """建立 ModbusTCP 连接"""
        # TODO:
        #   from pymodbus.client import ModbusTcpClient
        #   self._client = ModbusTcpClient(self.host, port=self.port,
        #                                  timeout=self.timeout)
        #   self._connected = self._client.connect()
        #   失败抛 DeviceConnectionError
        raise NotImplementedError("TODO: 实现 ModbusTCP 连接建立（pymodbus）")

    def close(self) -> None:
        """关闭连接"""
        # TODO: self._client.close()，置 self._connected = False
        raise NotImplementedError("TODO: 实现 ModbusTCP 连接关闭")

    def send(self, data: str) -> None:
        """Modbus 为寄存器操作协议，一般不直接 send，见 read_holding_registers"""
        raise NotImplementedError("Modbus 连接请使用 read_holding_registers / write_register")

    def query(self, data: str) -> str:
        """Modbus 为寄存器操作协议，一般不直接 query，见 read_holding_registers"""
        raise NotImplementedError("Modbus 连接请使用 read_holding_registers / write_register")

    # ---------------- Modbus 特有接口 ----------------

    def read_holding_registers(self, address: int, count: int) -> list[int]:
        """读取保持寄存器原始值

        Args:
            address: 起始寄存器地址
            count: 寄存器数量

        Returns:
            原始寄存器值列表（int）

        TODO: pymodbus 调用 + 异常响应检查（超时抛 DeviceTimeoutError）
        """
        raise NotImplementedError("TODO: 实现保持寄存器读取")

    def write_register(self, address: int, value: int) -> None:
        """写单个保持寄存器"""
        raise NotImplementedError("TODO: 实现保持寄存器写入")
