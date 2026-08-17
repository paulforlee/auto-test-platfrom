"""云平台接口请求封装（基于 requests）

接口 url 与请求方法统一定义在 Common/iot/interface.yml，
客户端加载接口定义后按名调用，业务方法逐个封装。

鉴权: 请求头 Authorization: Bearer <CLOUD_API_TOKEN>（.env 配置）

用法:
    client = IotClient()
    version = client.get_upgrade_version(device_sn="SN001")   # -> dict
    data = client.get_pv_stats(start="2026-08-01", end="2026-08-17")
"""
import logging
import os
from pathlib import Path

import requests
import yaml

from utils.exceptions import CloudApiError
from utils.retry import retry

logger = logging.getLogger(__name__)

DEFAULT_INTERFACE_YML = Path(__file__).resolve().parent / "interface.yml"


class IotClient:
    """云平台接口客户端

    内部机制：
    - 接口定义加载: 读 interface.yml，组装完整 url（base_url + path）
    - 鉴权: 自动附加 Bearer Token（CLOUD_API_TOKEN，.env 配置）
    - 重试: 网络类异常（超时/连接失败）按 utils.retry 自动重试
    - 错误: HTTP 非 2xx / 网络异常 / 响应解析失败统一抛 CloudApiError
    """

    def __init__(self, *,
                 base_url: str | None = None,
                 api_token: str | None = None,
                 interface_yml: str | Path | None = None,
                 timeout: float | None = None,
                 logger=None):
        """
        Args:
            base_url: 云平台地址，优先级: 参数 > 环境变量 CLOUD_API_URL > interface.yml
            api_token: API Token，优先级: 参数 > 环境变量 CLOUD_API_TOKEN
            interface_yml: 接口定义文件路径，默认 Common/iot/interface.yml
            timeout: 请求超时（秒），优先级: 参数 > interface.yml > 10.0
        """
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self.interface_yml = Path(interface_yml) if interface_yml else DEFAULT_INTERFACE_YML
        self._cfg = self._load_interfaces()

        # 加载项目根目录 .env（失败时忽略，环境变量可能已由外部设置）
        try:
            from dotenv import load_dotenv
            load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")
        except ImportError:
            pass

        self.base_url = (base_url or os.getenv("CLOUD_API_URL")
                         or self._cfg.get("base_url", "")).rstrip("/")
        if not self.base_url:
            raise CloudApiError("云平台地址未配置：请设置 CLOUD_API_URL 或 interface.yml 的 base_url")

        self.api_token = api_token or os.getenv("CLOUD_API_TOKEN", "")
        self.timeout = timeout or float(self._cfg.get("timeout", 10.0))
        self.session = requests.Session()
        if self.api_token:
            self.session.headers.update({"Authorization": f"Bearer {self.api_token}"})

    # ---------------- 接口定义加载 ----------------

    def _load_interfaces(self) -> dict:
        """加载 interface.yml 接口定义

        Returns:
            {base_url, timeout, interfaces: {接口名: {method, path, description, ...}}}
        """
        if not self.interface_yml.exists():
            raise CloudApiError(f"云平台接口定义文件不存在: {self.interface_yml}")
        with open(self.interface_yml, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def get_interface(self, name: str) -> dict:
        """查询接口定义（method + 完整 url）

        Args:
            name: 接口名（interface.yml 中 interfaces 的键）

        Returns:
            {"method": "GET", "url": "https://iot.com/api/v1/...", ...}
        """
        interfaces = self._cfg.get("interfaces", {})
        if name not in interfaces:
            raise CloudApiError(f"接口 '{name}' 未定义，可用接口: {list(interfaces)}")
        iface = dict(interfaces[name])
        path = iface.pop("path", "")
        iface["url"] = self.base_url + path
        return iface

    # ---------------- 通用请求 ----------------

    @retry(times=3, delay=1.0,
           exceptions=(requests.Timeout, requests.ConnectionError))
    def request(self, name: str, *,
                params: dict | None = None,
                json_body: dict | None = None,
                headers: dict | None = None,
                timeout: float | None = None) -> requests.Response:
        """按接口名执行请求（GET 走 params，POST 走 json_body）

        Args:
            name: 接口名（interface.yml 中定义）
            params: URL 查询参数（GET）
            json_body: JSON 请求体（POST）
            headers: 额外请求头（与鉴权头合并）
            timeout: 本次请求超时（秒），None 用默认值

        Returns:
            requests.Response（2xx 时返回；业务方法自行解析 json/二进制）

        Raises:
            CloudApiError: 接口未定义 / HTTP 非 2xx / 网络异常（重试耗尽）
        """
        iface = self.get_interface(name)
        method = iface["method"].upper()
        url = iface["url"]
        req_timeout = timeout or self.timeout

        try:
            resp = self.session.request(
                method, url, params=params, json=json_body,
                headers=headers, timeout=req_timeout)
        except requests.Timeout as exc:
            raise CloudApiError(f"请求超时 [{name}] {url}") from exc
        except requests.RequestException as exc:
            raise CloudApiError(f"网络异常 [{name}] {url}: {exc}") from exc

        if not resp.ok:
            raise CloudApiError(
                f"HTTP {resp.status_code} [{name}] {url}，响应: {resp.text[:200]}")
        return resp

    def get(self, name: str, params: dict | None = None, **kwargs) -> requests.Response:
        """GET 快捷方法"""
        return self.request(name, params=params, **kwargs)

    def post(self, name: str, json_body: dict | None = None, **kwargs) -> requests.Response:
        """POST 快捷方法"""
        return self.request(name, json_body=json_body, **kwargs)

    # ---------------- 业务接口（TODO: 按云平台接口文档核对参数与响应结构） ----------------

    def get_upgrade_version(self, device_sn: str | None = None) -> dict:
        """查询设备可升级版本信息

        Args:
            device_sn: 设备序列号（None 表示全部设备；TODO: 确认云平台实际参数名）

        Returns:
            升级版本信息 dict（结构以云平台接口文档为准）

        TODO: 确认请求参数名与响应字段（版本号/发布说明/升级包地址等）
        """
        params = {"device_sn": device_sn} if device_sn else None
        resp = self.request("upgrade_version", params=params)
        try:
            return resp.json()
        except ValueError as exc:
            raise CloudApiError(
                f"升级版本接口响应不是合法 JSON: {resp.text[:200]}") from exc

    def export_logs(self, device_sn: str,
                    start_time: str | None = None,
                    end_time: str | None = None) -> bytes:
        """导出设备日志

        Args:
            device_sn: 设备序列号
            start_time/end_time: 日志时间范围（格式以云平台文档为准，如 "2026-08-01 00:00:00"）

        Returns:
            日志文件原始内容（bytes）；若云平台返回下载地址而非文件内容，需调整解析逻辑

        TODO: 确认请求参数与响应格式（二进制文件流 / JSON 下载地址）
        """
        json_body = {
            "device_sn": device_sn,
            "start_time": start_time,
            "end_time": end_time,
        }
        resp = self.request("log_export", json_body=json_body)
        return resp.content

    def get_pv_stats(self, device_sn: str | None = None,
                     start: str | None = None,
                     end: str | None = None) -> dict:
        """光伏发电数据统计

        Args:
            device_sn: 设备序列号（None 表示全部设备）
            start/end: 统计周期（日期格式以云平台文档为准，如 "2026-08-01"）

        Returns:
            发电统计 dict（发电量/功率/收益等，结构以云平台接口文档为准）

        TODO: 确认请求参数名与响应字段
        """
        params = {k: v for k, v in
                  [("device_sn", device_sn), ("start", start), ("end", end)]
                  if v is not None}
        resp = self.request("pv_data_stats", params=params)
        try:
            return resp.json()
        except ValueError as exc:
            raise CloudApiError(
                f"发电数据统计接口响应不是合法 JSON: {resp.text[:200]}") from exc

    # ---------------- 资源管理 ----------------

    def close(self) -> None:
        """关闭会话（释放连接）"""
        self.session.close()

    def __enter__(self) -> "IotClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.close()
        return False
