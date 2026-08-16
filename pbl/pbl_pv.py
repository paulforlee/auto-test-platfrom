"""PV源复合操作（Public Business Layer）

需要 CL: cl_pv（MPPT 测试另需 cl_meter / cl_inverter）
"""
from pbl.base_pbl import BasePBL


class PblPV(BasePBL):
    """PV源复合业务

    将 PV 源原子操作编排为测试序列：
    - sweep_iv_curve: IV 曲线扫描（逐点设置工作点并记录）
    - run_mppt: MPPT 测试（模拟光照变化，验证最大功率点跟踪）
    """

    __slots__ = ()

    @property
    def cl_pv(self):
        return self._cl("cl_pv")

    def sweep_iv_curve(self, v_start: float, v_end: float, v_step: float,
                       current_limit: float) -> list[dict]:
        """IV 曲线扫描：从 v_start 到 v_end 按 v_step 逐点扫描

        Args:
            v_start: 起始电压（V）
            v_end: 终止电压（V）
            v_step: 电压步长（V）
            current_limit: 电流限值（A）

        Returns:
            扫描点数据列表 [{voltage, current, power}, ...]

        TODO:
        1. 开启输出并设置电流限值
        2. 逐点设置工作点电压，稳定后测量电压/电流/功率并记录
        3. 扫描结束关闭输出
        4. 数据交 pml.DataAnalyzer 计算 Voc/Isc/Pmax 等特征参数
        """
        raise NotImplementedError("TODO: 实现 PV IV 曲线扫描序列")

    def run_mppt(self, irradiance_profile: list[tuple[float, float]],
                 settle_time: float = 10.0) -> list[dict]:
        """MPPT 测试：按辐照度曲线变化模拟光照，验证最大功率点跟踪

        Args:
            irradiance_profile: [(时刻s, 辐照度W/m2), ...] 光照变化曲线
            settle_time: 每个光照档位的稳定等待时间（秒）

        Returns:
            跟踪数据列表 [{time, irradiance, voltage, current, power, mppt_eff}, ...]

        TODO:
        1. 按光照档位切换 PV 源 IV 曲线（需预先准备各档位曲线参数）
        2. 每档稳定 settle_time 后测量并记录
        3. 计算跟踪效率 mppt_eff = 实际功率 / 理论最大功率
        4. 校验跟踪效率是否满足指标（容差见 global_config.yaml）
        """
        raise NotImplementedError("TODO: 实现 PV MPPT 跟踪测试序列")
