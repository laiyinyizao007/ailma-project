# AILMA 项目结构设计

**版本**: v1.0
**创建日期**: 2025-11-27
**对应 PRD**: [PRD.md](./PRD.md)

---

## 📁 完整目录结构

```
ailma-project/
│
├── backend/                          # 后端服务
│   ├── api/                          # FastAPI 路由和端点
│   │   ├── __init__.py
│   │   ├── health.py                 # 健康检查端点
│   │   ├── webhooks.py               # Notion Webhook 接收
│   │   └── admin.py                  # 管理端点（可选）
│   │
│   ├── core/                         # 核心业务逻辑
│   │   ├── __init__.py
│   │   │
│   │   ├── ai/                       # AI 核心模块
│   │   │   ├── __init__.py
│   │   │   ├── task_parser.py        # 任务解析器（NLP 意图识别）
│   │   │   ├── report_generator.py   # 报告生成器
│   │   │   ├── llm_client.py         # LLM API 客户端封装
│   │   │   └── prompts.py            # Prompt 模板管理
│   │   │
│   │   ├── executor.py               # 任务执行器（调度 Adapters）
│   │   ├── intent_types.py           # 意图类型定义
│   │   └── entity_extractor.py       # 实体提取工具
│   │
│   ├── adapters/                     # 外部服务集成适配器
│   │   ├── __init__.py
│   │   ├── base_adapter.py           # 适配器基类
│   │   ├── notion_adapter.py         # Notion API 封装
│   │   ├── calendar_adapter.py       # 日历适配器基类
│   │   ├── google_calendar.py        # Google Calendar 实现
│   │   └── outlook_calendar.py       # Outlook Calendar 实现（Phase 2）
│   │
│   ├── listeners/                    # 监听器模块
│   │   ├── __init__.py
│   │   ├── notion_listener.py        # Notion 数据库轮询器
│   │   └── webhook_handler.py        # Webhook 处理逻辑
│   │
│   ├── models/                       # 数据模型（SQLAlchemy）
│   │   ├── __init__.py
│   │   ├── user.py                   # 用户模型
│   │   ├── user_settings.py          # 用户配置模型
│   │   ├── calendar_connection.py    # 日历连接模型
│   │   ├── task_log.py               # 任务日志模型
│   │   └── sync_status.py            # 同步状态模型
│   │
│   ├── schemas/                      # Pydantic 数据验证模型
│   │   ├── __init__.py
│   │   ├── command.py                # 指令相关 Schema
│   │   ├── calendar.py               # 日历事件 Schema
│   │   └── report.py                 # 报告 Schema
│   │
│   ├── utils/                        # 工具函数
│   │   ├── __init__.py
│   │   ├── encryption.py             # 加密/解密工具
│   │   ├── date_parser.py            # 日期解析工具
│   │   ├── logger.py                 # 日志配置
│   │   └── retry.py                  # 重试装饰器
│   │
│   ├── tasks/                        # Celery 异步任务
│   │   ├── __init__.py
│   │   ├── sync_calendar.py          # 日历同步任务
│   │   └── generate_report.py        # 报告生成任务
│   │
│   ├── database.py                   # 数据库连接配置
│   ├── config.py                     # 配置管理（环境变量）
│   ├── dependencies.py               # FastAPI 依赖注入
│   └── main.py                       # FastAPI 应用入口
│
├── tests/                            # 测试文件
│   ├── __init__.py
│   ├── conftest.py                   # pytest 配置和 fixtures
│   │
│   ├── unit/                         # 单元测试
│   │   ├── test_task_parser.py
│   │   ├── test_notion_adapter.py
│   │   ├── test_calendar_adapter.py
│   │   └── test_report_generator.py
│   │
│   ├── integration/                  # 集成测试
│   │   ├── test_full_workflow.py
│   │   └── test_api_endpoints.py
│   │
│   └── fixtures/                     # 测试数据
│       ├── sample_commands.json
│       └── mock_responses.json
│
├── scripts/                          # 工具脚本
│   ├── setup_notion.py               # Notion 数据库初始化脚本
│   ├── migrate_db.py                 # 数据库迁移脚本
│   └── seed_data.py                  # 测试数据生成
│
├── alembic/                          # 数据库迁移（Alembic）
│   ├── versions/                     # 迁移版本文件
│   ├── env.py
│   └── script.py.mako
│
├── docs/                             # 文档目录
│   ├── PRD.md                        # 产品需求文档（本文档）
│   ├── PROJECT-STRUCTURE.md          # 项目结构说明（本文件）
│   ├── API.md                        # API 文档
│   ├── DEPLOYMENT.md                 # 部署指南
│   ├── DEVELOPMENT.md                # 开发指南
│   └── TROUBLESHOOTING.md            # 故障排查手册
│
├── notion_templates/                 # Notion 模板文件
│   ├── command_center_template.json  # 指令中心数据库模板
│   ├── calendar_db_template.json     # 日历数据库模板
│   └── reports_db_template.json      # 报告数据库模板
│
├── .github/                          # GitHub 配置（可选）
│   └── workflows/
│       ├── ci.yml                    # CI/CD 工作流
│       └── deploy.yml                # 自动部署工作流
│
├── docker/                           # Docker 相关文件
│   ├── Dockerfile                    # 应用 Dockerfile
│   ├── Dockerfile.dev                # 开发环境 Dockerfile
│   └── nginx.conf                    # Nginx 配置（生产环境）
│
├── .env.example                      # 环境变量模板
├── .gitignore                        # Git 忽略文件
├── docker-compose.yml                # Docker Compose 配置
├── docker-compose.dev.yml            # 开发环境 Compose
├── requirements.txt                  # Python 依赖（生产环境）
├── requirements-dev.txt              # 开发依赖
├── pyproject.toml                    # 项目元数据和工具配置
├── pytest.ini                        # pytest 配置
├── alembic.ini                       # Alembic 配置
├── README.md                         # 项目说明
└── CHANGELOG.md                      # 变更日志
```

