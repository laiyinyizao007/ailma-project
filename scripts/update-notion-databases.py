#!/usr/bin/env python3
"""
AILMA Notion 数据库属性更新脚本

为已存在的数据库添加缺失的属性
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


def update_command_center_properties(notion, db_id):
    """为指令中心数据库添加属性"""
    print(f"\n{BLUE}更新数据库: 📋 指令中心{NC}")
    print("-" * 50)

    try:
        notion.databases.update(
            database_id=db_id,
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
        print_success("指令中心属性添加成功")
        return True
    except Exception as e:
        print_error(f"更新失败: {str(e)}")
        return False


def update_calendar_properties(notion, db_id):
    """为日历事件数据库添加属性"""
    print(f"\n{BLUE}更新数据库: 📅 日历事件{NC}")
    print("-" * 50)

    try:
        notion.databases.update(
            database_id=db_id,
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
        print_success("日历事件属性添加成功")
        return True
    except Exception as e:
        print_error(f"更新失败: {str(e)}")
        return False


def update_reports_properties(notion, db_id):
    """为工作报告数据库添加属性"""
    print(f"\n{BLUE}更新数据库: 📊 工作报告{NC}")
    print("-" * 50)

    try:
        notion.databases.update(
            database_id=db_id,
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
        print_success("工作报告属性添加成功")
        return True
    except Exception as e:
        print_error(f"更新失败: {str(e)}")
        return False


def main():
    """主函数"""
    print(f"{YELLOW}AILMA Notion 数据库属性更新工具{NC}")
    print("=" * 50)

    # 检查 API Key
    notion_api_key = os.getenv("NOTION_API_KEY")
    if not notion_api_key:
        print_error("NOTION_API_KEY 未配置")
        sys.exit(1)

    # 检查数据库 ID
    command_center_id = os.getenv("COMMAND_CENTER_DB_ID")
    calendar_id = os.getenv("CALENDAR_DB_ID")
    reports_id = os.getenv("REPORTS_DB_ID")

    if not all([command_center_id, calendar_id, reports_id]):
        print_error("数据库 ID 未完全配置")
        sys.exit(1)

    try:
        from notion_client import Client

        notion = Client(auth=notion_api_key)
        print_success("Notion API 连接成功")

        # 更新三个数据库
        results = []
        results.append(update_command_center_properties(notion, command_center_id))
        results.append(update_calendar_properties(notion, calendar_id))
        results.append(update_reports_properties(notion, reports_id))

        print("\n" + "=" * 50)
        if all(results):
            print_success("所有数据库属性更新成功！")
            print()
            print("下一步:")
            print("  1. 运行验证脚本: python scripts/verify-notion-databases.py")
            print("  2. 在 Notion 中查看数据库确认字段")
            print("  3. 配置 Claude API Key")
            print("  4. 运行: python scripts/test-api-connections.py")
            sys.exit(0)
        else:
            print_warning("部分数据库更新失败")
            sys.exit(1)

    except ImportError:
        print_error("notion-client 未安装")
        sys.exit(1)
    except Exception as e:
        print_error(f"更新失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
