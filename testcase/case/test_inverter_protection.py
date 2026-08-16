"""逆变器保护测试"""
import pytest

pytestmark = pytest.mark.inverter


def test_protection_actions(inverter_pbl, test_params, recorder):
    """保护动作验证：过压/欠压/过流等异常工况下逆变器应触发对应保护

    TODO 实现步骤:
    1. 从 test_params["inverter_protection"] 取保护用例列表
    2. 逐项调用 inverter_pbl.run_protection_test(...)
    3. 校验: 保护触发 / 反应时间 ≤ 指标 / 故障码与预期一致
    4. 每项结束后恢复工况，确认逆变器可恢复正常
    """
    raise NotImplementedError("TODO: 实现逆变器保护测试用例")


def test_grid_voltage_sag_protection(inverter_pbl, test_params, recorder):
    """电网欠压保护：AC 侧电压跌落至阈值以下，逆变器应停机保护"""
    # TODO: AC 源输出降至阈值 → 检测逆变器停机与故障码 → 恢复电压确认可重连
    raise NotImplementedError("TODO: 实现欠压保护用例")