---

## 📦 核心模块说明

### 1. API 层 (`backend/api/`)

#### `health.py`
健康检查端点，用于监控和负载均衡。

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "ailma-backend",
        "version": "1.0.0"
    }
```

#### `webhooks.py`
接收 Notion 的 Webhook 通知（可选，替代轮询）。

```python
from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.post("/webhooks/notion")
async def handle_notion_webhook(request: Request):
    """处理 Notion Webhook"""
    # 验证签名
    # 解析事件
    # 触发任务处理
    pass
```

---

### 2. AI 核心层 (`backend/core/ai/`)

#### `task_parser.py`
**职责**: 解析自然语言指令，识别意图和实体。

```python
from typing import Dict, Any
from .llm_client import LLMClient
from .prompts import INTENT_CLASSIFICATION_PROMPT

class TaskParser:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    async def parse(self, instruction: str) -> Dict[str, Any]:
        """
        解析用户指令

        Args:
            instruction: 用户输入的自然语言指令

        Returns:
            {
                "intent": "calendar_create",
                "entities": {
                    "event_title": "团队会议",
                    "start_time": "2025-11-28T15:00:00",
                    "duration_minutes": 60
                },
                "confidence": 0.95
            }
        """
        prompt = INTENT_CLASSIFICATION_PROMPT.format(
            instruction=instruction
        )

        response = await self.llm.complete(prompt)
        return self._parse_llm_response(response)
```

#### `report_generator.py`
**职责**: 生成结构化报告。

```python
class ReportGenerator:
    async def generate_weekly_report(
        self,
        calendar_events: List[Dict],
        notion_tasks: List[Dict]
    ) -> str:
        """生成周报（Markdown 格式）"""
        # 数据聚合
        stats = self._calculate_stats(calendar_events, notion_tasks)

        # 调用 LLM 生成摘要
        summary = await self.llm.generate_summary(calendar_events)

        # 格式化为 Markdown
        report = self._format_report(stats, summary)
        return report
```

#### `llm_client.py`
**职责**: 封装 LLM API 调用（Claude/GPT）。

```python
import anthropic
from typing import Optional

class LLMClient:
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    async def complete(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7
    ) -> str:
        """调用 Claude API"""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
```

---

### 3. 适配器层 (`backend/adapters/`)

#### `base_adapter.py`
**职责**: 定义适配器接口（抽象基类）。

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseAdapter(ABC):
    @abstractmethod
    async def connect(self) -> bool:
        """建立连接"""
        pass

    @abstractmethod
    async def test_connection(self) -> bool:
        """测试连接"""
        pass
```

#### `notion_adapter.py`
**职责**: 封装 Notion API 操作。

```python
from notion_client import AsyncClient

class NotionAdapter:
    def __init__(self, token: str):
        self.client = AsyncClient(auth=token)

    async def create_page(
        self,
        parent_id: str,
        title: str,
        content: str
    ) -> Dict:
        """创建 Notion 页面"""
        # 转换 Markdown 到 Notion Blocks
        blocks = self._markdown_to_blocks(content)

        response = await self.client.pages.create(
            parent={"database_id": parent_id},
            properties={
                "Name": {"title": [{"text": {"content": title}}]}
            },
            children=blocks
        )
        return response

    async def query_database(
        self,
        database_id: str,
        filter: Dict = None
    ) -> List[Dict]:
        """查询 Notion 数据库"""
        response = await self.client.databases.query(
            database_id=database_id,
            filter=filter
        )
        return response["results"]

    async def update_page(
        self,
        page_id: str,
        properties: Dict
    ) -> Dict:
        """更新页面属性"""
        return await self.client.pages.update(
            page_id=page_id,
            properties=properties
        )
```

