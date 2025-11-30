#!/usr/bin/env python3
"""
验证 Notion 数据库结构脚本

检查 3 个数据库的属性配置是否正确
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


def verify_database_properties(notion, db_id, db_name, expected_props):
    """验证数据库的属性"""
    print(f"\n{BLUE}检查数据库: {db_name}{NC}")
    print("-" * 50)

    try:
        database = notion.databases.retrieve(database_id=db_id)
        actual_props = database.get("properties", {})

        print_info(f"数据库 ID: {db_id}")
        print_info(f"实际属性数量: {len(actual_props)}")
        print_info(f"期望属性数量: {len(expected_props)}")
        print()

        missing_props = []
        existing_props = []

        for prop_name, prop_type in expected_props.items():
            if prop_name in actual_props:
                actual_type = actual_props[prop_name]["type"]
                if actual_type == prop_type:
                    print_success(f"{prop_name} ({prop_type})")
                    existing_props.append(prop_name)
                else:
                    print_warning(f"{prop_name} - 类型不匹配: 实际={actual_type}, 期望={prop_type}")
            else:
                print_error(f"{prop_name} ({prop_type}) - 缺失")
                missing_props.append(prop_name)

        if not missing_props:
            print()
            print_success(f"{db_name} 配置正确！")
            return True
        else:
            print()
            print_warning(f"{db_name} 缺少 {len(missing_props)} 个属性")
            return False

    except Exception as e:
        print_error(f"检查失败: {str(e)}")
        return False


def main():
    print(f"{YELLOW}Notion 数据库结构验证工具{NC}")
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

        # 定义期望的属性
        command_center_props = {
            "指令": "title",
            "状态": "select",
            "意图类型": "select",
            "置信度": "number",
            "执行结果": "rich_text",
            "错误信息": "rich_text",
            "创建时间": "created_time",
            "处理时间": "date"
        }

        calendar_props = {
            "事件标题": "title",
            "开始时间": "date",
            "地点": "rich_text",
            "参与者": "multi_select",
            "事件类型": "select",
            "状态": "select",
            "Google Calendar ID": "rich_text",
            "Meet 链接": "url",
            "描述": "rich_text",
            "创建时间": "created_time"
        }

        reports_props = {
            "报告标题": "title",
            "报告类型": "select",
            "时间范围": "date",
            "事件统计": "number",
            "会议时长": "number",
            "生成时间": "created_time",
            "状态": "select",
            "标签": "multi_select"
        }

        # 验证三个数据库
        results = []
        results.append(verify_database_properties(
            notion, command_center_id, "📋 指令中心", command_center_props
        ))
        results.append(verify_database_properties(
            notion, calendar_id, "📅 日历事件", calendar_props
        ))
        results.append(verify_database_properties(
            notion, reports_id, "📊 工作报告", reports_props
        ))

        print("\n" + "=" * 50)
        if all(results):
            print_success("所有数据库配置正确！")
            print()
            print("下一步:")
            print("  1. 配置 Claude API Key")
            print("  2. 运行: ./scripts/check-config.sh")
            print("  3. 运行: python scripts/test-api-connections.py")
            sys.exit(0)
        else:
            print_warning("部分数据库配置不正确")
            print()
            print("建议:")
            print("  1. 查看手动配置指南: docs/integrations/notion/manual-setup.md")
            print("  2. 或删除数据库并重新运行创建脚本")
            sys.exit(1)

    except ImportError:
        print_error("notion-client 未安装")
        sys.exit(1)
    except Exception as e:
        print_error(f"验证失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
