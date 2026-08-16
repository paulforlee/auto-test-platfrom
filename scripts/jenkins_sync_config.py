"""Jenkins 配置同步脚本

从 Jenkins Job 拉取设备配置/测试参数并同步到本地 config/ 与 testcase/config/。

用法：
    python scripts/jenkins_sync_config.py --job <job名> [--env Production_Line_3]

TODO:
1. Jenkins API 认证（token 放 .env）
2. 拉取 Job 构建参数/制品（如 env_config.yml、test_params.yaml）
3. 校验格式后覆盖本地配置文件，记录日志到 logs/config_sync.log
"""
import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def sync_from_jenkins(job_name: str, env: str) -> dict:
    """从 Jenkins 同步配置

    Args:
        job_name: Jenkins Job 名
        env: 目标环境名

    Returns:
        同步结果 {files: [已更新文件...], skipped: [...], errors: [...]}
    """
    # TODO:
    #   JENKINS_URL / JENKINS_TOKEN 从 .env 读取
    #   GET {JENKINS_URL}/job/{job}/lastSuccessfulBuild/artifact/...
    #   下载 env_config.yml / test_params.yaml 等配置制品
    #   校验 YAML 格式后写入本地，失败回滚
    raise NotImplementedError("TODO: 实现 Jenkins 配置同步")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Jenkins 配置同步")
    parser.add_argument("--job", required=True, help="Jenkins Job 名")
    parser.add_argument("--env", default="default", help="目标环境名")
    args = parser.parse_args(argv)

    result = sync_from_jenkins(args.job, args.env)
    print(f"同步完成: 更新 {len(result.get('files', []))} 个文件, "
          f"错误 {len(result.get('errors', []))} 个")
    return 1 if result.get("errors") else 0


if __name__ == "__main__":
    raise SystemExit(main())