#### `google_calendar.py`
**职责**: Google Calendar API 集成。

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class GoogleCalendarAdapter:
    def __init__(self, credentials: Credentials):
        self.service = build('calendar', 'v3', credentials=credentials)

    async def create_event(
        self,
        calendar_id: str,
        event_data: Dict
    ) -> Dict:
        """创建日历事件"""
        event = {
            'summary': event_data['title'],
            'start': {
                'dateTime': event_data['start_time'],
                'timeZone': 'Asia/Shanghai',
            },
            'end': {
                'dateTime': event_data['end_time'],
                'timeZone': 'Asia/Shanghai',
            },
        }

        result = self.service.events().insert(
            calendarId=calendar_id,
            body=event
        ).execute()

        return result

    async def get_events(
        self,
        calendar_id: str,
        time_min: str,
        time_max: str
    ) -> List[Dict]:
        """获取事件列表"""
        events_result = self.service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        return events_result.get('items', [])
```

---

### 4. 监听器层 (`backend/listeners/`)

#### `notion_listener.py`
**职责**: 轮询 Notion 指令中心，检测新指令。

```python
import asyncio
from backend.adapters.notion_adapter import NotionAdapter
from backend.core.executor import TaskExecutor

class NotionListener:
    def __init__(
        self,
        notion_adapter: NotionAdapter,
        task_executor: TaskExecutor,
        poll_interval: int = 30  # 秒
    ):
        self.notion = notion_adapter
        self.executor = task_executor
        self.poll_interval = poll_interval

    async def start(self):
        """启动监听器"""
        while True:
            try:
                await self._poll_commands()
            except Exception as e:
                logger.error(f"Listener error: {e}")

            await asyncio.sleep(self.poll_interval)

    async def _poll_commands(self):
        """检查待处理指令"""
        # 查询状态为 Pending 的指令
        commands = await self.notion.query_database(
            database_id=COMMAND_CENTER_DB_ID,
            filter={
                "property": "状态",
                "select": {"equals": "⏳ Pending"}
            }
        )

        for cmd in commands:
            # 更新为 Processing
            await self.notion.update_page(
                cmd['id'],
                {"状态": {"select": {"name": "🔄 Processing"}}}
            )

            # 执行任务
            result = await self.executor.execute(cmd)

            # 回写结果
            await self._write_result(cmd['id'], result)
```

---

### 5. 数据模型层 (`backend/models/`)

#### `user.py`
```python
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from backend.database import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(100))
    password_hash = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### `task_log.py`
```python
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB

class TaskLog(Base):
    __tablename__ = "task_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    command_text = Column(Text, nullable=False)
    intent = Column(String(100))
    entities = Column(JSONB)
    status = Column(String(50))  # pending, processing, completed, failed
    result_text = Column(Text)
    error_message = Column(Text)
    processing_time_ms = Column(Integer)
    notion_page_id = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
```

---

### 6. 配置管理 (`backend/config.py`)

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "AILMA Backend"
    DEBUG: bool = False

    # 数据库
    DATABASE_URL: str

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Notion
    NOTION_DEFAULT_TOKEN: Optional[str] = None

    # LLM
    ANTHROPIC_API_KEY: str
    LLM_MODEL: str = "claude-3-sonnet-20240229"

    # Google Calendar
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    # 安全
    SECRET_KEY: str
    ENCRYPTION_KEY: str  # AES 加密密钥

    # 性能
    POLL_INTERVAL_SECONDS: int = 30
    MAX_WORKERS: int = 4

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

---

### 7. 主应用入口 (`backend/main.py`)

```python
from fastapi import FastAPI
from backend.api import health, webhooks
from backend.listeners.notion_listener import NotionListener
from backend.config import settings
import asyncio

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 注册路由
app.include_router(health.router, tags=["Health"])
app.include_router(webhooks.router, prefix="/api/v1", tags=["Webhooks"])

# 启动时事件
@app.on_event("startup")
async def startup_event():
    # 启动 Notion Listener
    listener = NotionListener(
        notion_adapter=get_notion_adapter(),
        task_executor=get_task_executor(),
        poll_interval=settings.POLL_INTERVAL_SECONDS
    )

    asyncio.create_task(listener.start())

# 关闭时事件
@app.on_event("shutdown")
async def shutdown_event():
    # 清理资源
    pass
```

---

## 🔧 配置文件说明

