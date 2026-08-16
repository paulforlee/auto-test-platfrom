"""数据导出器：转 Excel / CSV

用法：
    DataExport.to_excel(records, Path("doc/reports/result.xlsx"))
    DataExport.to_csv(records, Path("testcase/data/raw/result.csv"))
"""
from pathlib import Path

from utils.exceptions import MeasurementError


class DataExport:
    """数据导出器

    TODO:
    1. to_excel: openpyxl 实现，支持多 sheet（原始数据 / 统计结果）
    2. 导出格式美化：表头样式、列宽自适应、数值格式
    3. 与 DataAnalyzer 联动：导出时附带统计行
    """

    @staticmethod
    def to_csv(records: list[dict], path: Path) -> Path:
        """导出 CSV（带表头）

        Args:
            records: 记录列表（dict 列表）
            path: 输出路径
        """
        # TODO: csv.DictWriter 导出（或复用 DataRecorder.save_csv）
        raise NotImplementedError("TODO: 实现 CSV 导出")

    @staticmethod
    def to_excel(records: list[dict], path: Path,
                 sheet_name: str = "data") -> Path:
        """导出 Excel（openpyxl）

        Args:
            records: 记录列表（dict 列表）
            path: 输出路径（.xlsx）
            sheet_name: 工作表名
        """
        if not records:
            raise MeasurementError("无数据可导出")
        # TODO:
        #   1. 表头取首条记录的字段顺序
        #   2. openpyxl 写入数据行
        #   3. 可选：追加统计 sheet（均值/极值，来自 DataAnalyzer.stats_all）
        raise NotImplementedError("TODO: 实现 Excel 导出（openpyxl）")
