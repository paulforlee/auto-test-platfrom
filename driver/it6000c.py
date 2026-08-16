"""IT6000C AC源驱动（SCPI）"""
from driver.base_driver import BaseDriver


class It6000cDriver(BaseDriver):
    """IT6000C AC源驱动

    命令映射表: config/command_maps/it6000c_cmds.json
    接口与 Pre2020sDriver 对齐（CL 层只依赖接口，不依赖具体型号）。

    TODO: 各方法按映射表调用 self._send / self._query_float 实现
    """

    DEFAULT_CMD_MAP = "it6000c_cmds.json"

    # ---------------- 基础 ----------------

    def identify(self) -> str:
        # TODO: return self._query("identify")
        raise NotImplementedError("TODO: 实现 *IDN? 查询")

    def reset(self) -> None:
        # TODO: self._send("reset")
        raise NotImplementedError("TODO: 实现设备复位")

    # ---------------- 输出控制 ----------------

    def set_voltage(self, voltage: float) -> None:
        """设置输出电压（V）"""
        # TODO: self._send("set_voltage", value=self._fmt("voltage", voltage))
        raise NotImplementedError("TODO: 实现输出电压设置")

    def set_frequency(self, frequency: float) -> None:
        """设置输出频率（Hz）"""
        # TODO: self._send("set_frequency", value=self._fmt("frequency", frequency))
        raise NotImplementedError("TODO: 实现输出频率设置")

    def set_current_limit(self, current: float) -> None:
        """设置输出电流限值（A）"""
        # TODO: self._send("set_current_limit", value=self._fmt("current", current))
        raise NotImplementedError("TODO: 实现电流限值设置")

    def output_on(self) -> None:
        """开启输出"""
        # TODO: self._send("output_on")
        raise NotImplementedError("TODO: 实现输出开启")

    def output_off(self) -> None:
        """关闭输出"""
        # TODO: self._send("output_off")
        raise NotImplementedError("TODO: 实现输出关闭")

    # ---------------- 测量 ----------------

    def measure_voltage(self) -> float:
        """测量输出电压（V）"""
        # TODO: return self._query_float("measure_voltage")
        raise NotImplementedError("TODO: 实现电压测量")

    def measure_current(self) -> float:
        """测量输出电流（A）"""
        # TODO: return self._query_float("measure_current")
        raise NotImplementedError("TODO: 实现电流测量")

    def measure_power(self) -> float:
        """测量输出功率（W）"""
        # TODO: return self._query_float("measure_power")
        raise NotImplementedError("TODO: 实现功率测量")

    def measure_frequency(self) -> float:
        """测量输出频率（Hz）"""
        # TODO: return self._query_float("measure_frequency")
        raise NotImplementedError("TODO: 实现频率测量")

    def measure_all(self) -> dict:
        """一次性读取电压/电流/功率/频率"""
        # TODO: 依次调用四个 measure 方法组装 dict
        raise NotImplementedError("TODO: 实现全量测量")

    # ---------------- 内部工具 ----------------

    def _fmt(self, kind: str, value: float) -> str:
        """按映射表 value_formats 格式化数值"""
        fmt = self.cmd_map.get("value_formats", {}).get(kind, "{:.3f}")
        return fmt.format(value)
