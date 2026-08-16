"""配置管理器：从 Web 平台拉取配置，失败时回退本地配置文件

配置优先级：
    1. Web 平台（WEB_API_URL + API_TOKEN，见 .env）
    2. 本地 config/env_config.yml / global_config.yaml

用法：
    cm = ConfigManager(env="Production_Line_3")
    dev_cfg = cm.get_device_config("ac_source")   # {model, connection: {...}}
    g_cfg = cm.get_global_config()                # {logging, paths, device, comparison}
"""
import json
import logging
from pathlib import Path

import yaml

from utils.exceptions import ConfigError

logger = logging.getLogger(__name__)


class ConfigManager:
    """配置管理器"""

    def __init__(self, env: str = "default",
                 config_dir: Path | None = None,
                 web_api_url: str | None = None,
                 api_token: str | None = None):
        """
        Args:
            env: 环境名，对应 env_config.yml 中 environments 的键
            config_dir: config 目录路径，默认 <项目根>/config
            web_api_url: Web 平台 API 地址，None 时从环境变量 WEB_API_URL 读取
            api_token: API Token，None 时从环境变量 API_TOKEN 读取
        """
        self.env = env
        self.config_dir = Path(config_dir) if config_dir else Path(__file__).resolve().parent
        self.web_api_url = web_api_url
        self.api_token = api_token

        self._env_config: dict = {}
        self._global_config: dict = {}
        self._remote_config: dict | None = None  # 远程拉取结果缓存

    # ---------------- 本地配置加载 ----------------

    def load_local_env(self, env: str | None = None) -> dict:
        """加载 env_config.yml 中指定环境的设备配置

        Returns:
            {设备键: {model, connection: {...}}}
        """
        env = env or self.env
        path = self.config_dir / "env_config.yml"
        if not path.exists():
            raise ConfigError(f"环境配置文件不存在: {path}")

        with open(path, encoding="utf-8") as f:
            all_envs = yaml.safe_load(f) or {}
        environments = all_envs.get("environments", {})
        if env not in environments:
            raise ConfigError(f"环境 '{env}' 不存在，可用环境: {list(environments)}")
        self._env_config = environments[env]
        return self._env_config

    def load_global(self) -> dict:
        """加载 global_config.yaml 全局配置"""
        path = self.config_dir / "global_config.yaml"
        if not path.exists():
            raise ConfigError(f"全局配置文件不存在: {path}")

        with open(path, encoding="utf-8") as f:
            self._global_config = yaml.safe_load(f) or {}
        return self._global_config

    # ---------------- Web 平台配置拉取 ----------------

    def fetch_remote(self, force: bool = False) -> dict:
        """从 Web 平台拉取配置并缓存

        TODO:
        1. GET {WEB_API_URL}/config?env={env}（或按平台实际接口调整）
        2. 请求头携带 Authorization: Bearer {API_TOKEN}
        3. 超时与失败处理：记录告警日志，返回 {}（由调用方回退本地配置）
        """
        # 示例骨架：
        # if not force and self._remote_config is not None:
        #     return self._remote_config
        # resp = requests.get(f"{self.web_api_url}/config", params={"env": self.env},
        #                     headers={"Authorization": f"Bearer {self.api_token}"},
        #                     timeout=10)
        # resp.raise_for_status()
        # self._remote_config = resp.json()
        # return self._remote_config
        raise NotImplementedError("TODO: 实现 Web 平台配置拉取（WEB_API_URL + API_TOKEN）")

    # ---------------- 对外接口 ----------------

    def get_device_config(self, device_key: str) -> dict:
        """获取指定设备的连接配置（远程优先，本地回退）

        Args:
            device_key: 设备键，如 ac_source / pv_simulator / power_meter / inverter

        Returns:
            {model, connection: {type, host, port, ...}}
        """
        remote = self._remote_config or {}
        if device_key in remote:
            return remote[device_key]

        env_cfg = self._env_config or self.load_local_env()
        if device_key not in env_cfg:
            raise ConfigError(f"设备 '{device_key}' 不存在于环境 '{self.env}'，"
                              f"可用设备: {list(env_cfg)}")
        return env_cfg[device_key]

    def get_global_config(self) -> dict:
        """获取全局配置"""
        return self._global_config or self.load_global()

    def get_command_map(self, model: str) -> dict:
        """加载指定型号的命令映射表（config/command_maps/<model>_cmds.json）

        Args:
            model: 设备型号（映射表文件名约定为 <model>_cmds.json）

        TODO: 确认与平台拉取配置的整合方式（远程映射优先？）
        """
        candidates = [
            self.config_dir / "command_maps" / f"{model}_cmds.json",
            self.config_dir / "command_maps" / f"{model.lower()}_cmds.json",
        ]
        for path in candidates:
            if path.exists():
                with open(path, encoding="utf-8") as f:
                    return json.load(f)
        raise ConfigError(f"命令映射表不存在，尝试路径: {candidates}")
