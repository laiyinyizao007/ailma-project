#!/usr/bin/env python3
"""
直接使用 Notion HTTP API 测试数据库更新

参考文档: https://developers.notion.com/reference/database-update
"""

import os
import sys
import json
import requests
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


def print_info(message):
    print(f"{BLUE}ℹ️  {message}{NC}")


def test_raw_api_update():
    """使用原始 HTTP API 更新数据库"""

    notion_api_key = os.getenv("NOTION_API_KEY")
    command_center_id = os.getenv("COMMAND_CENTER_DB_ID")

    if not all([notion_api_key, command_center_id]):
        print_error("缺少必要的环境变量")
        return False

    # Notion API endpoint
    url = f"https://api.notion.com/v1/databases/{command_center_id}"

    # Headers according to official docs
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"  # 使用官方推荐的稳定版本
    }

    # Request body - 按官方文档格式构造
    # 注意:
    # 1. 数据库已有默认的 "Name" title 属性，需要重命名而不是创建新的
    # 2. 使用 name 字段来重命名现有属性
    data = {
        "properties": {
            "Name": {
                "name": "指令",  # 重命名现有的 Name 属性为 "指令"
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
    }

    print(f"{YELLOW}=== 测试直接 HTTP API 调用 ==={NC}\n")
    print_info(f"数据库 ID: {command_center_id}")
    print_info(f"API Version: {headers['Notion-Version']}")
    print()

    print(f"{BLUE}请求 URL:{NC}")
    print(url)
    print()

    print(f"{BLUE}请求头:{NC}")
    print(json.dumps({k: v if k != "Authorization" else "Bearer ***" for k, v in headers.items()}, indent=2))
    print()

    print(f"{BLUE}请求体:{NC}")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print()

    # 发送 PATCH 请求
    print_info("发送 PATCH 请求...")
    try:
        response = requests.patch(url, headers=headers, json=data)

        print()
        print(f"{BLUE}响应状态码:{NC} {response.status_code}")
        print()

        if response.status_code == 200:
            print_success("API 调用成功")
            print()

            result = response.json()
            print(f"{BLUE}响应内容:{NC}")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print()

            # 检查 properties
            properties = result.get("properties", {})
            print(f"{BLUE}返回的属性数量:{NC} {len(properties)}")

            if properties:
                print(f"{GREEN}返回的属性列表:{NC}")
                for prop_name, prop_data in properties.items():
                    prop_type = prop_data.get("type", "unknown")
                    print(f"  - {prop_name}: {prop_type}")

                    # 如果是 select，显示选项
                    if prop_type == "select":
                        options = prop_data.get("select", {}).get("options", [])
                        print(f"    选项数量: {len(options)}")
                        for opt in options:
                            print(f"      • {opt.get('name')} ({opt.get('color')})")

                return True
            else:
                print_error("响应中没有 properties 字段或为空")
                return False

        else:
            print_error(f"API 调用失败: {response.status_code}")
            print()
            print(f"{RED}错误响应:{NC}")
            print(response.text)
            return False

    except Exception as e:
        print_error(f"请求异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def verify_database():
    """验证数据库当前状态"""

    notion_api_key = os.getenv("NOTION_API_KEY")
    command_center_id = os.getenv("COMMAND_CENTER_DB_ID")

    url = f"https://api.notion.com/v1/databases/{command_center_id}"

    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Notion-Version": "2022-06-28"
    }

    print(f"\n{YELLOW}=== 验证数据库当前状态 ==={NC}\n")

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            result = response.json()
            properties = result.get("properties", {})

            print_info(f"当前属性数量: {len(properties)}")

            if properties:
                print(f"{GREEN}当前属性列表:{NC}")
                for prop_name, prop_data in properties.items():
                    prop_type = prop_data.get("type", "unknown")
                    print(f"  ✅ {prop_name}: {prop_type}")
            else:
                print_error("数据库没有任何属性")

            return len(properties) > 0
        else:
            print_error(f"获取数据库失败: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"验证异常: {str(e)}")
        return False


def main():
    print(f"{YELLOW}Notion 原始 API 测试工具{NC}")
    print("=" * 60)
    print()

    # 先验证当前状态
    print(f"{BLUE}步骤 1: 检查数据库当前状态{NC}")
    verify_database()

    print("\n" + "=" * 60 + "\n")

    # 测试更新 API
    print(f"{BLUE}步骤 2: 测试 HTTP API 更新{NC}")
    success = test_raw_api_update()

    print("\n" + "=" * 60 + "\n")

    # 再次验证
    print(f"{BLUE}步骤 3: 再次验证数据库状态{NC}")
    has_properties = verify_database()

    print("\n" + "=" * 60)

    if success and has_properties:
        print_success("测试成功！属性已成功添加")
        print()
        print("结论: notion-client 库可能存在问题，原始 API 可以正常工作")
    elif success and not has_properties:
        print_error("API 返回成功但属性未实际添加")
        print()
        print("结论: 可能是 Notion API 的延迟或缓存问题")
    else:
        print_error("原始 API 也无法添加属性")
        print()
        print("结论: 可能是 API Key 权限或数据库配置问题")


if __name__ == "__main__":
    main()
