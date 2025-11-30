"""
日历操作执行器
"""

from datetime import datetime, timedelta
from typing import Optional

from src.executors.base_executor import BaseExecutor, ExecutionResult, ExecutionStatus
from src.adapters.google_calendar.adapter import GoogleCalendarAdapter
from src.ai.models.entity import ExtractedEntities


class CalendarExecutor(BaseExecutor):
    """日历执行器"""

    def __init__(self, calendar_adapter: GoogleCalendarAdapter):
        super().__init__(max_retries=3)
        self.calendar = calendar_adapter

    async def create_event(self, entities: ExtractedEntities) -> ExecutionResult:
        """创建日历事件"""
        started_at = datetime.now()

        try:
            # 验证必填字段
            if not entities.title:
                return ExecutionResult(
                    status=ExecutionStatus.FAILED,
                    message="缺少事件标题",
                    started_at=started_at,
                    completed_at=datetime.now(),
                )

            if not entities.time:
                return ExecutionResult(
                    status=ExecutionStatus.FAILED,
                    message="缺少时间信息",
                    started_at=started_at,
                    completed_at=datetime.now(),
                )

            # 计算结束时间
            end_time = entities.time.end
            if not end_time:
                # 默认 1 小时
                end_time = entities.time.start + timedelta(hours=1)

            # 准备参与者列表
            attendees = (
                [p.email for p in entities.participants if p.email]
                if entities.participants
                else None
            )

            # 调用 Google Calendar API
            event = await self.calendar.create_event(
                title=entities.title,
                start_time=entities.time.start,
                end_time=end_time,
                description=entities.description,
                location=entities.location.name if entities.location else None,
                attendees=attendees,
                is_all_day=entities.time.is_all_day,
            )

            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message=f"成功创建事件: {entities.title}",
                data=event,
                started_at=started_at,
                completed_at=datetime.now(),
            )

        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message="创建事件失败",
                error=str(e),
                started_at=started_at,
                completed_at=datetime.now(),
            )

    async def execute(self, entities: ExtractedEntities) -> ExecutionResult:
        """执行日历操作"""
        return await self.create_event(entities)
