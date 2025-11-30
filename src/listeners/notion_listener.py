"""
Notion 指令监听器
定期轮询 Notion Command Center，检测新指令并触发执行
"""

import asyncio
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import logging

from src.adapters.notion.adapter import NotionAdapter
from src.ai.task_parser import TaskParser
from src.executors.calendar_executor import CalendarExecutor
from src.executors.base_executor import ExecutionResult, ExecutionStatus
from src.config import settings

logger = logging.getLogger(__name__)


class NotionListener:
    """Notion 指令监听器"""

    def __init__(
        self,
        notion_adapter: NotionAdapter,
        task_parser: TaskParser,
        calendar_executor: CalendarExecutor,
        notion_executor=None,
        query_executor=None,
        report_generator=None,
        poll_interval: int = None,
    ):
        self.notion = notion_adapter
        self.parser = task_parser
        self.calendar_executor = calendar_executor
        self.notion_executor = notion_executor
        self.query_executor = query_executor
        self.report_generator = report_generator
        self.poll_interval = poll_interval or settings.poll_interval_seconds
        self.last_check_time = datetime.now()
        self.running = False

    async def start(self):
        """启动监听器"""
        logger.info("Notion Listener 启动")
        self.running = True

        while self.running:
            try:
                await self._poll_and_process()
                await asyncio.sleep(self.poll_interval)
            except Exception as e:
                logger.error(f"轮询错误: {str(e)}", exc_info=True)
                await asyncio.sleep(self.poll_interval)

    async def stop(self):
        """停止监听器"""
        logger.info("Notion Listener 停止")
        self.running = False

    async def _poll_and_process(self):
        """轮询并处理新指令"""
        # 查询 Command Center 数据库
        new_commands = await self._fetch_new_commands()

        logger.info(f"检测到 {len(new_commands)} 条新指令")

        for command in new_commands:
            try:
                await self._process_command(command)
            except Exception as e:
                logger.error(
                    f"处理指令失败: {command.get('id')}, 错误: {str(e)}", exc_info=True
                )
                await self._update_command_status(
                    command["id"], "failed", error=str(e)
                )

        # 更新最后检查时间
        self.last_check_time = datetime.now()

    async def _fetch_new_commands(self) -> List[Dict[str, Any]]:
        """获取新指令"""
        # 查询未处理的指令
        filter_conditions = {
            "and": [
                {"property": "Status", "select": {"equals": "pending"}},
                {
                    "property": "Created",
                    "date": {"after": self.last_check_time.isoformat()},
                },
            ]
        }

        sorts = [{"property": "Created", "direction": "ascending"}]

        results = await self.notion.query_database(
            database_id=settings.command_center_db_id,
            filter_conditions=filter_conditions,
            sorts=sorts,
        )

        return results

    async def _process_command(self, command: Dict[str, Any]):
        """处理单个指令"""
        command_id = command["id"]
        user_input = self._extract_command_text(command)

        logger.info(f"处理指令: {command_id} - {user_input}")

        # 更新状态为 processing
        await self._update_command_status(command_id, "processing")

        # Step 1: 解析指令
        parse_result = await self.parser.parse(user_input)

        if not parse_result.is_valid():
            # 意图不明确，需要澄清
            await self._update_command_status(
                command_id,
                "needs_clarification",
                message=f"无法理解您的指令。{parse_result.intent.explanation}",
            )
            return

        # Step 2: 执行任务
        from src.ai.models.intent import IntentType

        intent_type = parse_result.intent.type
        result = None

        try:
            if intent_type == IntentType.CALENDAR_CREATE:
                result = await self.calendar_executor.execute(parse_result.entities)

            elif intent_type == IntentType.CALENDAR_QUERY:
                if self.query_executor:
                    result = await self.query_executor.execute(parse_result.entities)
                else:
                    result = ExecutionResult(
                        status=ExecutionStatus.FAILED,
                        message="查询功能未启用",
                    )

            elif intent_type in [IntentType.NOTION_CREATE_PAGE, IntentType.NOTION_CREATE_TODO]:
                if self.notion_executor:
                    result = await self.notion_executor.execute(
                        parse_result.entities, intent_type.value
                    )
                else:
                    result = ExecutionResult(
                        status=ExecutionStatus.FAILED,
                        message="Notion 功能未启用",
                    )

            elif intent_type == IntentType.GENERATE_REPORT:
                if self.report_generator:
                    # 从描述中提取报告类型
                    report_type = "weekly"  # 默认
                    if parse_result.entities.description:
                        desc = parse_result.entities.description.lower()
                        if "月" in desc or "monthly" in desc:
                            report_type = "monthly"
                    result = await self.report_generator.execute(report_type)
                else:
                    result = ExecutionResult(
                        status=ExecutionStatus.FAILED,
                        message="报告生成功能未启用",
                    )

            else:
                # 其他意图暂未实现
                await self._update_command_status(
                    command_id,
                    "failed",
                    message=f"暂不支持的操作类型: {intent_type.value}",
                )
                return

        except Exception as e:
            logger.error(f"执行任务时出错: {str(e)}", exc_info=True)
            result = ExecutionResult(
                status=ExecutionStatus.FAILED,
                message="执行失败",
                error=str(e),
            )

        if not result:
            await self._update_command_status(
                command_id,
                "failed",
                message="执行失败: 未知错误",
            )
            return

        # Step 3: 更新结果
        if result.is_success():
            await self._update_command_status(
                command_id, "completed", message=result.message, data=result.data
            )
        else:
            await self._update_command_status(
                command_id, "failed", message=result.message, error=result.error
            )

    def _extract_command_text(self, command: Dict[str, Any]) -> str:
        """从 Notion 页面提取指令文本"""
        # 假设指令在 "Command" 属性中
        properties = command.get("properties", {})
        command_prop = properties.get("Command", {})

        # 处理不同类型的属性
        if "title" in command_prop:
            title_parts = command_prop["title"]
            if title_parts:
                return title_parts[0].get("plain_text", "")

        if "rich_text" in command_prop:
            rich_text_parts = command_prop["rich_text"]
            if rich_text_parts:
                return rich_text_parts[0].get("plain_text", "")

        return ""

    async def _update_command_status(
        self,
        command_id: str,
        status: str,
        message: Optional[str] = None,
        error: Optional[str] = None,
        data: Optional[Any] = None,
    ):
        """更新指令状态"""
        properties = {
            "Status": {"select": {"name": status}},
            "Updated": {"date": {"start": datetime.now().isoformat()}},
        }

        if message:
            properties["Result"] = {"rich_text": [{"text": {"content": message}}]}

        if error:
            properties["Error"] = {"rich_text": [{"text": {"content": error}}]}

        await self.notion.update_page(page_id=command_id, properties=properties)
