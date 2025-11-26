# AILMA 开发指南

**版本**: v1.0
**最后更新**: 2025-11-27

---

## 📋 目录

1. [环境准备](#环境准备)
2. [项目设置](#项目设置)
3. [开发流程](#开发流程)
4. [代码规范](#代码规范)
5. [测试指南](#测试指南)
6. [调试技巧](#调试技巧)
7. [常见问题](#常见问题)

---

## 🔧 环境准备

### 系统要求

| 组件 | 最低版本 | 推荐版本 | 说明 |
|------|---------|---------|------|
| **操作系统** | Linux/macOS/Windows | Ubuntu 22.04+ / macOS 13+ | WSL2 适用于 Windows |
| **Python** | 3.10 | 3.11+ | 支持最新特性 |
| **PostgreSQL** | 13 | 15+ | 主数据库 |
| **Redis** | 6 | 7+ | 缓存和任务队列 |
| **Docker** | 20.0 | 24.0+ | 容器化 |
| **Docker Compose** | 2.0 | 2.20+ | 服务编排 |
| **Git** | 2.30 | 2.40+ | 版本控制 |

### 开发工具推荐

| 类型 | 工具 | 说明 |
|------|------|------|
| **IDE** | VSCode / PyCharm | 推荐 VSCode + Python 扩展 |
| **终端** | iTerm2 / Windows Terminal | 增强终端体验 |
| **API 测试** | Postman / HTTPie | 测试 API 端点 |
| **数据库客户端** | DBeaver / pgAdmin | PostgreSQL 管理 |
| **Redis 客户端** | RedisInsight / redis-cli | Redis 管理 |

---

## 🚀 项目设置

### 1. 克隆项目

```bash
# 克隆仓库
git clone https://github.com/your-org/ailma-project.git
cd ailma-project

# 查看分支
git branch -a

# 切换到开发分支（如果有）
git checkout develop
```

---

### 2. 创建虚拟环境

```bash
# 方式 1: 使用 venv (推荐)
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 方式 2: 使用 conda
conda create -n ailma python=3.11
conda activate ailma

# 方式 3: 使用 poetry (高级)
poetry install
poetry shell
```

---

### 3. 安装依赖

```bash
# 升级 pip
pip install --upgrade pip

# 安装开发依赖（包含测试和代码质量工具）
pip install -r requirements-dev.txt

# 如果只需运行依赖
pip install -r requirements.txt
```

**requirements-dev.txt** 包含:
```
# 生产依赖
-r requirements.txt

# 测试框架
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0

# 代码质量
black==23.11.0
isort==5.12.0
flake8==6.1.0
pylint==3.0.3
mypy==1.7.1

# 开发工具
ipython==8.18.1
pre-commit==3.5.0
```

---

### 4. 配置环境变量

```bash
# 复制模板
cp .env.example .env

# 编辑配置文件
nano .env  # 或使用您喜欢的编辑器
```

**必需配置项**:
```bash
# Notion MCP
NOTION_API_KEY=secret_your_token_here
COMMAND_CENTER_DB_ID=your_db_id
CALENDAR_DB_ID=your_db_id
REPORTS_DB_ID=your_db_id

# LLM API
ANTHROPIC_API_KEY=sk-ant-your_key_here

# 数据库（开发环境使用 Docker）
DATABASE_URL=postgresql://ailma:password@localhost:5432/ailma
REDIS_URL=redis://localhost:6379/0

# 安全
SECRET_KEY=your-dev-secret-key
ENCRYPTION_KEY=your-dev-encryption-key

# 开发模式
DEBUG=True
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

---

### 5. 启动基础服务

#### 使用 Docker Compose (推荐)

```bash
# 启动 PostgreSQL 和 Redis
docker-compose up -d db redis

# 查看日志
docker-compose logs -f db redis

# 检查服务状态
docker-compose ps
```

#### 手动安装（可选）

**PostgreSQL**:
```bash
# Ubuntu/Debian
sudo apt install postgresql-15

# macOS
brew install postgresql@15

# 创建数据库
createdb ailma
```

**Redis**:
```bash
# Ubuntu/Debian
sudo apt install redis-server

# macOS
brew install redis

# 启动 Redis
redis-server
```

---

### 6. 数据库初始化

```bash
# 运行数据库迁移
alembic upgrade head

# 创建测试数据（可选）
python scripts/seed_data.py

# 验证连接
python -c "from backend.database import engine; print('Database connected:', engine.url)"
```

---

### 7. 验证安装

```bash
# 运行所有测试
pytest

# 快速健康检查
python -m backend.health_check

# 启动开发服务器
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看 API 文档。

---

## 💻 开发流程

### 日常开发循环

```
1. 拉取最新代码
   ↓
2. 创建功能分支
   ↓
3. 编写代码 + 测试
   ↓
4. 运行代码质量检查
   ↓
5. 提交代码
   ↓
6. 创建 Pull Request
```

---

### 1. 拉取最新代码

```bash
# 更新主分支
git checkout main
git pull origin main

# 更新开发分支
git checkout develop
git pull origin develop
```

---

### 2. 创建功能分支

```bash
# 命名规范: feature/功能描述 或 bugfix/问题描述
git checkout -b feature/add-calendar-sync

# 其他分支类型
# feature/  - 新功能
# bugfix/   - Bug 修复
# hotfix/   - 紧急修复
# refactor/ - 代码重构
# docs/     - 文档更新
```

---

### 3. 编写代码

#### 项目结构

```
backend/
├── api/                 # API 路由层
│   ├── __init__.py
│   ├── health.py       # 健康检查端点
│   └── webhooks.py     # Webhook 处理
│
├── core/               # 核心业务逻辑
│   ├── ai/            # AI 模块
│   │   ├── task_parser.py
│   │   ├── report_generator.py
│   │   └── llm_client.py
│   ├── executor.py    # 任务执行器
│   └── intent_types.py
│
├── adapters/          # 外部服务适配器
│   ├── base_adapter.py
│   ├── notion_mcp_client.py  # Notion MCP
│   └── google_calendar.py
│
├── listeners/         # 监听器
│   └── notion_mcp_listener.py
│
├── models/           # 数据模型 (SQLAlchemy)
│   ├── user.py
│   ├── task_log.py
│   └── sync_status.py
│
├── schemas/          # Pydantic 验证模型
│   ├── command.py
│   └── report.py
│
├── utils/           # 工具函数
│   ├── encryption.py
│   ├── date_parser.py
│   └── logger.py
│
├── tasks/          # Celery 异步任务
│   └── sync_calendar.py
│
├── database.py     # 数据库配置
├── config.py       # 应用配置
└── main.py         # FastAPI 入口
```

---

#### 示例：添加新的 API 端点

**1. 定义 Schema** (`backend/schemas/calendar.py`):
```python
from pydantic import BaseModel, Field
from datetime import datetime

class CalendarEventCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    start_time: datetime
    end_time: datetime
    description: str | None = None
    location: str | None = None

class CalendarEventResponse(BaseModel):
    id: str
    title: str
    start_time: datetime
    event_url: str

    class Config:
        from_attributes = True
```

**2. 创建路由** (`backend/api/calendar.py`):
```python
from fastapi import APIRouter, Depends, HTTPException
from backend.schemas.calendar import CalendarEventCreate, CalendarEventResponse
from backend.adapters.google_calendar import GoogleCalendarAdapter

router = APIRouter(prefix="/calendar", tags=["Calendar"])

@router.post("/events", response_model=CalendarEventResponse)
async def create_event(
    event: CalendarEventCreate,
    calendar: GoogleCalendarAdapter = Depends(get_calendar_adapter)
):
    """创建日历事件"""
    try:
        result = await calendar.create_event(
            title=event.title,
            start_time=event.start_time,
            end_time=event.end_time,
            description=event.description
        )
        return CalendarEventResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**3. 注册路由** (`backend/main.py`):
```python
from backend.api import calendar

app.include_router(calendar.router, prefix="/api/v1")
```

---

#### 示例：添加数据模型

**1. 创建模型** (`backend/models/calendar_event.py`):
```python
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from backend.database import Base
import uuid

class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    external_id = Column(String(255), unique=True)
    title = Column(String(255), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    description = Column(Text)
    source = Column(String(50))  # 'google', 'outlook', 'manual'
    created_at = Column(DateTime, default=datetime.utcnow)
```

**2. 创建迁移**:
```bash
# 生成迁移文件
alembic revision --autogenerate -m "Add calendar_events table"

# 查看迁移内容
cat alembic/versions/xxx_add_calendar_events_table.py

# 应用迁移
alembic upgrade head

# 回滚（如果需要）
alembic downgrade -1
```

---

### 4. 编写测试

#### 单元测试示例

**测试文件**: `tests/unit/test_task_parser.py`

```python
import pytest
from backend.core.ai.task_parser import TaskParser
from backend.core.ai.llm_client import LLMClient

@pytest.fixture
def task_parser():
    """创建 TaskParser 实例"""
    llm = LLMClient(api_key="test-key")
    return TaskParser(llm_client=llm)

@pytest.mark.asyncio
async def test_parse_calendar_create_intent(task_parser):
    """测试日历创建意图识别"""
    instruction = "帮我把明天下午3点的团队会议加到日历"

    result = await task_parser.parse(instruction)

    assert result["intent"] == "calendar_create"
    assert "event_title" in result["entities"]
    assert result["entities"]["event_title"] == "团队会议"
    assert result["confidence"] > 0.8

@pytest.mark.asyncio
async def test_parse_report_generation_intent(task_parser):
    """测试报告生成意图识别"""
    instruction = "生成本周工作总结报告"

    result = await task_parser.parse(instruction)

    assert result["intent"] == "generate_report"
    assert result["entities"]["report_type"] == "weekly"
```

#### 集成测试示例

**测试文件**: `tests/integration/test_api_endpoints.py`

```python
import pytest
from httpx import AsyncClient
from backend.main import app

@pytest.mark.asyncio
async def test_health_check():
    """测试健康检查端点"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_create_calendar_event():
    """测试创建日历事件"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "title": "测试会议",
            "start_time": "2025-12-01T14:00:00",
            "end_time": "2025-12-01T15:00:00"
        }

        response = await client.post("/api/v1/calendar/events", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "测试会议"
        assert "event_url" in data
```

---

### 5. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/unit/test_task_parser.py

# 运行特定测试函数
pytest tests/unit/test_task_parser.py::test_parse_calendar_create_intent

# 运行并查看覆盖率
pytest --cov=backend --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux

# 只运行失败的测试
pytest --lf

# 详细输出
pytest -v

# 显示打印输出
pytest -s
```

---

### 6. 代码质量检查

#### 格式化代码

```bash
# Black - 代码格式化
black backend/
black tests/

# isort - 导入排序
isort backend/
isort tests/

# 一次性格式化
black backend/ tests/ && isort backend/ tests/
```

#### 代码检查

```bash
# Flake8 - 代码风格检查
flake8 backend/

# Pylint - 静态分析
pylint backend/

# Mypy - 类型检查
mypy backend/
```

#### Pre-commit Hooks（推荐）

```bash
# 安装 pre-commit
pip install pre-commit

# 设置 hooks
pre-commit install

# 手动运行所有 hooks
pre-commit run --all-files
```

**配置文件**: `.pre-commit-config.yaml`
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
```

---

### 7. 提交代码

```bash
# 查看修改
git status
git diff

# 添加文件
git add backend/api/calendar.py
git add tests/unit/test_calendar.py

# 或添加所有修改
git add .

# 提交（遵循提交规范）
git commit -m "feat: add calendar event creation API

- Implement POST /api/v1/calendar/events endpoint
- Add CalendarEventCreate schema
- Add unit tests for calendar API
- Update API documentation

Refs: #123"
```

#### Git 提交规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type**:
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例**:
```
feat(api): add calendar event creation endpoint

Implement POST /api/v1/calendar/events to create calendar events
through Google Calendar API integration.

- Add CalendarEventCreate schema
- Add GoogleCalendarAdapter integration
- Add comprehensive unit tests
- Update OpenAPI documentation

Closes #123
```

---

### 8. 推送和创建 PR

```bash
# 推送到远程
git push origin feature/add-calendar-sync

# 如果是第一次推送
git push -u origin feature/add-calendar-sync
```

**在 GitHub 创建 Pull Request**:
1. 访问仓库页面
2. 点击 "Compare & pull request"
3. 填写 PR 描述（使用模板）
4. 请求代码审查
5. 确保 CI 通过

---

## 📖 代码规范

### Python 风格指南

遵循 **PEP 8** 和 **Google Python Style Guide**

#### 命名规范

```python
# 模块名: 小写+下划线
notion_mcp_client.py

# 类名: PascalCase
class NotionMCPClient:
    pass

# 函数/方法: snake_case
def parse_user_instruction():
    pass

# 常量: 大写+下划线
MAX_RETRY_ATTEMPTS = 3

# 私有属性/方法: 前缀下划线
def _internal_method():
    pass
```

#### 类型注解

```python
from typing import Dict, List, Optional

def create_event(
    title: str,
    start_time: datetime,
    duration_minutes: int = 60
) -> Dict[str, Any]:
    """创建日历事件

    Args:
        title: 事件标题
        start_time: 开始时间
        duration_minutes: 持续时间（分钟）

    Returns:
        包含事件信息的字典

    Raises:
        ValueError: 如果参数无效
    """
    pass
```

#### 文档字符串

使用 **Google Style** docstrings:

```python
def complex_function(param1: int, param2: str) -> bool:
    """这是一行简短描述

    这里是详细描述，可以跨多行。
    解释函数的目的和行为。

    Args:
        param1: 第一个参数的说明
        param2: 第二个参数的说明

    Returns:
        返回值的说明

    Raises:
        ValueError: 什么情况下抛出此异常
        TypeError: 什么情况下抛出此异常

    Example:
        >>> result = complex_function(42, "test")
        >>> print(result)
        True
    """
    pass
```

---

### 错误处理

```python
# ✅ 好的做法
try:
    result = await external_api.call()
except APIError as e:
    logger.error(f"API call failed: {e}", exc_info=True)
    raise HTTPException(status_code=502, detail="External service unavailable")
except Exception as e:
    logger.exception("Unexpected error")
    raise

# ❌ 避免
try:
    result = external_api.call()
except:  # 不要捕获所有异常
    pass  # 不要静默失败
```

---

### 日志记录

```python
import logging

logger = logging.getLogger(__name__)

# 使用不同级别
logger.debug("Detailed debug information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred", exc_info=True)

# 结构化日志
logger.info(
    "Event created",
    extra={
        "event_id": event.id,
        "user_id": user.id,
        "source": "google_calendar"
    }
)
```

---

## 🐛 调试技巧

### 1. 使用 Python Debugger (pdb)

```python
import pdb

def problematic_function():
    x = calculate_something()
    pdb.set_trace()  # 断点
    return process(x)
```

**常用命令**:
- `n` (next) - 下一行
- `s` (step) - 进入函数
- `c` (continue) - 继续执行
- `p variable` - 打印变量
- `l` (list) - 显示代码
- `q` (quit) - 退出

---

### 2. IPython 调试

```bash
# 安装 IPython
pip install ipython

# 运行脚本并在异常时自动进入调试器
ipython --pdb your_script.py
```

---

### 3. VSCode 调试配置

**`.vscode/launch.json`**:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "backend.main:app",
                "--reload",
                "--host", "0.0.0.0",
                "--port", "8000"
            ],
            "jinja": true,
            "justMyCode": false
        },
        {
            "name": "Python: Pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "-v",
                "-s"
            ],
            "console": "integratedTerminal"
        }
    ]
}
```

---

### 4. 日志调试

```python
# 临时提高日志级别
import logging
logging.getLogger("backend").setLevel(logging.DEBUG)

# 查看特定模块日志
logging.getLogger("backend.adapters.notion_mcp_client").setLevel(logging.DEBUG)
```

---

### 5. 数据库调试

```bash
# 连接到数据库
psql -U ailma -d ailma

# 查看所有表
\dt

# 查看表结构
\d task_logs

# 查询数据
SELECT * FROM task_logs ORDER BY created_at DESC LIMIT 10;

# 查看慢查询
SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;
```

---

## ❓ 常见问题

### Q1: 虚拟环境激活后 Python 版本不对

```bash
# 检查 Python 版本
python --version

# 如果不对，删除重建
rm -rf venv/
python3.11 -m venv venv
source venv/bin/activate
```

---

### Q2: 数据库连接失败

```bash
# 检查 PostgreSQL 是否运行
docker-compose ps db

# 查看日志
docker-compose logs db

# 重启数据库
docker-compose restart db

# 测试连接
psql -h localhost -U ailma -d ailma
```

---

### Q3: 依赖冲突

```bash
# 清理环境
pip uninstall -y -r requirements.txt
pip cache purge

# 重新安装
pip install -r requirements.txt
```

---

### Q4: 测试失败

```bash
# 清理测试缓存
pytest --cache-clear

# 重新运行失败的测试
pytest --lf -v

# 查看详细输出
pytest -vv -s
```

---

### Q5: pre-commit hooks 失败

```bash
# 跳过 hooks（不推荐）
git commit --no-verify -m "message"

# 手动修复后重新提交
black backend/
isort backend/
git add .
git commit -m "message"
```

---

## 📚 相关资源

### 官方文档
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- [Pydantic 文档](https://docs.pydantic.dev/)
- [Pytest 文档](https://docs.pytest.org/)

### 项目文档
- [PRD - 产品需求](./PRD.md)
- [MCP 架构设计](./ARCHITECTURE-MCP.md)
- [API 文档](./API.md)
- [部署指南](./DEPLOYMENT.md)

---

**Happy Coding!** 🚀
