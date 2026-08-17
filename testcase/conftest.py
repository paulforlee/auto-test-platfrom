"""测试用例级别的夹具：设备装配（连接 -> 驱动 -> CL -> PBL）与测试配置加载

装配链（session 级复用）：
    device_config.yaml
        -> connections（连接实例）
        -> device_drivers（驱动实例）
        -> cl_ac / cl_pv / cl_meter / cl_inverter（CL 实例）
        -> ac_pbl / pv_pbl / meter_pbl / inverter_pbl（PBL 实例，function 级，
           每个用例持有独立 recorder）
        -> ppl_schedule（PPL 公共流程调度器，function 级，组合所需 PBL）

骨架版本说明：设备连接尚未实现，device_drivers 夹具会跳过所有依赖硬件的用例。
TODO 实现顺序：
1. 按 device_config.yaml 用 connection.create_connection 建立连接
2. 用 driver.create_driver 创建各设备驱动
3. --mock 模式或连接失败时回退到模拟驱动（待实现 driver/mock/ 模拟设备包）
"""
from pathlib import Path

import pytest
import yaml

from utils.exceptions import ConfigError

TESTCASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = TESTCASE_DIR / "config"


def _load_yaml(name: str) -> dict:
    """加载 testcase/config/ 下的 YAML 配置"""
    path = CONFIG_DIR / name
    if not path.exists():
        raise ConfigError(f"测试配置文件不存在: {path}")
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


# ---------------- 配置夹具 ----------------

@pytest.fixture(scope="session")
def test_params() -> dict:
    """测试参数（电压范围、步长等），来自 testcase/config/test_params.yaml"""
    return _load_yaml("test_params.yaml")


@pytest.fixture(scope="session")
def device_config() -> dict:
    """设备连接参数，来自 testcase/config/device_config.yaml"""
    return _load_yaml("device_config.yaml")


# ---------------- 设备装配夹具 ----------------

@pytest.fixture(scope="session")
def device_drivers(device_config: dict) -> dict:
    """建立所有设备连接并创建驱动实例

    Returns:
        {设备键: 驱动实例}
    """
    # TODO:
    #   1. 遍历 device_config，用 connection.create_connection 建立连接并 open
    #   2. 用 driver.create_driver(model, connection, cmd_map) 创建驱动
    #   3. 若 pytest 命令行带 --mock 或连接失败，回退模拟驱动（TODO: driver/mock/）
    #   4. session 结束时统一 close 所有连接（用 yield + finally）
    pytest.skip("TODO: 设备连接与驱动装配尚未实现（骨架版本）")


@pytest.fixture(scope="session")
def cl_ac(device_drivers: dict):
    """AC源 CL 实例"""
    # TODO: return ClAC({"ac": device_drivers["ac_source"]})
    pytest.skip("TODO: CL 装配尚未实现（骨架版本）")


@pytest.fixture(scope="session")
def cl_pv(device_drivers: dict):
    """PV源 CL 实例"""
    # TODO: return ClPV({"pv": device_drivers["pv_simulator"]})
    pytest.skip("TODO: CL 装配尚未实现（骨架版本）")


@pytest.fixture(scope="session")
def cl_meter(device_drivers: dict):
    """功分仪 CL 实例"""
    # TODO: return ClMeter({"meter": device_drivers["power_meter"]})
    pytest.skip("TODO: CL 装配尚未实现（骨架版本）")


@pytest.fixture(scope="session")
def cl_inverter(device_drivers: dict):
    """逆变器 CL 实例"""
    # TODO: return ClInverter({"inverter": device_drivers["inverter"]})
    pytest.skip("TODO: CL 装配尚未实现（骨架版本）")


# ---------------- PBL 夹具（function 级，每个用例独立 recorder） ----------------

@pytest.fixture()
def recorder(request: pytest.FixtureRequest):
    """每个用例独立的数据记录器（数据存 testcase/data/raw/）"""
    from pml.data_recorder import DataRecorder
    rec = DataRecorder(request.node.name)
    yield rec
    # TODO: 用例结束时自动 save_csv / save_json（仅成功或始终保存？）
    rec.save_csv()


@pytest.fixture()
def ac_pbl(cl_ac, recorder, logger):
    """AC源 PBL 实例"""
    # TODO: return PblAC(cl_ac=cl_ac, recorder=recorder, logger=logger)
    pytest.skip("TODO: PBL 装配尚未实现（骨架版本）")


@pytest.fixture()
def pv_pbl(cl_pv, recorder, logger):
    """PV源 PBL 实例"""
    # TODO: return PblPV(cl_pv=cl_pv, recorder=recorder, logger=logger)
    pytest.skip("TODO: PBL 装配尚未实现（骨架版本）")


@pytest.fixture()
def meter_pbl(cl_meter, recorder, logger):
    """功分仪 PBL 实例"""
    # TODO: return PblMeter(cl_meter=cl_meter, recorder=recorder, logger=logger)
    pytest.skip("TODO: PBL 装配尚未实现（骨架版本）")


@pytest.fixture()
def inverter_pbl(cl_inverter, cl_pv, cl_ac, cl_meter, recorder, logger):
    """逆变器 PBL 实例（组合全部 CL）"""
    # TODO: return PblInverter(cl_inverter=cl_inverter, cl_pv=cl_pv,
    #                          cl_ac=cl_ac, cl_meter=cl_meter,
    #                          recorder=recorder, logger=logger)
    pytest.skip("TODO: PBL 装配尚未实现（骨架版本）")


# ---------------- PPL 夹具（function 级，组合所需 PBL） ----------------

@pytest.fixture()
def ppl_schedule(inverter_pbl, pv_pbl, ac_pbl, meter_pbl, recorder, logger):
    """PPL 公共流程调度器（跨设备组合流程，如电网过欠压/过欠频保护、高低穿）"""
    # TODO:
    #   from Common.ppl.ppl_schedule import PplSchedule
    #   return PplSchedule(pbl_inverter=inverter_pbl, pbl_pv=pv_pbl,
    #                      pbl_ac=ac_pbl, pbl_meter=meter_pbl,
    #                      recorder=recorder, logger=logger)
    # 注意: scope（示波器驱动）待 driver/oscilloscope.py 实现后接入
    pytest.skip("TODO: PPL 装配尚未实现（骨架版本）")
