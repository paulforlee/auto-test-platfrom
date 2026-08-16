"""pytest 全局夹具

提供：
- 项目根路径（保证顶层模块可直接 import）
- 环境名（--env 参数 > .env 的 TEST_ENV > "default"）
- 全局 logger
- 配置管理器 ConfigManager 实例

新增全局选项：
    --env <name>   指定环境名，对应 config/env_config.yml 中的 environments 键
"""
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils import logger as log_utils  # noqa: E402
from config.config_manager import ConfigManager  # noqa: E402


def pytest_addoption(parser: pytest.Parser) -> None:
    """注册全局命令行选项"""
    parser.addoption("--env", default=None,
                     help="环境名（对应 config/env_config.yml 中的 environments 键）")


@pytest.fixture(scope="session")
def project_root() -> Path:
    """项目根目录路径"""
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def env_name(request: pytest.FixtureRequest) -> str:
    """当前测试环境名

    优先级：--env 命令行参数 > .env 的 TEST_ENV > "default"
    """
    cli_env = request.config.getoption("--env")
    if cli_env:
        return cli_env

    try:
        from dotenv import load_dotenv
        load_dotenv(PROJECT_ROOT / ".env")
        import os
        return os.getenv("TEST_ENV", "default")
    except ImportError:
        return "default"


@pytest.fixture(scope="session")
def config_manager(project_root: Path, env_name: str) -> ConfigManager:
    """全局配置管理器（Web 平台配置拉取失败时回退本地文件）"""
    return ConfigManager(env=env_name, config_dir=project_root / "config")


@pytest.fixture(scope="session")
def logger(project_root: Path) -> object:
    """全局 logger（同时输出到控制台与 logs/test.log）"""
    log_dir = project_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_utils.setup_logging(log_dir=log_dir)
