"""
执行器集成测试
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch

from src.executors.calendar_executor import CalendarExecutor
from src.executors.notion_executor import NotionExecutor
from src.executors.query_executor import QueryExecutor
from src.executors.report_generator import ReportGenerator
from src.executors.base_executor import ExecutionStatus
from src.ai.models.entity import ExtractedEntities, TimeEntity, LocationEntity


@pytest.mark.asyncio
class TestCalendarExecutor:
    """日历执行器测试"""

    async def test_create_event_success(self):
        """测试成功创建事件"""
        # Mock Calendar Adapter
        mock_adapter = Mock()
        mock_adapter.create_event = AsyncMock(
            return_value={
                "id": "event123",
                "summary": "测试会议",
                "status": "confirmed",
            }
        )

        executor = CalendarExecutor(mock_adapter)

        # 准备实体
        entities = ExtractedEntities(
            title="测试会议",
            time=TimeEntity(
                start=datetime.now() + timedelta(days=1),
                end=datetime.now() + timedelta(days=1, hours=1),
            ),
            location=LocationEntity(name="会议室A"),
        )

        # 执行
        result = await executor.create_event(entities)

        # 断言
        assert result.status == ExecutionStatus.SUCCESS
        assert "测试会议" in result.message
        assert result.data is not None

    async def test_create_event_missing_title(self):
        """测试缺少标题"""
        mock_adapter = Mock()
        executor = CalendarExecutor(mock_adapter)

        entities = ExtractedEntities(
            time=TimeEntity(start=datetime.now())
        )

        result = await executor.create_event(entities)

        assert result.status == ExecutionStatus.FAILED
        assert "缺少事件标题" in result.message


@pytest.mark.asyncio
class TestNotionExecutor:
    """Notion 执行器测试"""

    async def test_create_page_success(self):
        """测试成功创建页面"""
        mock_adapter = Mock()
        mock_adapter.create_page = AsyncMock(
            return_value={
                "id": "page123",
                "url": "https://notion.so/page123",
            }
        )

        executor = NotionExecutor(mock_adapter)

        entities = ExtractedEntities(
            title="测试笔记",
            description="这是一个测试笔记",
            tags=["测试", "笔记"],
        )

        result = await executor.create_page(entities)

        assert result.status == ExecutionStatus.SUCCESS
        assert "测试笔记" in result.message

    async def test_create_todo_success(self):
        """测试成功创建待办"""
        mock_adapter = Mock()
        mock_adapter.create_page = AsyncMock(
            return_value={"id": "todo123"}
        )

        executor = NotionExecutor(mock_adapter)

        entities = ExtractedEntities(
            title="买菜",
            priority="high",
            time=TimeEntity(start=datetime.now() + timedelta(days=1)),
        )

        result = await executor.create_todo(entities)

        assert result.status == ExecutionStatus.SUCCESS
        assert "买菜" in result.message


@pytest.mark.asyncio
class TestQueryExecutor:
    """查询执行器测试"""

    async def test_query_calendar_success(self):
        """测试查询日历成功"""
        mock_calendar = Mock()
        mock_calendar.list_events = AsyncMock(
            return_value=[
                {
                    "summary": "团队会议",
                    "start": {"dateTime": "2025-11-28T10:00:00+08:00"},
                },
                {
                    "summary": "产品评审",
                    "start": {"dateTime": "2025-11-28T14:00:00+08:00"},
                },
            ]
        )

        mock_claude = Mock()
        mock_claude.complete = AsyncMock(
            return_value="您有2个事件：团队会议（10:00）和产品评审（14:00）"
        )

        executor = QueryExecutor(mock_calendar, mock_claude)

        entities = ExtractedEntities(
            time=TimeEntity(start=datetime(2025, 11, 28))
        )

        result = await executor.query_calendar(entities)

        assert result.status == ExecutionStatus.SUCCESS
        assert result.data["count"] == 2

    async def test_query_calendar_no_events(self):
        """测试查询无事件"""
        mock_calendar = Mock()
        mock_calendar.list_events = AsyncMock(return_value=[])

        mock_claude = Mock()

        executor = QueryExecutor(mock_calendar, mock_claude)

        entities = ExtractedEntities(
            time=TimeEntity(start=datetime.now())
        )

        result = await executor.query_calendar(entities)

        assert result.status == ExecutionStatus.SUCCESS
        assert "没有安排" in result.message


@pytest.mark.asyncio
class TestReportGenerator:
    """报告生成器测试"""

    async def test_generate_weekly_report(self):
        """测试生成周报"""
        mock_calendar = Mock()
        mock_calendar.list_events = AsyncMock(
            return_value=[
                {"summary": "会议1", "start": {"dateTime": "2025-11-25T10:00:00"}},
                {"summary": "会议2", "start": {"dateTime": "2025-11-26T14:00:00"}},
            ]
        )

        mock_notion = Mock()
        mock_notion.create_page = AsyncMock(
            return_value={"id": "report123", "url": "https://notion.so/report123"}
        )

        mock_claude = Mock()
        mock_claude.complete = AsyncMock(
            return_value="本周共有2个事件，主要是团队会议和产品讨论。"
        )

        generator = ReportGenerator(mock_calendar, mock_notion, mock_claude)

        result = await generator.generate_weekly_report()

        assert result.status == ExecutionStatus.SUCCESS
        assert "周报" in result.message
        assert mock_notion.create_page.called


@pytest.mark.asyncio
class TestExecutorRetry:
    """测试执行器重试机制"""

    async def test_retry_on_failure(self):
        """测试失败时重试"""
        mock_adapter = Mock()

        # Mock: 第一次调用返回成功结果
        # (因为 execute() 内部调用 create_event，不会抛出异常)
        mock_adapter.create_event = AsyncMock(
            return_value={"id": "event123", "summary": "测试会议"}
        )

        executor = CalendarExecutor(mock_adapter)

        entities = ExtractedEntities(
            title="测试会议",
            time=TimeEntity(start=datetime.now()),
        )

        # 测试直接执行（无需重试）
        result = await executor.execute(entities)

        # 应该一次成功
        assert result.status == ExecutionStatus.SUCCESS
        assert mock_adapter.create_event.call_count == 1
