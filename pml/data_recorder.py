"""数据记录器：实时存储测试数据

用法：
    recorder = DataRecorder("soft_start_20260816_001")
    recorder.record(step=1, voltage=230.0, current=1.2)
    recorder.save_csv()   # -> testcase/data/raw/<name>.csv
    recorder.save_json()  # -> testcase/data/raw/<name>.json
"""
import csv
import json
import time
from pathlib import Path

from utils.exceptions import MeasurementError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = PROJECT_ROOT / "testcase" / "data" / "raw"


class DataRecorder:
    """数据记录器

    内存缓存 + 落盘保存。字段集合由首条记录决定（后续记录字段不一致时补空值）。

    TODO:
    1. 长时测试的实时落盘（缓冲刷盘策略，防止内存占用过大）
    2. 采样时间戳自动生成（当前为相对时刻，需确认是否要绝对时间）
    """

    def __init__(self, name: str, data_dir: Path | None = None):
        """
        Args:
            name: 记录名称（文件名主体，建议含用例名 + 时间戳）
            data_dir: 保存目录，默认 testcase/data/raw/
        """
        self.name = name
        self.data_dir = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
        self.records: list[dict] = []
        self.fields: list[str] = []
        self._start_time = time.monotonic()

    def record(self, **fields) -> None:
        """追加一条记录

        Args:
            **fields: 测量数据键值对；未提供 time 时自动填充相对时间（秒）

        Raises:
            MeasurementError: 首条记录无任何字段
        """
        if not fields and not self.fields:
            raise MeasurementError("记录至少需要一个字段")

        # 自动维护字段列表（保证后续导出列一致）
        for key in fields:
            if key not in self.fields:
                self.fields.append(key)

        if "time" not in fields:
            fields = {"time": round(time.monotonic() - self._start_time, 3), **fields}

        row = {key: fields.get(key) for key in self.fields}
        self.records.append(row)

    def save_csv(self, path: Path | None = None) -> Path:
        """保存为 CSV，返回文件路径

        Args:
            path: 输出路径；None 时默认 <data_dir>/<name>.csv
        """
        path = Path(path) if path else self.data_dir / f"{self.name}.csv"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(self.records)
        return path

    def save_json(self, path: Path | None = None) -> Path:
        """保存为 JSON，返回文件路径

        Args:
            path: 输出路径；None 时默认 <data_dir>/<name>.json
        """
        path = Path(path) if path else self.data_dir / f"{self.name}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"name": self.name, "records": self.records},
                      f, ensure_ascii=False, indent=2)
        return path

    def clear(self) -> None:
        """清空已记录数据"""
        self.records.clear()
        self.fields.clear()

    def __len__(self) -> int:
        return len(self.records)
