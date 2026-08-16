# PV/逆变器测试自动化平台

基于 pytest 的分层测试自动化框架，用于 AC 源（PRE2020S / IT6000C）、PV 源模拟器、功分仪与逆变器的自动化测试。

> ⚠️ 当前为**骨架版本**：目录结构、类接口签名与配置模板已就绪，具体业务逻辑均以 `TODO` 标记，需按设备手册逐步填充后接入真实设备。

## 目录结构

```
pv-test-platform/
├── Compara.py                          # 顶层数据比较与报告生成入口
├── conftest.py                         # pytest 全局夹具
├── run_tests.py                        # 测试运行入口
├── requirements.txt                    # Python 依赖
├── pytest.ini                          # pytest 配置
├── config/                             # 配置目录
│   ├── env_config.yml                  # 环境配置（设备IP/型号/端口等）
│   ├── global_config.yaml              # 全局配置（日志级别、报告路径等）
│   ├── config_manager.py               # 配置管理器（从Web平台拉取配置）
│   └── command_maps/                   # 命令映射表（驱动配置）
├── connection/                         # 物理连接层（ModbusTCP / SCPI / VISA / TCP）
├── driver/                             # 驱动层（协议翻译）
├── cl/                                 # 原子业务层（Common Layer）
├── pbl/                                # 复合业务层（Public Business Layer）
├── pml/                                # 数据记录层（Public Measure Layer）
├── testcase/                           # 测试用例目录
│   ├── case/                           # 测试用例脚本
│   ├── config/                         # 测试配置（用于平台展示）
│   └── data/raw/                       # 原始数据文件
├── doc/                                # 文档输出目录（报告 / 模板）
├── scripts/                            # 工具脚本（Jenkins同步 / 急停 / 设备检查）
├── utils/                              # 工具类（日志 / 计时 / 重试 / 异常）
└── logs/                               # 日志目录
```

## 分层设计

| 层 | 职责 | 说明 |
|---|---|---|
| `connection` | 物理连接 | 抽象 SCPI / ModbusTCP / VISA / 自定义 TCP 四种连接方式 |
| `driver` | 协议翻译 | 每种设备一个驱动，命令由 `config/command_maps/*.json` 映射表驱动，协议变动只改配置 |
| `cl` | 原子操作 | 单步设备操作（设电压、开输出、读测量值），持有驱动实例插槽 |
| `pbl` | 复合业务 | 测试序列编排（缓启动、电源循环、IV 扫描、MPPT、效率测试） |
| `pml` | 数据记录 | 实时记录 → 统计分析 → 导出 Excel/CSV |
| `testcase` | 测试用例 | pytest 用例脚本，通过夹具自动装配 PBL/CL 实例 |
| `Compara.py` | 结果比对 | 实测数据 vs 期望数据，生成 HTML 报告 |

## 安装

```bash
pip install -r requirements.txt
```

## 环境变量

复制 `.env.example` 为 `.env` 并按实际环境修改（`.env` 不提交到 Git）：

```
WEB_API_URL=http://test-platform.example.com/api/v1   # Web 测试平台 API（配置拉取）
API_TOKEN=your-api-token-here
TEST_ENV=Production_Line_3                             # 对应 env_config.yml 中的环境名
```

## 运行

```bash
# 运行全部用例
python run_tests.py

# 运行单个用例文件
python run_tests.py --case testcase/case/test_ac_soft_start.py

# 生成 HTML 报告
python run_tests.py --report

# 强制使用模拟设备（无真实硬件时）
python run_tests.py --mock

# 直接使用 pytest（标记说明见 pytest.ini）
pytest testcase/case/test_ac_soft_start.py -m ac
```

## 常用脚本

```bash
python scripts/device_checker.py     # 设备连通性检查
python scripts/emergency_stop.py     # 紧急停止（所有设备下电）
python scripts/jenkins_sync_config.py # 从 Jenkins 同步配置
```