### `docker-compose.yml`

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: docker/Dockerfile
    container_name: ailma-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://ailma:password@db:5432/ailma
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app/backend
    command: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:15-alpine
    container_name: ailma-postgres
    environment:
      POSTGRES_USER: ailma
      POSTGRES_PASSWORD: password
      POSTGRES_DB: ailma
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    container_name: ailma-redis
    ports:
      - "6379:6379"

  celery_worker:
    build:
      context: .
      dockerfile: docker/Dockerfile
    container_name: ailma-celery-worker
    command: celery -A backend.tasks.celery_app worker --loglevel=info
    depends_on:
      - redis
      - db
    environment:
      - DATABASE_URL=postgresql://ailma:password@db:5432/ailma
      - REDIS_URL=redis://redis:6379

  celery_beat:
    build:
      context: .
      dockerfile: docker/Dockerfile
    container_name: ailma-celery-beat
    command: celery -A backend.tasks.celery_app beat --loglevel=info
    depends_on:
      - redis
      - db
    environment:
      - REDIS_URL=redis://redis:6379

volumes:
  postgres_data:
```

---

### `.env.example`

```bash
# Application
APP_NAME=AILMA Backend
DEBUG=True

# Database
DATABASE_URL=postgresql://ailma:password@localhost:5432/ailma

# Redis
REDIS_URL=redis://localhost:6379

# Notion
NOTION_DEFAULT_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# LLM API
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LLM_MODEL=claude-3-sonnet-20240229

# Google Calendar
GOOGLE_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ENCRYPTION_KEY=your-32-byte-encryption-key-base64-encoded

# Performance
POLL_INTERVAL_SECONDS=30
MAX_WORKERS=4
```

---

### `requirements.txt`

```txt
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.23
asyncpg==0.29.0
alembic==1.12.1
psycopg2-binary==2.9.9

# AI/NLP
anthropic==0.7.7
langchain==0.1.0
spacy==3.7.2

# External APIs
notion-client==2.2.1
google-api-python-client==2.108.0
google-auth-httplib2==0.2.0
google-auth-oauthlib==1.1.0

# Task Queue
celery==5.3.4
redis==5.0.1

# HTTP Client
httpx==0.25.2
aiohttp==3.9.1

# Utilities
python-dateutil==2.8.2
pytz==2023.3
cryptography==41.0.7
pyjwt==2.8.0

# Logging
loguru==0.7.2

# Testing (dev only, see requirements-dev.txt)
```

---

### `requirements-dev.txt`

```txt
-r requirements.txt

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0

# Code Quality
black==23.11.0
isort==5.12.0
flake8==6.1.0
pylint==3.0.3
mypy==1.7.1

# Tools
ipython==8.18.1
pre-commit==3.5.0
```

---

## 🚀 快速开始

### 1. 克隆项目并安装依赖

```bash
# 克隆仓库（假设已创建）
git clone https://github.com/your-org/ailma-project.git
cd ailma-project

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements-dev.txt
```

### 2. 配置环境变量

```bash
# 复制模板
cp .env.example .env

# 编辑 .env 文件，填写真实的 API Keys
nano .env
```

### 3. 启动数据库和 Redis

```bash
# 使用 Docker Compose 启动依赖服务
docker-compose up -d db redis
```

### 4. 运行数据库迁移

```bash
# 初始化 Alembic
alembic upgrade head
```

### 5. 启动开发服务器

```bash
# 启动 FastAPI 应用
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 访问 API 文档
# http://localhost:8000/docs
```

### 6. 启动 Celery Worker（后台任务）

```bash
# 新开一个终端
celery -A backend.tasks.celery_app worker --loglevel=info

# 启动定时任务调度器
celery -A backend.tasks.celery_app beat --loglevel=info
```

---

## 📖 开发指南

### 添加新的意图类型

1. 在 `backend/core/intent_types.py` 添加意图定义
2. 在 `backend/core/ai/prompts.py` 更新 Prompt
3. 在 `backend/core/executor.py` 添加处理逻辑
4. 编写单元测试

### 添加新的外部服务集成

1. 在 `backend/adapters/` 创建新的 Adapter 类
2. 继承 `BaseAdapter` 并实现接口
3. 在 `backend/config.py` 添加配置项
4. 更新文档

### 运行测试

```bash
# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit/

# 生成覆盖率报告
pytest --cov=backend --cov-report=html
```

---

## 📚 相关文档

- [PRD - 产品需求文档](./PRD.md)
- [API 文档](./API.md)（待创建）
- [部署指南](./DEPLOYMENT.md)（待创建）
- [故障排查](./TROUBLESHOOTING.md)（待创建）

---

**文档版本**: v1.0
**最后更新**: 2025-11-27
