"""数据分析器：计算统计值

用法：
    analyzer = DataAnalyzer(recorder.records)
    stats = analyzer.stats("voltage")   # {mean, min, max, std, p2p, count}
    eff = analyzer.efficiency("ac_power", "dc_power")
"""
import statistics

from utils.exceptions import MeasurementError


class DataAnalyzer:
    """数据分析器

    TODO:
    1. 支持 pandas DataFrame 输入（大数据量时性能更好）
    2. IV 曲线特征参数提取（Voc / Isc / Vmp / Imp / Pmax / 填充因子）
    3. MPPT 跟踪效率计算
    """

    def __init__(self, records: list[dict]):
        """
        Args:
            records: DataRecorder.records（list[dict]）或等价格式
        """
        if not records:
            raise MeasurementError("数据为空，无法分析")
        self.records = records
        self.fields = [k for k in records[0].keys()]

    def _values(self, key: str) -> list[float]:
        """提取指定字段的数值序列"""
        if not any(key in rec for rec in self.records):
            raise MeasurementError(f"数据中不存在字段 '{key}'，可用字段: {self.fields}")
        return [float(rec[key]) for rec in self.records if key in rec]

    def stats(self, key: str) -> dict:
        """计算单字段统计值：均值/最小值/最大值/标准差/峰峰值/样本数"""
        values = self._values(key)
        return {
            "key": key,
            "count": len(values),
            "mean": statistics.fmean(values),
            "min": min(values),
            "max": max(values),
            "std": statistics.stdev(values) if len(values) > 1 else 0.0,
            "p2p": max(values) - min(values),
        }

    def stats_all(self) -> dict[str, dict]:
        """计算全部数值字段的统计值"""
        return {key: self.stats(key) for key in self.fields if key != "time"}

    def efficiency(self, output_key: str, input_key: str) -> list[float]:
        """逐点计算效率 = output / input

        Args:
            output_key: 输出功率字段名（如 ac_power）
            input_key: 输入功率字段名（如 dc_power）

        Returns:
            每点的效率值列表（0~1）
        """
        outs = self._values(output_key)
        ins = self._values(input_key)
        if len(outs) != len(ins):
            raise MeasurementError(
                f"字段 '{output_key}' 与 '{input_key}' 样本数不一致")
        return [o / i if i else 0.0 for o, i in zip(outs, ins)]

    def to_dataframe(self):
        """转换为 pandas DataFrame（大数据量分析用）"""
        # TODO: import pandas as pd; return pd.DataFrame(self.records)
        raise NotImplementedError("TODO: 实现 DataFrame 转换（pandas）")
