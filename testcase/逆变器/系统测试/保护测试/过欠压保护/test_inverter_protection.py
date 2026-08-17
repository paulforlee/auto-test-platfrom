"""逆变器保护测试"""
import pytest

pytestmark = pytest.mark.inverter
from Common.ppl.ppl_schedule import PplSchedule as PPL

def test_protection_actions(ppl_schedule, test_params, recorder):
    """保护动作验证：过压/欠压/过流等异常工况下逆变器应触发对应保护

    TODO 实现步骤:
    1. 从 test_params["inverter_protection"] 取保护用例列表
    2. 过/欠压项复用 Common/ppl 通用流程
       （ppl_schedule.grid_over/under_voltage_protection，含波形记录与保护时间），
       其余项调用 inverter_pbl.run_protection_test(...)
    3. 校验: 保护触发 / 反应时间 ≤ 指标 / 故障码与预期一致
    4. 每项结束后恢复工况，确认逆变器可恢复正常
    """

    PPL.start_waveform_recording()
    PPL.save_waveform()
    raise NotImplementedError("TODO: 实现逆变器保护测试用例")


def test_grid_voltage_sag_protection(ppl_schedule, test_params, recorder):
    """电网欠压保护：AC 侧电压跌落至阈值以下，逆变器应停机保护

    TODO: 优先复用 Common/ppl 的通用流程:
        result = ppl_schedule.grid_under_voltage_protection(
            voltage=test_params["inverter_protection"]["cases"][1]["value"],
            max_reaction_time=test_params["inverter_protection"]["max_reaction_time"])
        assert result["passed"]  # 含保护触发/反应时间/波形文件路径
    """
    raise NotImplementedError("TODO: 实现欠压保护用例")
