#!/usr/bin/env python3
"""
使用原始 HTTP API 验证数据库配置
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

# Colors
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'


def check_database(api_key, db_id, db_name):
    """检查数据库属性"""

    url = f"https://api.notion.com/v1/databases/{db_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            result = response.json()
            properties = result.get("properties", {})

            print(f"\n{BLUE}数据库: {db_name}{NC}")
            print("-" * 60)
            print(f"{BLUE}属性数量: {len(properties)}{NC}")

            if properties:
                print(f"{GREEN}属性列表:{NC}")
                for prop_name, prop_data in sorted(properties.items()):
                    prop_type = prop_data.get("type", "unknown")
                    print(f"  ✅ {prop_name}: {prop_type}")

                    # 显示 select 选项
                    if prop_type == "select":
                        options = prop_data.get("select", {}).get("options", [])
                        if options:
                            print(f"     选项: {', '.join([opt['name'] for opt in options])}")

                    # 显示 multi_select 选项
                    elif prop_type == "multi_select":
                        options = prop_data.get("multi_select", {}).get("options", [])
                        if options:
                            print(f"     选项: {', '.join([opt['name'] for opt in options])}")

                return len(properties)
            else:
                print(f"{RED}❌ 没有属性{NC}")
                return 0

        else:
            print(f"{RED}❌ 获取失败: {response.status_code}{NC}")
            return 0

    except Exception as e:
        print(f"{RED}❌ 异常: {str(e)}{NC}")
        return 0


def main():
    print(f"{YELLOW}Notion 数据库验证工具 (原始 API){NC}")
    print("=" * 60)

    api_key = os.getenv("NOTION_API_KEY")
    command_center_id = os.getenv("COMMAND_CENTER_DB_ID")
    calendar_id = os.getenv("CALENDAR_DB_ID")
    reports_id = os.getenv("REPORTS_DB_ID")

    if not all([api_key, command_center_id, calendar_id, reports_id]):
        print(f"{RED}❌ 缺少环境变量{NC}")
        sys.exit(1)

    # 检查三个数据库
    count1 = check_database(api_key, command_center_id, "📋 指令中心")
    count2 = check_database(api_key, calendar_id, "📅 日历事件")
    count3 = check_database(api_key, reports_id, "📊 工作报告")

    print("\n" + "=" * 60)
    print(f"\n{BLUE}配置总结:{NC}")
    print(f"  📋 指令中心: {count1} 个属性 (期望 8)")
    print(f"  📅 日历事件: {count2} 个属性 (期望 10)")
    print(f"  📊 工作报告: {count3} 个属性 (期望 8)")

    if count1 == 8 and count2 == 10 and count3 == 8:
        print(f"\n{GREEN}✅ 所有数据库配置正确！{NC}")
        sys.exit(0)
    else:
        print(f"\n{YELLOW}⚠️  部分数据库配置不完整{NC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
