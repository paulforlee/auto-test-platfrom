"""AC源缓启动测试"""
import pytest

pytestmark = pytest.mark.ac


def test_soft_start_voltage_ramp(ac_pbl, test_params, recorder):
    """缓启动：分步升压至目标电压，校验每步电压与总超调

    TODO 实现步骤:
    1. 从 test_params["ac_soft_start"] 取电压/频率/步数/间隔
    2. 调用 ac_pbl.soft_start(...) 执行缓启动序列
    3. 用 pml.DataAnalyzer 计算每步稳态误差与超调量
    4. 按 config/global_config.yaml comparison 容差断言
    5. 失败时立即输出关机（fixture teardown 中处理）
    """
    raise NotImplementedError("TODO: 实现 AC 缓启动测试用例")


def test_soft_start_no_overshoot(ac_pbl, test_params, recorder):
    """缓启动过程电压不得超调（逐级单调上升）"""
    # TODO: 断言每步测量电压 ≤ 设定电压 × (1 + 容差)
    raise NotImplementedError("TODO: 实现缓启动超调校验用例")
