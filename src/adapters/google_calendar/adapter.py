"""
Google Calendar MCP Adapter
通过 MCP 协议操作 Google Calendar
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import httpx

from src.adapters import BaseAdapter
from src.config import settings


class GoogleCalendarAdapter(BaseAdapter):
    """Google Calendar MCP 适配器"""

    def __init__(
        self,
        mcp_server_url: Optional[str] = None,
        calendar_id: Optional[str] = None,
    ):
        self.mcp_server_url = mcp_server_url or settings.google_calendar_mcp_server_url
        self.calendar_id = calendar_id or settings.google_calendar_default_id
        self.client = httpx.AsyncClient(timeout=30.0)

    async def initialize(self) -> None:
        """初始化连接"""
        await self.health_check()

    async def health_check(self) -> bool:
        """健康检查"""
        try:
            response = await self.client.get(f"{self.mcp_server_url}/health")
            return response.status_code == 200
        except:
            return False

    async def create_event(
        self,
        title: str,
        start_time: datetime,
        end_time: Optional[datetime] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        is_all_day: bool = False,
    ) -> Dict[str, Any]:
        """
        创建日历事件

        Args:
            title: 事件标题
            start_time: 开始时间
            end_time: 结束时间
            description: 描述
            location: 地点
            attendees: 参与者邮箱列表
            is_all_day: 是否全天事件

        Returns:
            创建的事件信息
        """
        # 构造 MCP 请求
        payload = {
            "tool": "create_event",
            "parameters": {
                "calendar_id": self.calendar_id,
                "summary": title,
                "start": {
                    "dateTime": start_time.isoformat() if not is_all_day else None,
                    "date": start_time.date().isoformat() if is_all_day else None,
                    "timeZone": settings.google_calendar_timezone,
                },
                "end": {
                    "dateTime": (
                        end_time.isoformat()
                        if end_time and not is_all_day
                        else None
                    ),
                    "date": (
                        end_time.date().isoformat() if end_time and is_all_day else None
                    ),
                    "timeZone": settings.google_calendar_timezone,
                },
            },
        }

        if description:
            payload["parameters"]["description"] = description
        if location:
            payload["parameters"]["location"] = location
        if attendees:
            payload["parameters"]["attendees"] = [
                {"email": email} for email in attendees
            ]

        # 调用 MCP Server
        response = await self.client.post(
            f"{self.mcp_server_url}/execute", json=payload
        )
        response.raise_for_status()

        return response.json()

    async def list_events(
        self,
        time_min: datetime,
        time_max: datetime,
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        列出事件

        Args:
            time_min: 开始时间
            time_max: 结束时间
            max_results: 最多返回数量

        Returns:
            事件列表
        """
        payload = {
            "tool": "list_events",
            "parameters": {
                "calendar_id": self.calendar_id,
                "time_min": time_min.isoformat(),
                "time_max": time_max.isoformat(),
                "max_results": max_results,
            },
        }

        response = await self.client.post(
            f"{self.mcp_server_url}/execute", json=payload
        )
        response.raise_for_status()

        return response.json().get("items", [])

    async def update_event(
        self, event_id: str, updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        更新事件

        Args:
            event_id: 事件 ID
            updates: 更新的字段

        Returns:
            更新后的事件
        """
        payload = {
            "tool": "update_event",
            "parameters": {
                "calendar_id": self.calendar_id,
                "event_id": event_id,
                **updates,
            },
        }

        response = await self.client.post(
            f"{self.mcp_server_url}/execute", json=payload
        )
        response.raise_for_status()

        return response.json()

    async def delete_event(self, event_id: str) -> bool:
        """
        删除事件

        Args:
            event_id: 事件 ID

        Returns:
            是否成功
        """
        payload = {
            "tool": "delete_event",
            "parameters": {"calendar_id": self.calendar_id, "event_id": event_id},
        }

        response = await self.client.post(
            f"{self.mcp_server_url}/execute", json=payload
        )

        return response.status_code == 200

    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
