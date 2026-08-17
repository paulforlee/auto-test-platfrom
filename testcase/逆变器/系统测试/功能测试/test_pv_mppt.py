"""PV源MPPT测试"""
import pytest

pytestmark = pytest.mark.pv


def test_mppt_tracking(pv_pbl, test_params, recorder):
    """MPPT 跟踪：按辐照度曲线变化，验证最大功率点跟踪效率

    TODO 实现步骤:
    1. 从 test_params["pv_mppt"] 取辐照度曲线与稳定时间
    2. 调用 pv_pbl.run_mppt(...) 执行跟踪序列
    3. 计算每个光照档位的跟踪效率（实际功率 / 理论最大功率）
    4. 校验跟踪效率 ≥ 指标值（如 98%）
    """
    raise NotImplementedError("TODO: 实现 PV MPPT 跟踪测试用例")


def test_mppt_response_time(pv_pbl, test_params, recorder):
    """MPPT 响应时间：光照阶跃变化后，跟踪到新最大功率点的时间应满足指标"""
    # TODO: 测量光照阶跃时刻到功率稳定的时间差，断言 ≤ 指标值
    raise NotImplementedError("TODO: 实现 MPPT 响应时间用例")
