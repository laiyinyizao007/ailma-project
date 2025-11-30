"""
查询执行器
处理日历查询和数据检索
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any

from src.executors.base_executor import BaseExecutor, ExecutionResult, ExecutionStatus
from src.adapters.google_calendar.adapter import GoogleCalendarAdapter
from src.ai.clients.claude import ClaudeClient
from src.ai.models.entity import ExtractedEntities


class QueryExecutor(BaseExecutor):
    """查询执行器"""

    def __init__(
        self,
        calendar_adapter: GoogleCalendarAdapter,
        claude_client: ClaudeClient,
    ):
        super().__init__(max_retries=2)
        self.calendar = calendar_adapter
        self.claude = claude_client

    async def query_calendar(self, entities: ExtractedEntities) -> ExecutionResult:
        """查询日历事件"""
        started_at = datetime.now()

        try:
            # 解析查询时间范围
            time_range = self._parse_time_range(entities)

            # 查询事件
            events = await self.calendar.list_events(
                time_min=time_range["start"],
                time_max=time_range["end"],
                max_results=100,
            )

            # 使用 AI 格式化响应
            formatted_response = await self._format_query_response(
                events, time_range
            )

            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message=formatted_response,
                data={"events": events, "count": len(events)},
                started_at=started_at,
                completed_at=datetime.now(),
            )

        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message="查询日历失败",
                error=str(e),
                started_at=started_at,
                completed_at=datetime.now(),
            )

    def _parse_time_range(self, entities: ExtractedEntities) -> Dict[str, datetime]:
        """解析查询时间范围"""
        now = datetime.now()

        if entities.time and entities.time.start:
            # 如果指定了时间，使用指定的时间
            start = entities.time.start
            if entities.time.end:
                end = entities.time.end
            else:
                # 默认查询一天
                end = start + timedelta(days=1)
        else:
            # 默认查询今天
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)

        # 检查描述中的时间关键词
        if entities.description:
            desc_lower = entities.description.lower()

            if "明天" in desc_lower:
                start = start + timedelta(days=1)
                end = start + timedelta(days=1)
            elif "本周" in desc_lower or "这周" in desc_lower:
                # 本周一到周日
                start = now - timedelta(days=now.weekday())
                end = start + timedelta(days=7)
            elif "下周" in desc_lower:
                start = now - timedelta(days=now.weekday()) + timedelta(days=7)
                end = start + timedelta(days=7)
            elif "本月" in desc_lower or "这个月" in desc_lower:
                start = now.replace(day=1)
                # 下个月第一天
                if start.month == 12:
                    end = start.replace(year=start.year + 1, month=1)
                else:
                    end = start.replace(month=start.month + 1)

        return {"start": start, "end": end}

    async def _format_query_response(
        self, events: List[Dict[str, Any]], time_range: Dict[str, datetime]
    ) -> str:
        """格式化查询响应"""
        if not events:
            return f"在 {time_range['start'].strftime('%Y-%m-%d')} 到 {time_range['end'].strftime('%Y-%m-%d')} 期间没有安排"

        # 构建事件列表
        events_text = "\n".join([
            f"- {event.get('summary', '无标题')} ({self._format_event_time(event)})"
            for event in events
        ])

        # 使用 AI 生成自然语言回复
        prompt = f"""
用户查询了日历安排。请用简洁、友好的语气总结以下事件：

时间范围: {time_range['start'].strftime('%Y-%m-%d')} 到 {time_range['end'].strftime('%Y-%m-%d')}

事件列表:
{events_text}

要求：
- 总结事件数量
- 按时间顺序列出主要事件
- 突出重要会议
- 语气自然友好
"""

        response = await self.claude.complete(prompt, max_tokens=512)
        return response

    def _format_event_time(self, event: Dict[str, Any]) -> str:
        """格式化事件时间"""
        start = event.get("start", {})

        if "dateTime" in start:
            # 有具体时间
            dt = datetime.fromisoformat(start["dateTime"].replace("Z", "+00:00"))
            return dt.strftime("%m-%d %H:%M")
        elif "date" in start:
            # 全天事件
            return start["date"]
        else:
            return "未知时间"

    async def execute(self, entities: ExtractedEntities) -> ExecutionResult:
        """执行查询"""
        return await self.query_calendar(entities)
