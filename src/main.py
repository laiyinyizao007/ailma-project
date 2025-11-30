"""
AILMA 主应用
"""

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.ai.clients.claude import ClaudeClient
from src.ai.prompts.templates import PromptManager
from src.ai.parsers.time_parser import TimeParser
from src.ai.classifiers.intent_classifier import IntentClassifier
from src.ai.extractors.entity_extractor import EntityExtractor
from src.ai.task_parser import TaskParser
from src.adapters.google_calendar.adapter import GoogleCalendarAdapter
from src.adapters.notion.adapter import NotionAdapter
from src.executors.calendar_executor import CalendarExecutor
from src.executors.notion_executor import NotionExecutor
from src.executors.query_executor import QueryExecutor
from src.executors.report_generator import ReportGenerator
from src.listeners.notion_listener import NotionListener

# 配置日志
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# 全局实例
listener: NotionListener = None
listener_task: asyncio.Task = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    global listener, listener_task

    logger.info("AILMA 启动中...")

    # 初始化组件
    claude_client = ClaudeClient()
    prompt_manager = PromptManager()
    time_parser = TimeParser()

    # AI 组件
    intent_classifier = IntentClassifier(claude_client, prompt_manager)
    entity_extractor = EntityExtractor(claude_client, prompt_manager, time_parser)
    task_parser = TaskParser(intent_classifier, entity_extractor)

    # Adapters
    calendar_adapter = GoogleCalendarAdapter()
    notion_adapter = NotionAdapter()

    await calendar_adapter.initialize()
    await notion_adapter.initialize()

    # Executors
    calendar_executor = CalendarExecutor(calendar_adapter)
    notion_executor = NotionExecutor(notion_adapter)
    query_executor = QueryExecutor(calendar_adapter, claude_client)
    report_generator = ReportGenerator(calendar_adapter, notion_adapter, claude_client)

    # Listener
    listener = NotionListener(
        notion_adapter=notion_adapter,
        task_parser=task_parser,
        calendar_executor=calendar_executor,
        notion_executor=notion_executor,
        query_executor=query_executor,
        report_generator=report_generator,
    )

    # 启动后台监听器
    listener_task = asyncio.create_task(listener.start())

    logger.info("AILMA 启动完成")

    yield  # 应用运行期间

    # 关闭
    logger.info("AILMA 关闭中...")
    await listener.stop()
    listener_task.cancel()
    await calendar_adapter.close()
    await notion_adapter.close()
    logger.info("AILMA 已关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title="AILMA API",
    description="AI Life Management Assistant",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """健康检查"""
    return {
        "service": "AILMA",
        "version": "0.1.0",
        "status": "running",
        "listener_active": listener.running if listener else False,
    }


@app.get("/health")
async def health_check():
    """详细健康检查"""
    return {
        "status": "healthy",
        "components": {
            "listener": listener.running if listener else False,
            "last_check": (
                listener.last_check_time.isoformat() if listener else None
            ),
        },
    }


@app.post("/api/parse")
async def parse_command(command: dict):
    """
    手动解析指令 API

    Body:
        {"text": "用户指令"}

    Returns:
        解析结果
    """
    from src.ai.clients.claude import ClaudeClient
    from src.ai.prompts.templates import PromptManager
    from src.ai.parsers.time_parser import TimeParser
    from src.ai.classifiers.intent_classifier import IntentClassifier
    from src.ai.extractors.entity_extractor import EntityExtractor
    from src.ai.task_parser import TaskParser

    # 临时创建组件
    claude_client = ClaudeClient()
    prompt_manager = PromptManager()
    time_parser = TimeParser()
    intent_classifier = IntentClassifier(claude_client, prompt_manager)
    entity_extractor = EntityExtractor(claude_client, prompt_manager, time_parser)
    task_parser = TaskParser(intent_classifier, entity_extractor)

    # 解析
    text = command.get("text", "")
    result = await task_parser.parse(text)

    return {
        "intent": {
            "type": result.intent.type.value,
            "confidence": result.intent.confidence,
            "explanation": result.intent.explanation,
        },
        "entities": {
            "title": result.entities.title,
            "description": result.entities.description,
            "time": (
                {
                    "start": result.entities.time.start.isoformat(),
                    "end": (
                        result.entities.time.end.isoformat()
                        if result.entities.time.end
                        else None
                    ),
                    "is_all_day": result.entities.time.is_all_day,
                }
                if result.entities.time
                else None
            ),
            "location": (
                {"name": result.entities.location.name}
                if result.entities.location
                else None
            ),
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
