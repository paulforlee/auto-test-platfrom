"""紧急停止脚本

异常情况下立即切断所有设备输出并断开连接（保证人身与设备安全）。

用法：
    python scripts/emergency_stop.py [--env Production_Line_3]

TODO:
1. 按 config/env_config.yml 遍历全部设备建立连接
2. 优先发送输出关闭指令（AC/PV 源 OUTP OFF，逆变器停机）
3. 指令失败时尝试直接断开连接（物理层强制断开）
4. 全部完成后输出执行结果；任一失败抛 EmergencyStopError
"""
import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def emergency_stop(env: str) -> dict:
    """对所有设备执行紧急停止

    Args:
        env: 环境名（对应 config/env_config.yml）

    Returns:
        {设备键: {action: 已执行动作, ok: bool}}
    """
    # TODO:
    #   1. ConfigManager(env).load_local_env() 取设备列表
    #   2. 逐设备创建连接 -> 创建驱动 -> output_off / stop
    #   3. 失败记录并继续处理下一台（不能因一台失败而中断急停）
    #   4. 最终统一关闭全部连接
    raise NotImplementedError("TODO: 实现紧急停止逻辑")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="紧急停止：切断所有设备输出")
    parser.add_argument("--env", default="default", help="环境名")
    args = parser.parse_args(argv)

    confirm = input(f"确认对环境 '{args.env}' 执行紧急停止? [y/N] ")
    if confirm.strip().lower() != "y":
        print("已取消")
        return 0

    result = emergency_stop(args.env)
    failed = {k: v for k, v in result.items() if not v.get("ok")}
    print(f"急停完成: {len(result) - len(failed)}/{len(result)} 台设备成功")
    if failed:
        print(f"失败设备: {list(failed)}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
