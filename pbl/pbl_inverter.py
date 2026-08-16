"""逆变器复合操作（Public Business Layer）

需要 CL: cl_inverter + cl_pv + cl_ac + cl_meter（按测试场景组合）
"""
from pbl.base_pbl import BasePBL


class PblInverter(BasePBL):
    """逆变器复合业务

    将逆变器与外围设备编排为整机测试序列：
    - run_efficiency_test: 效率测试（多负载点，计算转换效率）
    - run_protection_test: 保护测试（过压/欠压/过流等保护动作验证）
    """

    __slots__ = ()

    @property
    def cl_inverter(self):
        return self._cl("cl_inverter")

    def run_efficiency_test(self, load_points: list[float],
                            settle_time: float = 60.0) -> list[dict]:
        """效率测试：在多个负载点（%额定功率）测量直流输入与交流输出，计算效率

        Args:
            load_points: 负载点列表（额定功率百分比，如 [25, 50, 75, 100]）
            settle_time: 每个负载点的稳定等待时间（秒）

        Returns:
            效率数据列表 [{load_percent, dc_voltage, dc_current, dc_power,
                           ac_power, efficiency}, ...]

        TODO:
        1. 逐负载点设置 PV 源工作点，使逆变器输出达到目标功率
        2. 稳定 settle_time 后用功分仪测交流侧、逆变器读直流侧
        3. 计算效率 = ac_power / dc_power，记录到 recorder
        4. 与基准效率比较（Compara.py 或直接按容差判定）
        """
        raise NotImplementedError("TODO: 实现逆变器效率测试序列")

    def run_protection_test(self, cases: list[dict]) -> list[dict]:
        """保护测试：逐项验证保护动作（过压/欠压/过流/过温等）

        Args:
            cases: 保护用例列表，每项形如
                   {"name": "过压保护", "param": "voltage", "value": 600.0, ...}

        Returns:
            每项结果列表 [{name, triggered, reaction_time, faults}, ...]

        TODO:
        1. 按用例设置异常工况（AC 过压 / PV 过流 / 电网异常等）
        2. 检测逆变器是否触发对应保护并记录反应时间与故障码
        3. 保护触发后恢复工况，确认逆变器可恢复正常（自动/手动）
        """
        raise NotImplementedError("TODO: 实现逆变器保护测试序列")
