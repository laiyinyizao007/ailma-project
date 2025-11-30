"""
意图类型定义
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class IntentType(str, Enum):
    """支持的意图类型"""

    # 日历操作
    CALENDAR_CREATE = "calendar_create"
    CALENDAR_QUERY = "calendar_query"
    CALENDAR_UPDATE = "calendar_update"
    CALENDAR_DELETE = "calendar_delete"

    # Notion 操作
    NOTION_CREATE_PAGE = "notion_create_page"
    NOTION_CREATE_TODO = "notion_create_todo"
    NOTION_QUERY = "notion_query"

    # 报告生成
    GENERATE_REPORT = "generate_report"

    # 设置
    UPDATE_SETTINGS = "update_settings"

    # 未知
    UNKNOWN = "unknown"


@dataclass
class IntentResult:
    """意图识别结果"""

    type: IntentType
    confidence: float
    raw_input: str
    explanation: Optional[str] = None

    def is_confident(self, threshold: float = 0.7) -> bool:
        """判断置信度是否达标"""
        return self.confidence >= threshold
