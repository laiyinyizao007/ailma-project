"""
Notion MCP 连接测试脚本

此脚本测试与 Notion 的基本连接，验证：
1. Notion API Token 是否有效
2. 能否访问工作区
3. 能否读取指定的数据库
4. 基本的 CRUD 操作

使用方法:
    python tests/mcp_integration/test_notion_connection.py
"""

import os
import sys
import asyncio
from datetime import datetime
from typing import Dict, Any, List

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 使用官方 Notion SDK（暂时，后续替换为 MCP Client）
from notion_client import AsyncClient


class NotionConnectionTester:
    """Notion 连接测试类"""

    def __init__(self):
        self.api_key = os.getenv("NOTION_API_KEY")
        self.command_db_id = os.getenv("COMMAND_CENTER_DB_ID")

        if not self.api_key:
            raise ValueError(
                "❌ 未找到 NOTION_API_KEY 环境变量！\n"
                "请在项目根目录创建 .env 文件并配置 NOTION_API_KEY"
            )

        self.client = AsyncClient(auth=self.api_key)
        print(f"✅ Notion Client 初始化成功")
        print(f"📋 API Key (前10位): {self.api_key[:10]}...")

    async def test_connection(self) -> bool:
        """测试基本连接"""
        print("\n" + "="*60)
        print("🔍 测试 1: 验证 API Token 有效性")
        print("="*60)

        try:
            # 获取当前用户信息
            me = await self.client.users.me()
            print(f"✅ 连接成功！")
            print(f"👤 用户信息:")
            print(f"   - Type: {me['type']}")
            print(f"   - ID: {me['id']}")
            return True

        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False

    async def test_search(self) -> bool:
        """测试搜索功能"""
        print("\n" + "="*60)
        print("🔍 测试 2: 搜索工作区内容")
        print("="*60)

        try:
            # 搜索所有页面和数据库
            results = await self.client.search(
                filter={"property": "object", "value": "database"}
            )

            databases = results.get("results", [])
            print(f"✅ 搜索成功！")
            print(f"📊 找到 {len(databases)} 个数据库:")

            for i, db in enumerate(databases[:5], 1):  # 只显示前5个
                title = db.get("title", [{}])[0].get("plain_text", "无标题")
                print(f"   {i}. {title} (ID: {db['id']})")

            return True

        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            return False

    async def test_database_query(self) -> bool:
        """测试数据库查询"""
        print("\n" + "="*60)
        print("🔍 测试 3: 查询指定数据库")
        print("="*60)

        if not self.command_db_id:
            print("⚠️  未配置 COMMAND_CENTER_DB_ID，跳过此测试")
            return True

        try:
            # 查询数据库内容
            response = await self.client.databases.query(
                database_id=self.command_db_id
            )

            items = response.get("results", [])
            print(f"✅ 查询成功！")
            print(f"📝 数据库包含 {len(items)} 条记录")

            if items:
                print(f"\n前3条记录:")
                for i, item in enumerate(items[:3], 1):
                    props = item.get("properties", {})
                    # 尝试提取标题
                    title_prop = None
                    for key, value in props.items():
                        if value.get("type") == "title":
                            title_content = value.get("title", [])
                            if title_content:
                                title_prop = title_content[0].get("plain_text", "")
                            break

                    print(f"   {i}. {title_prop or '(无标题)'}")

            return True

        except Exception as e:
            print(f"❌ 查询失败: {e}")
            print(f"提示: 请确保 Integration 已被添加到此数据库")
            return False

    async def test_create_page(self) -> bool:
        """测试创建页面"""
        print("\n" + "="*60)
        print("🔍 测试 4: 创建测试页面")
        print("="*60)

        if not self.command_db_id:
            print("⚠️  未配置 COMMAND_CENTER_DB_ID，跳过此测试")
            return True

        try:
            # 创建测试页面
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            new_page = await self.client.pages.create(
                parent={"database_id": self.command_db_id},
                properties={
                    "指令": {  # 假设数据库有 "指令" 字段（title 类型）
                        "title": [
                            {
                                "text": {
                                    "content": f"🧪 连接测试 - {timestamp}"
                                }
                            }
                        ]
                    },
                    # 如果有状态字段
                    # "状态": {
                    #     "select": {"name": "⏳ Pending"}
                    # }
                }
            )

            page_id = new_page["id"]
            page_url = new_page["url"]

            print(f"✅ 页面创建成功！")
            print(f"📄 页面 ID: {page_id}")
            print(f"🔗 页面链接: {page_url}")

            # 清理：删除测试页面
            print(f"\n🗑️  清理测试数据...")
            await self.client.pages.update(
                page_id=page_id,
                archived=True
            )
            print(f"✅ 测试页面已删除")

            return True

        except Exception as e:
            print(f"❌ 创建页面失败: {e}")
            print(f"\n可能的原因:")
            print(f"1. 数据库字段名称不匹配（需要有 'title' 类型的字段）")
            print(f"2. Integration 权限不足（需要 'insert content' 权限）")
            return False

    async def test_markdown_scenario(self) -> bool:
        """测试 Markdown 场景（模拟 MCP 行为）"""
        print("\n" + "="*60)
        print("🔍 测试 5: Markdown 内容写入 (模拟 MCP)")
        print("="*60)

        if not self.command_db_id:
            print("⚠️  未配置 COMMAND_CENTER_DB_ID，跳过此测试")
            return True

        try:
            # Markdown 内容
            markdown_content = """
# 📊 测试报告

## 完成事项
- [x] 完成连接测试
- [x] 验证数据库访问

## 统计信息
- 测试用例: 5个
- 执行时间: < 5秒

## 结论
✅ 所有测试通过！
            """

            # 将 Markdown 转换为 Notion Blocks (简化版)
            blocks = self._markdown_to_blocks(markdown_content)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 创建带内容的页面
            new_page = await self.client.pages.create(
                parent={"database_id": self.command_db_id},
                properties={
                    "指令": {
                        "title": [
                            {
                                "text": {
                                    "content": f"🧪 Markdown 测试 - {timestamp}"
                                }
                            }
                        ]
                    }
                },
                children=blocks
            )

            page_url = new_page["url"]

            print(f"✅ Markdown 页面创建成功！")
            print(f"🔗 页面链接: {page_url}")
            print(f"\n📝 注意: MCP 版本可以直接传入 Markdown 字符串，")
            print(f"         无需手动转换为 Blocks（这是 MCP 的优势！）")

            # 清理
            await asyncio.sleep(2)  # 给用户查看时间
            await self.client.pages.update(
                page_id=new_page["id"],
                archived=True
            )
            print(f"✅ 测试页面已删除")

            return True

        except Exception as e:
            print(f"❌ Markdown 测试失败: {e}")
            return False

    def _markdown_to_blocks(self, markdown: str) -> List[Dict[str, Any]]:
        """
        简化的 Markdown → Notion Blocks 转换
        注意: 真实的 MCP 客户端会自动处理这个转换！
        """
        blocks = []
        lines = markdown.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 标题
            if line.startswith('# '):
                blocks.append({
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                    }
                })
            elif line.startswith('## '):
                blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                    }
                })
            # 列表项
            elif line.startswith('- '):
                is_checked = line.startswith('- [x]')
                text = line[6:] if is_checked else line[2:]

                blocks.append({
                    "object": "block",
                    "type": "to_do" if '[' in line[:6] else "bulleted_list_item",
                    ("to_do" if '[' in line[:6] else "bulleted_list_item"): {
                        "rich_text": [{"type": "text", "text": {"content": text}}],
                        **({"checked": is_checked} if '[' in line[:6] else {})
                    }
                })
            # 普通段落
            else:
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": line}}]
                    }
                })

        return blocks

    async def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "🚀"*30)
        print("🚀  AILMA - Notion MCP 连接测试")
        print("🚀"*30)

        results = []

        # 测试 1: 基本连接
        results.append(await self.test_connection())

        # 测试 2: 搜索
        results.append(await self.test_search())

        # 测试 3: 数据库查询
        results.append(await self.test_database_query())

        # 测试 4: 创建页面
        results.append(await self.test_create_page())

        # 测试 5: Markdown 场景
        results.append(await self.test_markdown_scenario())

        # 汇总结果
        print("\n" + "="*60)
        print("📊 测试结果汇总")
        print("="*60)

        passed = sum(results)
        total = len(results)

        print(f"✅ 通过: {passed}/{total}")
        print(f"❌ 失败: {total - passed}/{total}")

        if passed == total:
            print("\n🎉 所有测试通过！Notion 连接正常！")
            print("\n💡 下一步:")
            print("   1. 将直接 API 调用替换为 MCP Client")
            print("   2. 利用 MCP 的 Markdown 原生支持")
            print("   3. 开始实现核心业务逻辑")
        else:
            print("\n⚠️  部分测试失败，请检查配置")


async def main():
    """主函数"""
    try:
        tester = NotionConnectionTester()
        await tester.run_all_tests()

    except ValueError as e:
        print(f"\n{e}")
        print("\n📝 配置步骤:")
        print("1. 访问 https://www.notion.so/my-integrations")
        print("2. 创建新的 Integration")
        print("3. 复制 Internal Integration Token")
        print("4. 在项目根目录创建 .env 文件")
        print("5. 添加: NOTION_API_KEY=secret_your_token")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ 测试执行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
