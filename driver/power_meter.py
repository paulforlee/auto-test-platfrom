"""功分仪驱动（ModbusTCP）"""
from driver.base_driver import BaseDriver


class PowerMeterDriver(BaseDriver):
    """功分仪驱动

    命令映射表: config/command_maps/power_meter_cmds.json（Modbus 寄存器表）
    与 SCPI 类驱动不同，命令映射表中每项为寄存器描述
    （function/address/count/data_type/scale/unit）。

    TODO:
    - _read(name): 按映射表读寄存器并解析（float32 需按 byte_order 组字）
    - 各 measure 方法基于 _read 实现
    """

    DEFAULT_CMD_MAP = "power_meter_cmds.json"

    # ---------------- 基础 ----------------

    def identify(self) -> str:
        """功分仪一般无 *IDN?，返回映射表中的设备描述"""
        return f"{self.cmd_map.get('device')}: {self.cmd_map.get('description', '')}"

    def reset(self) -> None:
        """功分仪一般无复位命令，置为空操作"""
        # TODO: 确认设备是否支持复位命令（部分型号有复功率/清零命令）
        pass

    # ---------------- 测量 ----------------

    def _read(self, name: str) -> float:
        """按映射表读取单个测量量

        Args:
            name: 测量量名（read_voltage / read_current / read_power / ...）

        TODO:
        1. 取映射表该命令的 function/address/count
        2. 调用 self.connection.read_holding_registers(address, count)
        3. 按 data_type（float32/uint16/uint32）+ byte_order 解析原始寄存器
        4. 乘以 scale 返回物理值
        """
        raise NotImplementedError("TODO: 实现 Modbus 寄存器读取与解析")

    def measure_voltage(self) -> float:
        """测量电压（V）"""
        # TODO: return self._read("read_voltage")
        raise NotImplementedError("TODO: 实现电压测量")

    def measure_current(self) -> float:
        """测量电流（A）"""
        # TODO: return self._read("read_current")
        raise NotImplementedError("TODO: 实现电流测量")

    def measure_power(self) -> float:
        """测量功率（W）"""
        # TODO: return self._read("read_power")
        raise NotImplementedError("TODO: 实现功率测量")

    def measure_frequency(self) -> float:
        """测量频率（Hz）"""
        # TODO: return self._read("read_frequency")
        raise NotImplementedError("TODO: 实现频率测量")

    def measure_power_factor(self) -> float:
        """测量功率因数"""
        # TODO: return self._read("read_power_factor")
        raise NotImplementedError("TODO: 实现功率因数测量")

    def measure_energy(self) -> float:
        """读取累计电能（kWh）"""
        # TODO: return self._read("read_energy")
        raise NotImplementedError("TODO: 实现电能读取")

    def measure_all(self) -> dict:
        """一次性读取电压/电流/功率/频率/功率因数"""
        # TODO: 依次调用各 measure 方法组装 dict
        raise NotImplementedError("TODO: 实现全量测量")
