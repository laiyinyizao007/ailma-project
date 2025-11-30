"""
端到端测试 - 完整工作流
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock

from src.ai.task_parser import TaskParser
from src.ai.classifiers.intent_classifier import IntentClassifier
from src.ai.extractors.entity_extractor import EntityExtractor
from src.executors.calendar_executor import CalendarExecutor
from src.ai.models.intent import IntentType


@pytest.mark.asyncio
@pytest.mark.e2e
class TestCompleteWorkflow:
    """完整工作流测试"""

    async def test_create_calendar_event_workflow(self):
        """
        测试完整的日历事件创建流程:
        用户输入 -> 意图分类 -> 实体提取 -> 执行创建 -> 返回结果
        """
        # 1. Mock Claude 客户端
        mock_claude = Mock()

        # 意图分类响应
        mock_claude.complete_json = AsyncMock(
            side_effect=[
                # 第一次调用: 意图分类
                {
                    "intent": "calendar_create",
                    "confidence": 0.95,
                    "explanation": "用户想创建日历事件",
                },
                # 第二次调用: 实体提取
                {
                    "title": "团队会议",
                    "time": {
                        "start": (datetime.now() + timedelta(days=1)).replace(
                            hour=15, minute=0
                        ).isoformat(),
                        "is_all_day": False,
                    },
                    "location": {"name": "会议室A"},
                },
            ]
        )

        # 2. 构建组件
        from src.ai.prompts.templates import PromptManager
        from src.ai.parsers.time_parser import TimeParser

        prompt_manager = PromptManager()
        time_parser = TimeParser()

        intent_classifier = IntentClassifier(mock_claude, prompt_manager)
        entity_extractor = EntityExtractor(mock_claude, prompt_manager, time_parser)
        task_parser = TaskParser(intent_classifier, entity_extractor)

        # 3. Mock Calendar Adapter
        mock_calendar = Mock()
        mock_calendar.create_event = AsyncMock(
            return_value={
                "id": "event_abc123",
                "summary": "团队会议",
                "htmlLink": "https://calendar.google.com/event?eid=abc123",
            }
        )

        calendar_executor = CalendarExecutor(mock_calendar)

        # 4. 执行完整流程
        user_input = "明天下午3点在会议室A开团队会议"

        # Step 1: 解析
        parse_result = await task_parser.parse(user_input)

        # Step 2: 验证解析结果
        assert parse_result.is_valid()
        assert parse_result.intent.type == IntentType.CALENDAR_CREATE
        assert parse_result.entities.title == "团队会议"
        assert parse_result.entities.location.name == "会议室A"

        # Step 3: 执行
        execution_result = await calendar_executor.execute(parse_result.entities)

        # Step 4: 验证结果
        assert execution_result.is_success()
        assert "团队会议" in execution_result.message
        assert execution_result.data["id"] == "event_abc123"

    async def test_query_calendar_workflow(self):
        """测试查询日历流程"""
        # Mock 组件
        mock_claude = Mock()
        mock_claude.complete_json = AsyncMock(
            side_effect=[
                {
                    "intent": "calendar_query",
                    "confidence": 0.92,
                    "explanation": "用户想查询日程",
                },
                {
                    "description": "查询明天的安排",
                    "time": {
                        "start": (datetime.now() + timedelta(days=1)).isoformat()
                    },
                },
            ]
        )

        mock_claude.complete = AsyncMock(
            return_value="您明天有3个安排：早上9点站会，下午2点产品评审，晚上6点团队聚餐。"
        )

        # 构建 Task Parser
        from src.ai.prompts.templates import PromptManager
        from src.ai.parsers.time_parser import TimeParser

        prompt_manager = PromptManager()
        time_parser = TimeParser()
        intent_classifier = IntentClassifier(mock_claude, prompt_manager)
        entity_extractor = EntityExtractor(mock_claude, prompt_manager, time_parser)
        task_parser = TaskParser(intent_classifier, entity_extractor)

        # Mock Calendar
        mock_calendar = Mock()
        mock_calendar.list_events = AsyncMock(
            return_value=[
                {"summary": "站会", "start": {"dateTime": "2025-11-28T09:00:00"}},
                {"summary": "产品评审", "start": {"dateTime": "2025-11-28T14:00:00"}},
                {"summary": "团队聚餐", "start": {"dateTime": "2025-11-28T18:00:00"}},
            ]
        )

        # 执行查询
        from src.executors.query_executor import QueryExecutor

        query_executor = QueryExecutor(mock_calendar, mock_claude)

        user_input = "我明天有什么安排"

        parse_result = await task_parser.parse(user_input)
        assert parse_result.intent.type == IntentType.CALENDAR_QUERY

        execution_result = await query_executor.execute(parse_result.entities)

        assert execution_result.is_success()
        assert execution_result.data["count"] == 3

    async def test_create_notion_page_workflow(self):
        """测试创建 Notion 页面流程"""
        mock_claude = Mock()
        mock_claude.complete_json = AsyncMock(
            side_effect=[
                {
                    "intent": "notion_create_page",
                    "confidence": 0.88,
                    "explanation": "用户想创建笔记",
                },
                {
                    "title": "今日思考",
                    "description": "记录今天的想法和思考",
                    "tags": ["日记", "思考"],
                },
            ]
        )

        from src.ai.prompts.templates import PromptManager
        from src.ai.parsers.time_parser import TimeParser

        prompt_manager = PromptManager()
        time_parser = TimeParser()
        intent_classifier = IntentClassifier(mock_claude, prompt_manager)
        entity_extractor = EntityExtractor(mock_claude, prompt_manager, time_parser)
        task_parser = TaskParser(intent_classifier, entity_extractor)

        # Mock Notion
        mock_notion = Mock()
        mock_notion.create_page = AsyncMock(
            return_value={"id": "page123", "url": "https://notion.so/page123"}
        )

        from src.executors.notion_executor import NotionExecutor

        notion_executor = NotionExecutor(mock_notion)

        user_input = "记录今天的想法和思考"

        parse_result = await task_parser.parse(user_input)
        assert parse_result.intent.type == IntentType.NOTION_CREATE_PAGE

        execution_result = await notion_executor.execute(
            parse_result.entities, "notion_create_page"
        )

        assert execution_result.is_success()
        assert "今日思考" in execution_result.message
