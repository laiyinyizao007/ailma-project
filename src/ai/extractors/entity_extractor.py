"""
实体提取器
"""

from datetime import datetime
from typing import Dict, Any

from src.ai.models.entity import (
    ExtractedEntities,
    TimeEntity,
    LocationEntity,
    PersonEntity,
)
from src.ai.models.intent import IntentType
from src.ai.clients.claude import ClaudeClient
from src.ai.prompts.templates import PromptManager
from src.ai.parsers.time_parser import TimeParser
from src.config import settings


class EntityExtractor:
    """实体提取器"""

    def __init__(
        self,
        claude_client: ClaudeClient,
        prompt_manager: PromptManager,
        time_parser: TimeParser,
    ):
        self.client = claude_client
        self.prompts = prompt_manager
        self.time_parser = time_parser

    async def extract(
        self, user_input: str, intent: IntentType
    ) -> ExtractedEntities:
        """
        从用户输入中提取实体

        Args:
            user_input: 用户输入
            intent: 意图类型

        Returns:
            提取的实体
        """
        # 生成 prompt
        current_time = datetime.now().isoformat()
        timezone = settings.google_calendar_timezone

        prompt = self.prompts.get_entity_prompt(
            user_input=user_input,
            intent_type=intent.value,
            current_time=current_time,
            timezone=timezone,
        )

        try:
            # 调用 LLM 提取实体
            response = await self.client.complete_json(
                prompt=prompt, max_tokens=1024
            )

            # 解析响应
            entities = ExtractedEntities()

            # 基本字段
            entities.title = response.get("title")
            entities.description = response.get("description")
            entities.tags = response.get("tags", [])
            entities.priority = response.get("priority")

            # 时间实体
            if "time" in response:
                time_data = response["time"]
                entities.time = TimeEntity(
                    start=self._parse_datetime(time_data.get("start")),
                    end=(
                        self._parse_datetime(time_data.get("end"))
                        if time_data.get("end")
                        else None
                    ),
                    is_all_day=time_data.get("is_all_day", False),
                    recurrence=time_data.get("recurrence"),
                    timezone=timezone,
                )

            # 地点实体
            if "location" in response:
                loc_data = response["location"]
                entities.location = LocationEntity(
                    name=loc_data.get("name", ""),
                    address=loc_data.get("address"),
                    url=loc_data.get("url"),
                )

            # 参与者
            if "participants" in response:
                entities.participants = [
                    PersonEntity(
                        name=p.get("name", ""), email=p.get("email")
                    )
                    for p in response["participants"]
                ]

            # 元数据
            entities.metadata = response.get("metadata", {})

            # 验证必填字段
            self._validate_entities(entities, intent)

            return entities

        except Exception as e:
            # 返回空实体
            return ExtractedEntities(metadata={"error": str(e)})

    def _parse_datetime(self, dt_str: str) -> datetime:
        """解析日期时间字符串"""
        if not dt_str:
            return datetime.now()

        try:
            # 尝试 ISO 8601
            return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        except:
            # 使用时间解析器
            return self.time_parser.parse(dt_str)

    def _validate_entities(
        self, entities: ExtractedEntities, intent: IntentType
    ) -> None:
        """验证实体完整性"""
        if intent in [
            IntentType.CALENDAR_CREATE,
            IntentType.NOTION_CREATE_PAGE,
            IntentType.NOTION_CREATE_TODO,
        ]:
            if not entities.title:
                raise ValueError("缺少标题")

        if intent == IntentType.CALENDAR_CREATE:
            if not entities.time:
                raise ValueError("缺少时间信息")
