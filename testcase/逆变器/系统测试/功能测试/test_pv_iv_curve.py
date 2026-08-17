"""PV源IV曲线测试"""
import pytest

pytestmark = pytest.mark.pv


def test_iv_curve_scan(pv_pbl, test_params, recorder):
    """IV 曲线扫描：逐点扫描并提取特征参数

    TODO 实现步骤:
    1. 从 test_params["pv_iv_curve"] 取起始/终止电压、步长、电流限值
    2. 调用 pv_pbl.sweep_iv_curve(...) 执行扫描
    3. 用 DataAnalyzer 提取 Voc / Isc / Vmp / Imp / Pmax
    4. 与期望 IV 曲线（testcase/data/ 下基准数据或 test_params 期望值）比对
    5. 数据保存后由 Compara.py 生成曲线对比报告
    """
    raise NotImplementedError("TODO: 实现 PV IV 曲线扫描用例")


def test_iv_curve_repeatability(pv_pbl, test_params, recorder):
    """IV 曲线重复性：连续两次扫描结果偏差应在容差内"""
    # TODO: 两次扫描逐点比较，偏差 ≤ global_config.yaml comparison 容差
    raise NotImplementedError("TODO: 实现 IV 曲线重复性用例")
