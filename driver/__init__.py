"""driver 驱动层：协议翻译

每种设备一个驱动类，命令由 config/command_maps/*.json 映射表驱动，
协议变动只需改映射表。

通过设备型号创建驱动：
    create_driver("PRE2020S", connection, cmd_map_path)
"""
from driver.base_driver import BaseDriver  # noqa: F401
from driver.inverter import InverterDriver  # noqa: F401
from driver.it6000c import It6000cDriver  # noqa: F401
from driver.power_meter import PowerMeterDriver  # noqa: F401
from driver.pre2020s import Pre2020sDriver  # noqa: F401
from driver.pv_simulator import PvSimulatorDriver  # noqa: F401

from utils.exceptions import ConfigError  # noqa: F401

# 设备型号 -> 驱动类
_DRIVER_REGISTRY: dict[str, type[BaseDriver]] = {
    "PRE2020S": Pre2020sDriver,
    "IT6000C": It6000cDriver,
    "PV_SIMULATOR": PvSimulatorDriver,
    "POWER_METER": PowerMeterDriver,
    "INVERTER": InverterDriver,
}


def create_driver(model: str, connection, cmd_map_path: str | None = None) -> BaseDriver:
    """按设备型号创建驱动实例

    Args:
        model: 设备型号（对应 env_config.yml 中设备的 model 字段）
        connection: BaseConnection 实例
        cmd_map_path: 命令映射表 JSON 路径，None 时按型号自动查找

    Raises:
        ConfigError: 未注册的设备型号
    """
    driver_cls = _DRIVER_REGISTRY.get(model.upper())
    if driver_cls is None:
        raise ConfigError(f"未注册的设备型号 '{model}'，已注册: {list(_DRIVER_REGISTRY)}")
    return driver_cls(connection, cmd_map_path=cmd_map_path)
