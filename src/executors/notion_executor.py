"""
Notion 操作执行器
"""

from datetime import datetime
from typing import Optional

from src.executors.base_executor import BaseExecutor, ExecutionResult, ExecutionStatus
from src.adapters.notion.adapter import NotionAdapter
from src.ai.models.entity import ExtractedEntities
from src.config import settings


class NotionExecutor(BaseExecutor):
    """Notion 执行器"""

    def __init__(self, notion_adapter: NotionAdapter):
        super().__init__(max_retries=3)
        self.notion = notion_adapter

    async def create_page(self, entities: ExtractedEntities) -> ExecutionResult:
        """创建 Notion 页面"""
        started_at = datetime.now()

        try:
            # 验证必填字段
            if not entities.title:
                return ExecutionResult(
                    status=ExecutionStatus.FAILED,
                    message="缺少页面标题",
                    started_at=started_at,
                    completed_at=datetime.now(),
                )

            # 构建页面内容
            content = self._build_page_content(entities)

            # 创建页面
            page = await self.notion.create_page(
                parent_id=settings.reports_db_id,  # 默认创建在 Reports 数据库
                title=entities.title,
                content=content,
                properties=self._build_properties(entities),
            )

            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message=f"成功创建页面: {entities.title}",
                data=page,
                started_at=started_at,
                completed_at=datetime.now(),
            )

        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message="创建页面失败",
                error=str(e),
                started_at=started_at,
                completed_at=datetime.now(),
            )

    async def create_todo(self, entities: ExtractedEntities) -> ExecutionResult:
        """创建待办事项"""
        started_at = datetime.now()

        try:
            if not entities.title:
                return ExecutionResult(
                    status=ExecutionStatus.FAILED,
                    message="缺少待办事项标题",
                    started_at=started_at,
                    completed_at=datetime.now(),
                )

            # 创建待办页面
            properties = {
                "Status": {"select": {"name": "Not Started"}},
                "Priority": {
                    "select": {"name": entities.priority or "Medium"}
                },
            }

            if entities.time and entities.time.start:
                properties["Due Date"] = {
                    "date": {"start": entities.time.start.isoformat()}
                }

            page = await self.notion.create_page(
                parent_id=settings.command_center_db_id,
                title=entities.title,
                content=entities.description,
                properties=properties,
            )

            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message=f"成功创建待办: {entities.title}",
                data=page,
                started_at=started_at,
                completed_at=datetime.now(),
            )

        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message="创建待办失败",
                error=str(e),
                started_at=started_at,
                completed_at=datetime.now(),
            )

    def _build_page_content(self, entities: ExtractedEntities) -> str:
        """构建页面内容（Markdown）"""
        content_parts = []

        if entities.description:
            content_parts.append(entities.description)

        # 添加元数据
        if entities.time:
            content_parts.append(f"\n## 时间\n{entities.time.start.strftime('%Y-%m-%d %H:%M')}")

        if entities.location:
            content_parts.append(f"\n## 地点\n{entities.location.name}")

        if entities.participants:
            participants_list = "\n".join([f"- {p.name}" for p in entities.participants])
            content_parts.append(f"\n## 参与者\n{participants_list}")

        if entities.tags:
            tags_str = ", ".join([f"#{tag}" for tag in entities.tags])
            content_parts.append(f"\n## 标签\n{tags_str}")

        return "\n\n".join(content_parts)

    def _build_properties(self, entities: ExtractedEntities) -> dict:
        """构建 Notion 属性"""
        properties = {}

        if entities.tags:
            properties["Tags"] = {
                "multi_select": [{"name": tag} for tag in entities.tags]
            }

        if entities.priority:
            properties["Priority"] = {"select": {"name": entities.priority}}

        return properties

    async def execute(self, entities: ExtractedEntities, intent_type: str) -> ExecutionResult:
        """执行 Notion 操作"""
        from src.ai.models.intent import IntentType

        if intent_type == IntentType.NOTION_CREATE_PAGE.value:
            return await self.create_page(entities)
        elif intent_type == IntentType.NOTION_CREATE_TODO.value:
            return await self.create_todo(entities)
        else:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message=f"不支持的操作类型: {intent_type}",
            )
