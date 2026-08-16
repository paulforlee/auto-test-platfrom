"""重试工具：@retry 装饰器

设备通信类操作建议默认开启重试，次数与间隔见 config/global_config.yaml
的 device.retry_times / device.retry_interval（TODO: 接入配置）。
"""
import time
from functools import wraps

from utils.logger import get_logger


def retry(times: int = 3, delay: float = 1.0,
          exceptions: tuple[type[BaseException], ...] = (Exception,), logger=None):
    """重试装饰器

    Args:
        times: 最大尝试次数（含首次）
        delay: 每次重试前等待秒数
        exceptions: 触发重试的异常类型
        logger: 日志记录器，默认使用模块 logger

    用法：
        @retry(times=3, delay=1.0, exceptions=(DeviceTimeoutError,))
        def query_device(): ...
    """
    def decorator(func):
        log = logger or get_logger(__name__)

        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc: BaseException | None = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    if attempt < times:
                        log.warning("%s 第 %d/%d 次失败（%s），%.1fs 后重试",
                                    func.__qualname__, attempt, times, exc, delay)
                        time.sleep(delay)
            raise last_exc  # type: ignore[misc]

        return wrapper
    return decorator
