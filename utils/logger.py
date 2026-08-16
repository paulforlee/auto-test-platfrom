"""日志工具：统一日志初始化与获取

日志级别由 config/global_config.yaml 的 logging 段控制（TODO: 接入）。
默认同时输出到控制台与 logs/test.log，错误另存 logs/error.log。
"""
import logging
from pathlib import Path

_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(log_dir: Path, level: int = logging.INFO) -> logging.Logger:
    """初始化全局日志配置，返回根 logger

    Args:
        log_dir: 日志目录（自动创建）
        level: 日志级别
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    root.setLevel(level)

    # 避免重复添加 handler（多次初始化时）
    if not root.handlers:
        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter(_FORMAT, _DATE_FORMAT))
        root.addHandler(console)

        test_handler = logging.FileHandler(log_dir / "test.log", encoding="utf-8")
        test_handler.setFormatter(logging.Formatter(_FORMAT, _DATE_FORMAT))
        root.addHandler(test_handler)

        error_handler = logging.FileHandler(log_dir / "error.log", encoding="utf-8")
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(_FORMAT, _DATE_FORMAT))
        root.addHandler(error_handler)

    # TODO: 从 global_config.yaml 读取日志级别覆盖默认值
    return root


def get_logger(name: str) -> logging.Logger:
    """获取指定名称的 logger"""
    return logging.getLogger(name)
