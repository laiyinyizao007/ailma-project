#!/usr/bin/env python3
"""
查找 Notion 父页面 ID 的辅助脚本

帮助用户找到正确的父页面 ID（而不是数据库 ID）
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Colors
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'


def print_success(message):
    print(f"{GREEN}✅ {message}{NC}")


def print_error(message):
    print(f"{RED}❌ {message}{NC}")


def print_warning(message):
    print(f"{YELLOW}⚠️  {message}{NC}")


def print_info(message):
    print(f"{BLUE}ℹ️  {message}{NC}")


def main():
    print(f"{YELLOW}Notion 父页面查找工具{NC}")
    print("=" * 50)

    notion_api_key = os.getenv("NOTION_API_KEY")
    if not notion_api_key:
        print_error("NOTION_API_KEY 未配置")
        sys.exit(1)

    try:
        from notion_client import Client

        notion = Client(auth=notion_api_key)

        # 搜索所有页面
        print_info("搜索你的 Notion 工作区中的页面...")
        print()

        response = notion.search(
            filter={"property": "object", "value": "page"},
            page_size=10
        )

        if not response["results"]:
            print_warning("未找到任何页面")
            print()
            print("解决方案:")
            print("1. 在 Notion 中创建一个新页面（命名为 'AILMA 工作区'）")
            print("2. 将 Integration 分享给该页面")
            print("3. 复制页面 URL 中的 ID 部分")
            sys.exit(1)

        print(f"{GREEN}找到 {len(response['results'])} 个页面：{NC}\n")

        for i, page in enumerate(response["results"], 1):
            page_id = page["id"].replace("-", "")

            # 获取页面标题
            title = "无标题"
            if page.get("properties"):
                title_prop = page["properties"].get("title")
                if title_prop and title_prop.get("title"):
                    if len(title_prop["title"]) > 0:
                        title = title_prop["title"][0]["plain_text"]
            elif page.get("title"):
                if len(page["title"]) > 0:
                    title = page["title"][0]["plain_text"]

            print(f"{i}. {title}")
            print(f"   ID: {page_id}")
            print(f"   URL: https://www.notion.so/{page_id}")
            print()

        print("=" * 50)
        print(f"{YELLOW}如何选择父页面：{NC}")
        print()
        print("1. 选择一个现有页面，或在 Notion 中创建新页面")
        print("2. 确保该页面已分享给你的 Integration")
        print("3. 复制页面 ID 到 .env 文件")
        print()
        print("示例:")
        print(f"  {BLUE}# 在 .env 中添加{NC}")
        print("  PARENT_PAGE_ID=你选择的页面ID")
        print()

    except ImportError:
        print_error("notion-client 未安装")
        print_info("安装: pip install notion-client")
        sys.exit(1)
    except Exception as e:
        print_error(f"查询失败: {str(e)}")
        print()
        print("可能的原因:")
        print("1. API Key 无效")
        print("2. Integration 未分享给任何页面")
        print("3. 网络连接问题")
        sys.exit(1)


if __name__ == "__main__":
    main()
