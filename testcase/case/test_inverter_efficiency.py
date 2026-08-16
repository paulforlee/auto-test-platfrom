"""逆变器效率测试"""
import pytest

pytestmark = pytest.mark.inverter


def test_efficiency_curve(inverter_pbl, test_params, recorder):
    """效率曲线：多负载点测量直流输入与交流输出，计算转换效率

    TODO 实现步骤:
    1. 从 test_params["inverter_efficiency"] 取负载点列表与稳定时间
    2. 调用 inverter_pbl.run_efficiency_test(...) 逐负载点测试
    3. 校验各点效率 ≥ 指标值（如满载 ≥ 96%）
    4. 生成效率曲线数据（平台展示用，见 display_config.json）
    """
    raise NotImplementedError("TODO: 实现逆变器效率测试用例")


def test_maximum_power_point_efficiency(inverter_pbl, test_params, recorder):
    """满载点效率：额定功率下的转换效率应满足指标"""
    # TODO: 取额定负载点重复测量 N 次，取均值与指标比对
    raise NotImplementedError("TODO: 实现满载效率用例")
