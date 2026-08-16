"""顶层数据比较与报告生成入口

将测试实测数据（pml 层输出）与期望/基准数据进行比较，
按容差判定 PASS/FAIL，并基于 doc/templates/report_template.html 生成 HTML 报告。

用法：
    python Compara.py --expected <期望数据路径> --actual <实测数据路径> --out <报告输出目录>
"""
import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))


@dataclass
class ComparisonItem:
    """单条比较结果"""
    name: str                      # 参数名（如 "output_voltage"）
    expected: float                # 期望值
    actual: float                  # 实测值
    tolerance: float               # 容差（相对值，如 0.05 表示 ±5%）
    unit: str = ""
    passed: bool = False           # 是否在容差范围内
    deviation: float = 0.0         # 相对偏差
    notes: str = ""


@dataclass
class ComparisonReport:
    """整体比较报告"""
    title: str = "测试数据比较报告"
    items: list[ComparisonItem] = field(default_factory=list)

    @property
    def all_passed(self) -> bool:
        return all(item.passed for item in self.items)


class DataComparer:
    """数据比较器：加载期望数据与实测数据，逐项比较并生成报告

    TODO:
    1. load_expected / load_actual 支持 CSV、JSON、Excel 三种格式
    2. compare 按 config/global_config.yaml 的 comparison 容差配置逐项判定
    3. render_report 用 Jinja2 渲染 doc/templates/report_template.html
    """

    def __init__(self, tolerance_map: dict[str, float] | None = None):
        """Args:
            tolerance_map: 参数名 -> 容差的映射；None 时使用 global_config.yaml 默认值
        """
        self.tolerance_map = tolerance_map or {}

    def load_expected(self, path: Path) -> dict[str, float]:
        """加载期望/基准数据 -> {参数名: 期望值}"""
        # TODO: 按文件扩展名分发（CSV / JSON / Excel）
        raise NotImplementedError("TODO: 实现期望数据加载")

    def load_actual(self, path: Path) -> dict[str, float]:
        """加载实测数据 -> {参数名: 实测值}"""
        # TODO: 按文件扩展名分发（CSV / JSON / Excel）
        raise NotImplementedError("TODO: 实现实测数据加载")

    def compare(self, expected: dict[str, float], actual: dict[str, float]) -> ComparisonReport:
        """逐项比较，按容差判定 PASS/FAIL"""
        # TODO:
        #   - 取两者参数名并集，缺失项记为 FAIL 并注明 notes
        #   - 相对偏差 = |actual - expected| / |expected|
        #   - 使用 self.tolerance_map 或全局默认容差
        raise NotImplementedError("TODO: 实现逐项容差比较")

    def render_report(self, report: ComparisonReport, output_dir: Path) -> Path:
        """基于 doc/templates/report_template.html 渲染 HTML 报告，返回报告文件路径"""
        # TODO: Jinja2 渲染模板，输出到 output_dir/comparison_report.html
        raise NotImplementedError("TODO: 实现报告渲染")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="数据比较与报告生成")
    parser.add_argument("--expected", required=True, help="期望/基准数据文件路径")
    parser.add_argument("--actual", required=True, help="实测数据文件路径")
    parser.add_argument("--out", default=str(PROJECT_ROOT / "doc" / "reports" / "html"),
                        help="报告输出目录")
    args = parser.parse_args(argv)

    comparer = DataComparer()
    report = comparer.compare(
        comparer.load_expected(Path(args.expected)),
        comparer.load_actual(Path(args.actual)),
    )
    comparer.render_report(report, Path(args.out))
    return 0 if report.all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
