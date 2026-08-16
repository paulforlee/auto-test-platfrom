"""connection 物理连接层

支持四种连接方式，通过连接类型字符串创建：
    "scpi"   -> SCPIConnection
    "modbus" -> ModbusTCPConnection
    "visa"   -> VisaConnection
    "tcp"    -> TCPConnection
"""
from connection.base_connection import (  # noqa: F401
    BaseConnection,
    create_connection,
    register_connection,
)
from connection.modbus_connection import ModbusTCPConnection  # noqa: F401
from connection.scpi_connection import SCPIConnection  # noqa: F401
from connection.tcp_connection import TCPConnection  # noqa: F401
from connection.visa_connection import VisaConnection  # noqa: F401

# 注册默认连接类型
register_connection("scpi", SCPIConnection)
register_connection("modbus", ModbusTCPConnection)
register_connection("visa", VisaConnection)
register_connection("tcp", TCPConnection)
