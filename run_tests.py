"""测试运行入口

用法示例：
    python run_tests.py                                   # 运行全部用例
    python run_tests.py --case testcase/case/test_ac_soft_start.py
    python run_tests.py --report --mock                   # 生成 HTML 报告 + 模拟设备模式
"""
import argparse
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))  # 保证顶层模块（config/connection/driver/...）可 import


def build_pytest_args(case: str | None, env: str | None,
                      report: bool, mock: bool) -> list[str]:
    """构造 pytest 命令行参数

    Args:
        case: 单个用例文件路径；None 表示运行全部
        env: 环境名（对应 config/env_config.yml 中的环境）
        report: 是否生成 HTML 报告（输出到 doc/reports/html/）
        mock: 是否强制使用模拟设备
    """
    args: list[str] = []
    if case:
        args.append(case)
    if env:
        args.extend(["--env", env])
    if mock:
        args.append("-m mock")  # TODO: 确认与用例自身标记的组合方式（and/or）
    if report:
        report_dir = PROJECT_ROOT / "doc" / "reports" / "html"
        report_dir.mkdir(parents=True, exist_ok=True)
        args.extend(["--html", str(report_dir / "report.html"), "--self-contained-html"])
    return args


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="测试运行入口")
    parser.add_argument("--case", default=None, help="单个用例文件路径，默认运行全部")
    parser.add_argument("--env", default=None,
                        help="环境名（对应 config/env_config.yml），默认取 .env 的 TEST_ENV")
    parser.add_argument("--report", action="store_true", help="生成 HTML 报告到 doc/reports/html/")
    parser.add_argument("--mock", action="store_true", help="强制使用模拟设备（不连真实硬件）")
    args = parser.parse_args(argv)

    pytest_args = build_pytest_args(args.case, args.env, args.report, args.mock)
    exit_code = pytest.main(pytest_args)

    # TODO: 测试结束后调用 Compara.py，将实测数据与期望数据比对并生成比较报告
    return int(exit_code)


if __name__ == "__main__":
    raise SystemExit(main())
