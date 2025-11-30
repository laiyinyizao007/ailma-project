#!/usr/bin/env python3
"""
AILMA Notion 数据库创建脚本

自动在 Notion 中创建 AILMA 所需的 3 个数据库：
1. 指令中心 (Command Center) - 接收和处理用户指令
2. 日历事件 (Calendar Events) - 存储日历事件记录
3. 工作报告 (Reports) - 存储生成的周报/月报
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
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


def create_command_center_database(notion, parent_page_id):
    """创建指令中心数据库"""
    print(f"\n{BLUE}创建数据库: 指令中心 (Command Center)...{NC}")
    print("-" * 50)

    try:
        database = notion.databases.create(
            parent={
                "type": "page_id",
                "page_id": parent_page_id
            },
            title=[
                {
                    "type": "text",
                    "text": {"content": "📋 AILMA 指令中心"}
                }
            ],
            properties={
                "指令": {
                    "title": {}
                },
                "状态": {
                    "select": {
                        "options": [
                            {"name": "pending", "color": "yellow"},
                            {"name": "processing", "color": "blue"},
                            {"name": "completed", "color": "green"},
                            {"name": "failed", "color": "red"}
                        ]
                    }
                },
                "意图类型": {
                    "select": {
                        "options": [
                            {"name": "calendar_create", "color": "blue"},
                            {"name": "calendar_query", "color": "purple"},
                            {"name": "calendar_update", "color": "orange"},
                            {"name": "calendar_delete", "color": "red"},
                            {"name": "notion_create_page", "color": "green"},
                            {"name": "notion_create_todo", "color": "yellow"},
                            {"name": "generate_report", "color": "pink"},
                            {"name": "unknown", "color": "gray"}
                        ]
                    }
                },
                "置信度": {
                    "number": {
                        "format": "percent"
                    }
                },
                "执行结果": {
                    "rich_text": {}
                },
                "错误信息": {
                    "rich_text": {}
                },
                "创建时间": {
                    "created_time": {}
                },
                "处理时间": {
                    "date": {}
                }
            }
        )

        db_id = database["id"]
        print_success(f"指令中心数据库创建成功")
        print_info(f"数据库 ID: {db_id}")
        print_info(f"URL: https://www.notion.so/{db_id.replace('-', '')}")

        return db_id

    except Exception as e:
        print_error(f"创建失败: {str(e)}")
        return None


def create_calendar_events_database(notion, parent_page_id):
    """创建日历事件数据库"""
    print(f"\n{BLUE}创建数据库: 日历事件 (Calendar Events)...{NC}")
    print("-" * 50)

    try:
        database = notion.databases.create(
            parent={
                "type": "page_id",
                "page_id": parent_page_id
            },
            title=[
                {
                    "type": "text",
                    "text": {"content": "📅 AILMA 日历事件"}
                }
            ],
            properties={
                "事件标题": {
                    "title": {}
                },
                "开始时间": {
                    "date": {}
                },
                "地点": {
                    "rich_text": {}
                },
                "参与者": {
                    "multi_select": {
                        "options": []
                    }
                },
                "事件类型": {
                    "select": {
                        "options": [
                            {"name": "会议", "color": "blue"},
                            {"name": "个人", "color": "green"},
                            {"name": "团队活动", "color": "purple"},
                            {"name": "培训", "color": "orange"},
                            {"name": "其他", "color": "gray"}
                        ]
                    }
                },
                "状态": {
                    "select": {
                        "options": [
                            {"name": "已计划", "color": "yellow"},
                            {"name": "进行中", "color": "blue"},
                            {"name": "已完成", "color": "green"},
                            {"name": "已取消", "color": "red"}
                        ]
                    }
                },
                "Google Calendar ID": {
                    "rich_text": {}
                },
                "Meet 链接": {
                    "url": {}
                },
                "描述": {
                    "rich_text": {}
                },
                "创建时间": {
                    "created_time": {}
                }
            }
        )

        db_id = database["id"]
        print_success(f"日历事件数据库创建成功")
        print_info(f"数据库 ID: {db_id}")
        print_info(f"URL: https://www.notion.so/{db_id.replace('-', '')}")

        return db_id

    except Exception as e:
        print_error(f"创建失败: {str(e)}")
        return None


def create_reports_database(notion, parent_page_id):
    """创建工作报告数据库"""
    print(f"\n{BLUE}创建数据库: 工作报告 (Reports)...{NC}")
    print("-" * 50)

    try:
        database = notion.databases.create(
            parent={
                "type": "page_id",
                "page_id": parent_page_id
            },
            title=[
                {
                    "type": "text",
                    "text": {"content": "📊 AILMA 工作报告"}
                }
            ],
            properties={
                "报告标题": {
                    "title": {}
                },
                "报告类型": {
                    "select": {
                        "options": [
                            {"name": "日报", "color": "blue"},
                            {"name": "周报", "color": "green"},
                            {"name": "月报", "color": "purple"},
                            {"name": "季度报告", "color": "orange"},
                            {"name": "年度总结", "color": "red"}
                        ]
                    }
                },
                "时间范围": {
                    "date": {}
                },
                "事件统计": {
                    "number": {}
                },
                "会议时长": {
                    "number": {
                        "format": "number_with_commas"
                    }
                },
                "生成时间": {
                    "created_time": {}
                },
                "状态": {
                    "select": {
                        "options": [
                            {"name": "草稿", "color": "yellow"},
                            {"name": "已完成", "color": "green"},
                            {"name": "已归档", "color": "gray"}
                        ]
                    }
                },
                "标签": {
                    "multi_select": {
                        "options": [
                            {"name": "重要", "color": "red"},
                            {"name": "团队", "color": "blue"},
                            {"name": "个人", "color": "green"}
                        ]
                    }
                }
            }
        )

        db_id = database["id"]
        print_success(f"工作报告数据库创建成功")
        print_info(f"数据库 ID: {db_id}")
        print_info(f"URL: https://www.notion.so/{db_id.replace('-', '')}")

        return db_id

    except Exception as e:
        print_error(f"创建失败: {str(e)}")
        return None


def update_env_file(command_center_id, calendar_id, reports_id):
    """更新 .env 文件中的数据库 ID"""
    print(f"\n{BLUE}更新 .env 文件...{NC}")
    print("-" * 50)

    try:
        with open('.env', 'r') as f:
            content = f.read()

        # 替换数据库 ID
        content = content.replace(
            f'COMMAND_CENTER_DB_ID=2bb84b1a1c798051a616de266920ab4e',
            f'COMMAND_CENTER_DB_ID={command_center_id}'
        )
        content = content.replace(
            f'CALENDAR_DB_ID=2bb84b1a1c798051a616de266920ab4e',
            f'CALENDAR_DB_ID={calendar_id}'
        )
        content = content.replace(
            f'REPORTS_DB_ID=2bb84b1a1c798051a616de266920ab4e',
            f'REPORTS_DB_ID={reports_id}'
        )

        with open('.env', 'w') as f:
            f.write(content)

        print_success(".env 文件已更新")
        return True

    except Exception as e:
        print_error(f"更新 .env 失败: {str(e)}")
        return False


def main():
    """主函数"""
    print(f"{YELLOW}AILMA Notion 数据库创建工具{NC}")
    print("=" * 50)

    # 检查 Notion API Key
    notion_api_key = os.getenv("NOTION_API_KEY")
    if not notion_api_key or notion_api_key == "secret_your_notion_integration_token_here":
        print_error("NOTION_API_KEY 未配置")
        print_info("请先在 .env 文件中配置 Notion API Key")
        sys.exit(1)

    # 检查父页面 ID
    parent_page_id = os.getenv("PARENT_PAGE_ID")
    if not parent_page_id:
        print_error("PARENT_PAGE_ID 未配置")
        print_info("请在 .env 文件中添加: PARENT_PAGE_ID=你的页面ID")
        sys.exit(1)

    # 清理 ID（移除破折号）
    parent_page_id = parent_page_id.replace("-", "")
    print_info(f"父页面 ID: {parent_page_id}")
    print_info(f"父页面 URL: https://www.notion.so/{parent_page_id}")

    try:
        from notion_client import Client

        # 初始化 Notion 客户端
        notion = Client(auth=notion_api_key)

        print_success("Notion API 连接成功")

        # 创建三个数据库
        command_center_id = create_command_center_database(notion, parent_page_id)
        calendar_id = create_calendar_events_database(notion, parent_page_id)
        reports_id = create_reports_database(notion, parent_page_id)

        # 检查是否全部成功
        if command_center_id and calendar_id and reports_id:
            print("\n" + "=" * 50)
            print(f"{GREEN}✅ 所有数据库创建成功！{NC}")
            print("=" * 50)

            # 更新 .env 文件
            if update_env_file(
                command_center_id.replace("-", ""),
                calendar_id.replace("-", ""),
                reports_id.replace("-", "")
            ):
                print("\n" + f"{GREEN}配置总结:{NC}")
                print(f"  1. 指令中心: {command_center_id}")
                print(f"  2. 日历事件: {calendar_id}")
                print(f"  3. 工作报告: {reports_id}")

                print(f"\n{YELLOW}下一步:{NC}")
                print("  1. 在 Notion 中打开这些数据库")
                print("  2. 将 Integration 分享给每个数据库")
                print("     (点击数据库右上角 '...' → 'Add connections')")
                print("  3. 运行配置检查: ./scripts/check-config.sh")
                print("  4. 测试 API 连接: python scripts/test-api-connections.py")
                sys.exit(0)
        else:
            print_error("\n部分数据库创建失败")
            sys.exit(1)

    except ImportError:
        print_error("notion-client 未安装")
        print_info("安装: pip install notion-client")
        sys.exit(1)
    except Exception as e:
        print_error(f"执行失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
