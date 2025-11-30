"""
Notion MCP Adapter
通过 MCP 协议操作 Notion
"""

from typing import List, Optional, Dict, Any
import httpx

from src.adapters import BaseAdapter
from src.config import settings


class NotionAdapter(BaseAdapter):
    """Notion MCP 适配器"""

    def __init__(self, mcp_server_url: Optional[str] = None):
        self.mcp_server_url = mcp_server_url or settings.notion_mcp_server_url
        self.api_key = settings.notion_api_key
        self.client = httpx.AsyncClient(
            timeout=30.0, headers={"Authorization": f"Bearer {self.api_key}"}
        )

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

    async def create_page(
        self,
        parent_id: str,
        title: str,
        content: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        创建 Notion 页面

        Args:
            parent_id: 父页面/数据库 ID
            title: 页面标题
            content: 页面内容 (Markdown)
            properties: 自定义属性

        Returns:
            创建的页面信息
        """
        payload = {
            "tool": "create_page",
            "parameters": {
                "parent": {"database_id": parent_id},
                "properties": {"title": {"title": [{"text": {"content": title}}]}},
            },
        }

        if properties:
            payload["parameters"]["properties"].update(properties)

        if content:
            # 转换 Markdown 为 Notion blocks
            payload["parameters"]["children"] = self._markdown_to_blocks(content)

        response = await self.client.post(
            f"{self.mcp_server_url}/execute", json=payload
        )
        response.raise_for_status()

        return response.json()

    async def query_database(
        self,
        database_id: str,
        filter_conditions: Optional[Dict[str, Any]] = None,
        sorts: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        查询数据库

        Args:
            database_id: 数据库 ID
            filter_conditions: 过滤条件
            sorts: 排序条件

        Returns:
            查询结果
        """
        payload = {
            "tool": "query_database",
            "parameters": {"database_id": database_id},
        }

        if filter_conditions:
            payload["parameters"]["filter"] = filter_conditions
        if sorts:
            payload["parameters"]["sorts"] = sorts

        response = await self.client.post(
            f"{self.mcp_server_url}/execute", json=payload
        )
        response.raise_for_status()

        return response.json().get("results", [])

    async def update_page(
        self, page_id: str, properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        更新页面属性

        Args:
            page_id: 页面 ID
            properties: 要更新的属性

        Returns:
            更新后的页面
        """
        payload = {
            "tool": "update_page",
            "parameters": {"page_id": page_id, "properties": properties},
        }

        response = await self.client.post(
            f"{self.mcp_server_url}/execute", json=payload
        )
        response.raise_for_status()

        return response.json()

    async def append_blocks(
        self, page_id: str, content: str
    ) -> Dict[str, Any]:
        """
        追加内容到页面

        Args:
            page_id: 页面 ID
            content: 内容 (Markdown)

        Returns:
            更新结果
        """
        blocks = self._markdown_to_blocks(content)

        payload = {
            "tool": "append_block_children",
            "parameters": {"block_id": page_id, "children": blocks},
        }

        response = await self.client.post(
            f"{self.mcp_server_url}/execute", json=payload
        )
        response.raise_for_status()

        return response.json()

    def _markdown_to_blocks(self, markdown: str) -> List[Dict[str, Any]]:
        """
        将 Markdown 转换为 Notion blocks

        简化版实现，仅支持段落和标题
        """
        blocks = []
        lines = markdown.split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 标题
            if line.startswith("# "):
                blocks.append(
                    {
                        "object": "block",
                        "type": "heading_1",
                        "heading_1": {
                            "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                        },
                    }
                )
            elif line.startswith("## "):
                blocks.append(
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                        },
                    }
                )
            else:
                # 段落
                blocks.append(
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": line}}]
                        },
                    }
                )

        return blocks

    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
