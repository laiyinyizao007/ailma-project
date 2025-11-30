"""
报告生成器
从多个数据源聚合信息并生成结构化报告
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from src.executors.base_executor import BaseExecutor, ExecutionResult, ExecutionStatus
from src.adapters.google_calendar.adapter import GoogleCalendarAdapter
from src.adapters.notion.adapter import NotionAdapter
from src.ai.clients.claude import ClaudeClient
from src.config import settings


class ReportGenerator(BaseExecutor):
    """报告生成器"""

    def __init__(
        self,
        calendar_adapter: GoogleCalendarAdapter,
        notion_adapter: NotionAdapter,
        claude_client: ClaudeClient,
    ):
        super().__init__(max_retries=2)
        self.calendar = calendar_adapter
        self.notion = notion_adapter
        self.claude = claude_client

    async def generate_weekly_report(self) -> ExecutionResult:
        """生成周报"""
        started_at = datetime.now()

        try:
            # 1. 获取本周时间范围
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)

            # 2. 聚合数据
            calendar_events = await self._fetch_calendar_events(week_start, week_end)

            # 3. 使用 AI 生成摘要
            summary = await self._generate_summary(
                calendar_events,
                week_start,
                week_end,
                report_type="weekly"
            )

            # 4. 创建报告页面
            report_title = f"周报 - {week_start.strftime('%Y-%m-%d')} 到 {week_end.strftime('%Y-%m-%d')}"
            report_content = self._format_report(summary, calendar_events)

            page = await self.notion.create_page(
                parent_id=settings.reports_db_id,
                title=report_title,
                content=report_content,
                properties={
                    "Type": {"select": {"name": "Weekly Report"}},
                    "Period Start": {"date": {"start": week_start.isoformat()}},
                    "Period End": {"date": {"start": week_end.isoformat()}},
                },
            )

            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message=f"成功生成周报: {report_title}",
                data=page,
                started_at=started_at,
                completed_at=datetime.now(),
            )

        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message="生成周报失败",
                error=str(e),
                started_at=started_at,
                completed_at=datetime.now(),
            )

    async def generate_monthly_report(self) -> ExecutionResult:
        """生成月报"""
        started_at = datetime.now()

        try:
            # 1. 获取本月时间范围
            today = datetime.now()
            month_start = today.replace(day=1)

            # 下个月第一天 - 1天 = 本月最后一天
            if month_start.month == 12:
                next_month = month_start.replace(year=month_start.year + 1, month=1)
            else:
                next_month = month_start.replace(month=month_start.month + 1)
            month_end = next_month - timedelta(days=1)

            # 2. 聚合数据
            calendar_events = await self._fetch_calendar_events(month_start, month_end)

            # 3. 使用 AI 生成摘要
            summary = await self._generate_summary(
                calendar_events,
                month_start,
                month_end,
                report_type="monthly"
            )

            # 4. 创建报告页面
            report_title = f"月报 - {month_start.strftime('%Y年%m月')}"
            report_content = self._format_report(summary, calendar_events)

            page = await self.notion.create_page(
                parent_id=settings.reports_db_id,
                title=report_title,
                content=report_content,
                properties={
                    "Type": {"select": {"name": "Monthly Report"}},
                    "Period Start": {"date": {"start": month_start.isoformat()}},
                    "Period End": {"date": {"start": month_end.isoformat()}},
                },
            )

            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message=f"成功生成月报: {report_title}",
                data=page,
                started_at=started_at,
                completed_at=datetime.now(),
            )

        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message="生成月报失败",
                error=str(e),
                started_at=started_at,
                completed_at=datetime.now(),
            )

    async def _fetch_calendar_events(
        self, start: datetime, end: datetime
    ) -> List[Dict[str, Any]]:
        """获取日历事件"""
        events = await self.calendar.list_events(
            time_min=start,
            time_max=end,
            max_results=1000,
        )
        return events

    async def _generate_summary(
        self,
        events: List[Dict[str, Any]],
        start: datetime,
        end: datetime,
        report_type: str = "weekly",
    ) -> str:
        """使用 AI 生成摘要"""
        # 构建提示
        events_text = "\n".join([
            f"- {event.get('summary', '无标题')} ({event.get('start', {}).get('dateTime', '未知时间')})"
            for event in events
        ])

        period_label = "本周" if report_type == "weekly" else "本月"

        prompt = f"""
分析以下{period_label}的日历事件，生成工作总结报告。

时间范围: {start.strftime('%Y-%m-%d')} 到 {end.strftime('%Y-%m-%d')}

事件列表:
{events_text}

请生成结构化的总结报告，包括：
1. 总体概览（事件总数、主要活动类型）
2. 重点事件（最重要的3-5个事件）
3. 时间分配分析（会议、工作、个人时间等）
4. 关键成果和产出
5. 下周/下月建议

要求：
- 简洁明了
- 突出重点
- 数据驱动
"""

        summary = await self.claude.complete(prompt, max_tokens=1024)
        return summary

    def _format_report(self, summary: str, events: List[Dict[str, Any]]) -> str:
        """格式化报告内容"""
        content = f"""# AI 生成摘要

{summary}

---

# 详细事件列表

共 {len(events)} 个事件

"""

        # 按日期分组
        events_by_date = {}
        for event in events:
            start_time = event.get("start", {}).get("dateTime", "")
            if not start_time:
                continue

            date_key = start_time.split("T")[0]
            if date_key not in events_by_date:
                events_by_date[date_key] = []
            events_by_date[date_key].append(event)

        # 生成每日事件列表
        for date_key in sorted(events_by_date.keys()):
            content += f"\n## {date_key}\n\n"
            for event in events_by_date[date_key]:
                title = event.get("summary", "无标题")
                start_time = event.get("start", {}).get("dateTime", "")
                time_str = start_time.split("T")[1][:5] if "T" in start_time else ""
                content += f"- **{time_str}** {title}\n"

        return content

    async def execute(self, report_type: str = "weekly") -> ExecutionResult:
        """执行报告生成"""
        if report_type == "weekly":
            return await self.generate_weekly_report()
        elif report_type == "monthly":
            return await self.generate_monthly_report()
        else:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message=f"不支持的报告类型: {report_type}",
            )
