"""计时器工具：@timeit 装饰器与 Timer 上下文管理器"""
import time
from contextlib import ContextDecorator
from functools import wraps

from utils.logger import get_logger


class Timer(ContextDecorator):
    """计时器：可用作装饰器或上下文管理器，自动记录耗时

    用法：
        @Timer("读取测量值")
        def measure(): ...

        with Timer("IV 曲线扫描") as t:
            ...
        print(t.elapsed)
    """

    def __init__(self, name: str = "操作", logger=None):
        self.name = name
        self.logger = logger or get_logger(__name__)
        self.elapsed: float = 0.0

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, *exc_info) -> bool:
        self.elapsed = time.perf_counter() - self._start
        self.logger.info("%s 耗时 %.3f s", self.name, self.elapsed)
        return False  # 不吞异常


def timeit(name: str | None = None, logger=None):
    """计时装饰器

    用法：
        @timeit()
        def f(): ...

        @timeit("设备初始化")
        def g(): ...
    """
    def decorator(func):
        label = name or func.__qualname__

        @wraps(func)
        def wrapper(*args, **kwargs):
            with Timer(label, logger=logger):
                return func(*args, **kwargs)
        return wrapper
    return decorator
