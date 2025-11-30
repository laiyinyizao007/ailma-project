#!/usr/bin/env python3
"""
自动配置所有 Notion 数据库属性

使用原始 HTTP API 来添加属性，避免 notion-client 库的问题
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


def configure_command_center(api_key, db_id):
    """配置指令中心数据库"""

    print(f"\n{BLUE}配置数据库: 📋 指令中心{NC}")
    print("-" * 60)

    url = f"https://api.notion.com/v1/databases/{db_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    data = {
        "properties": {
            "Name": {
                "name": "指令",
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

    try:
        response = requests.patch(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            properties = result.get("properties", {})
            print_success(f"指令中心配置成功 ({len(properties)} 个属性)")
            return True
        else:
            print_error(f"配置失败: {response.status_code}")
            print(f"错误: {response.text}")
            return False

    except Exception as e:
        print_error(f"异常: {str(e)}")
        return False


def configure_calendar(api_key, db_id):
    """配置日历事件数据库"""

    print(f"\n{BLUE}配置数据库: 📅 日历事件{NC}")
    print("-" * 60)

    url = f"https://api.notion.com/v1/databases/{db_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    data = {
        "properties": {
            "Name": {
                "name": "事件标题",
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
    }

    try:
        response = requests.patch(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            properties = result.get("properties", {})
            print_success(f"日历事件配置成功 ({len(properties)} 个属性)")
            return True
        else:
            print_error(f"配置失败: {response.status_code}")
            print(f"错误: {response.text}")
            return False

    except Exception as e:
        print_error(f"异常: {str(e)}")
        return False


def configure_reports(api_key, db_id):
    """配置工作报告数据库"""

    print(f"\n{BLUE}配置数据库: 📊 工作报告{NC}")
    print("-" * 60)

    url = f"https://api.notion.com/v1/databases/{db_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    data = {
        "properties": {
            "Name": {
                "name": "报告标题",
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
    }

    try:
        response = requests.patch(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            properties = result.get("properties", {})
            print_success(f"工作报告配置成功 ({len(properties)} 个属性)")
            return True
        else:
            print_error(f"配置失败: {response.status_code}")
            print(f"错误: {response.text}")
            return False

    except Exception as e:
        print_error(f"异常: {str(e)}")
        return False


def main():
    print(f"{YELLOW}AILMA Notion 数据库自动配置工具{NC}")
    print("=" * 60)

    # 检查环境变量
    api_key = os.getenv("NOTION_API_KEY")
    command_center_id = os.getenv("COMMAND_CENTER_DB_ID")
    calendar_id = os.getenv("CALENDAR_DB_ID")
    reports_id = os.getenv("REPORTS_DB_ID")

    if not all([api_key, command_center_id, calendar_id, reports_id]):
        print_error("缺少必要的环境变量")
        print()
        print("请确保 .env 文件包含:")
        print("  - NOTION_API_KEY")
        print("  - COMMAND_CENTER_DB_ID")
        print("  - CALENDAR_DB_ID")
        print("  - REPORTS_DB_ID")
        sys.exit(1)

    print_success("环境变量检查通过")

    # 配置三个数据库
    results = []
    results.append(configure_command_center(api_key, command_center_id))
    results.append(configure_calendar(api_key, calendar_id))
    results.append(configure_reports(api_key, reports_id))

    print("\n" + "=" * 60)

    if all(results):
        print_success("所有数据库配置成功！")
        print()
        print("下一步:")
        print("  1. 运行验证: python scripts/verify-notion-databases.py")
        print("  2. 在 Notion 中查看数据库")
        print("  3. 配置 Claude API Key")
        print("  4. 测试连接: python scripts/test-api-connections.py")
        sys.exit(0)
    else:
        print_error("部分数据库配置失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
