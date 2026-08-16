"""设备连通性检查脚本

按配置逐个检查设备网络连通性与协议响应，输出状态表。

用法：
    python scripts/device_checker.py [--env Production_Line_3]

TODO:
1. TCP 层检查：socket 连接 + *IDN?（SCPI 设备）或寄存器读取（Modbus 设备）
2. 输出状态表：设备 / 型号 / IP:端口 / TCP / 协议响应 / 耗时
3. 任一设备不可达时退出码非 0（供 Jenkins 门禁使用）
"""
import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def check_device(name: str, cfg: dict) -> dict:
    """检查单台设备连通性

    Args:
        name: 设备键（如 ac_source）
        cfg: {model, connection: {...}}

    Returns:
        {device, model, host, port, tcp_ok, protocol_ok, elapsed, error}
    """
    # TODO:
    #   1. socket.create_connection 检查 TCP 连通性
    #   2. 按连接类型发送探测指令（SCPI: *IDN?；Modbus: 读寄存器）
    #   3. 返回检查结果（含异常信息）
    raise NotImplementedError("TODO: 实现设备连通性检查")


def check_all(env: str) -> list[dict]:
    """检查环境中全部设备"""
    # TODO: ConfigManager(env).load_local_env() 遍历调用 check_device
    raise NotImplementedError("TODO: 实现批量设备检查")


def print_status_table(results: list[dict]) -> None:
    """输出状态表"""
    # TODO: 对齐打印 设备/型号/IP:端口/TCP/协议/耗时/错误
    raise NotImplementedError("TODO: 实现状态表输出")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="设备连通性检查")
    parser.add_argument("--env", default="default", help="环境名")
    args = parser.parse_args(argv)

    results = check_all(args.env)
    print_status_table(results)
    return 0 if all(r.get("tcp_ok") and r.get("protocol_ok") for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
