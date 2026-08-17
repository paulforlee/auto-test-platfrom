"""AC源电源循环测试"""
import pytest

pytestmark = pytest.mark.ac


def test_power_cycle_stability(ac_pbl, test_params, recorder):
    """电源循环：反复通断输出，每轮上电后测量值应稳定

    TODO 实现步骤:
    1. 从 test_params["ac_power_cycle"] 取循环次数/通断时长/输出参数
    2. 调用 ac_pbl.power_cycle(...) 执行循环序列
    3. 校验每轮上电后电压/频率在容差内（见 global_config.yaml comparison）
    4. 全部轮次成功后数据交 DataAnalyzer 计算波动统计
    """
    raise NotImplementedError("TODO: 实现 AC 电源循环测试用例")
