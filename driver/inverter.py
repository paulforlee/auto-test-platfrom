"""逆变器驱动（自定义 TCP 协议）"""
from driver.base_driver import BaseDriver


class InverterDriver(BaseDriver):
    """逆变器驱动

    逆变器采用私有 TCP 协议（连接层: TCPConnection），协议命令集中于此驱动。

    TODO:
    1. 按逆变器通讯协议文档定义命令帧常量
    2. start/stop/get_status/read_measurements/read_faults 基于
       self.connection.query 实现
    3. 确认是否需要心跳保活
    """

    # 逆变器协议非 SCPI，暂不使用 JSON 命令映射表
    DEFAULT_CMD_MAP = ""

    def __init__(self, connection, cmd_map_path=None, cmd_map=None):
        # 逆变器协议命令硬编码于本驱动（TODO: 确认后也可改为映射表驱动）
        super().__init__(connection, cmd_map_path=cmd_map_path,
                         cmd_map=cmd_map or {"device": "INVERTER", "commands": {}})

    # ---------------- 基础 ----------------

    def identify(self) -> str:
        """查询逆变器型号/版本信息"""
        # TODO: 发送版本查询帧，返回型号信息
        raise NotImplementedError("TODO: 实现逆变器版本查询")

    def reset(self) -> None:
        """逆变器复位（谨慎使用）"""
        # TODO: 发送复位帧
        raise NotImplementedError("TODO: 实现逆变器复位")

    # ---------------- 运行控制 ----------------

    def start(self) -> None:
        """启动逆变器并网运行"""
        # TODO: 发送启动指令帧，确认逆变器进入运行状态
        raise NotImplementedError("TODO: 实现逆变器启动")

    def stop(self) -> None:
        """停止逆变器运行"""
        # TODO: 发送停机指令帧，确认逆变器停机
        raise NotImplementedError("TODO: 实现逆变器停机")

    def get_status(self) -> str:
        """查询运行状态（如 STANDBY / RUNNING / FAULT）"""
        # TODO: 发送状态查询帧，返回状态码/状态字符串
        raise NotImplementedError("TODO: 实现运行状态查询")

    # ---------------- 测量 ----------------

    def measure_grid_voltage(self) -> float:
        """读取并网电压（V）"""
        raise NotImplementedError("TODO: 实现并网电压读取")

    def measure_grid_current(self) -> float:
        """读取并网电流（A）"""
        raise NotImplementedError("TODO: 实现并网电流读取")

    def measure_output_power(self) -> float:
        """读取输出功率（W）"""
        raise NotImplementedError("TODO: 实现输出功率读取")

    def measure_dc_voltage(self) -> float:
        """读取直流侧电压（V）"""
        raise NotImplementedError("TODO: 实现直流侧电压读取")

    def measure_dc_current(self) -> float:
        """读取直流侧电流（A）"""
        raise NotImplementedError("TODO: 实现直流侧电流读取")

    def measure_all(self) -> dict:
        """一次性读取全部运行参数

        Returns:
            {status, grid_voltage, grid_current, output_power,
             dc_voltage, dc_current}
        """
        raise NotImplementedError("TODO: 实现全量测量")

    # ---------------- 故障 ----------------

    def read_faults(self) -> list[str]:
        """读取故障码列表（空列表表示无故障）"""
        # TODO: 发送故障查询帧，解析故障码
        raise NotImplementedError("TODO: 实现故障码读取")
