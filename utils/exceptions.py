"""自定义异常体系"""


class TestPlatformError(Exception):
    """平台所有异常的基类"""
    pass


class ConfigError(TestPlatformError):
    """配置错误：配置文件缺失/格式错误/字段缺失"""
    pass


class DeviceConnectionError(TestPlatformError):
    """设备连接错误：连接失败/断开/重连失败"""
    pass


class DeviceTimeoutError(TestPlatformError):
    """设备通信超时"""
    pass


class DeviceResponseError(TestPlatformError):
    """设备响应异常：返回格式无法解析/值超出合理范围"""
    pass


class MeasurementError(TestPlatformError):
    """测量数据错误：测量值异常、数据记录失败"""
    pass


class EmergencyStopError(TestPlatformError):
    """紧急停止执行失败（用于急停脚本）"""
    pass


class CloudApiError(TestPlatformError):
    """云平台接口错误：地址未配置 / 接口未定义 / HTTP 非 2xx / 网络异常 / 响应解析失败"""
    pass
