#!/usr/bin/env python3
"""
AILMA API 连接测试脚本

测试所有配置的 API Keys 是否有效
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Colors for terminal output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No Color


def print_success(message):
    print(f"{GREEN}✅ {message}{NC}")


def print_error(message):
    print(f"{RED}❌ {message}{NC}")


def print_warning(message):
    print(f"{YELLOW}⚠️  {message}{NC}")


def test_notion_api():
    """测试 Notion API 连接"""
    print("\n测试 Notion API...")
    print("-" * 50)

    api_key = os.getenv("NOTION_API_KEY")

    if not api_key or api_key == "secret_your_notion_integration_token_here":
        print_error("NOTION_API_KEY 未配置")
        return False

    try:
        # 使用 httpx 测试（避免依赖 notion-client）
        import httpx

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

        response = httpx.get(
            "https://api.notion.com/v1/users/me",
            headers=headers,
            timeout=10.0
        )

        if response.status_code == 200:
            user_data = response.json()
            user_type = user_data.get("type", "unknown")
            print_success(f"Notion API 连接成功")
            print(f"   用户类型: {user_type}")
            return True
        else:
            print_error(f"Notion API 返回错误: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False

    except ImportError:
        print_warning("httpx 未安装，跳过 Notion API 测试")
        print("   安装: pip install httpx")
        return None
    except Exception as e:
        print_error(f"Notion API 连接失败: {str(e)}")
        return False


def test_claude_api():
    """测试 Claude API 连接"""
    print("\n测试 Claude API...")
    print("-" * 50)

    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key or api_key == "sk-ant-your_api_key_here":
        print_error("ANTHROPIC_API_KEY 未配置")
        return False

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)

        # 发送最小测试请求
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=10,
            messages=[{"role": "user", "content": "test"}]
        )

        if response.content:
            print_success("Claude API 连接成功")
            print(f"   模型: {response.model}")
            print(f"   Token 使用: {response.usage.input_tokens} 输入 + {response.usage.output_tokens} 输出")
            return True
        else:
            print_error("Claude API 返回空响应")
            return False

    except ImportError:
        print_warning("anthropic 未安装，跳过 Claude API 测试")
        print("   安装: pip install anthropic")
        return None
    except Exception as e:
        print_error(f"Claude API 连接失败: {str(e)}")
        return False


def test_database_connection():
    """测试数据库连接"""
    print("\n测试数据库连接...")
    print("-" * 50)

    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        print_warning("DATABASE_URL 未配置（可选）")
        return None

    try:
        from sqlalchemy import create_engine

        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            if result:
                print_success("数据库连接成功")
                print(f"   URL: {db_url.split('@')[1] if '@' in db_url else db_url}")
                return True

    except ImportError:
        print_warning("sqlalchemy 未安装，跳过数据库测试")
        return None
    except Exception as e:
        print_error(f"数据库连接失败: {str(e)}")
        return False


def test_redis_connection():
    """测试 Redis 连接"""
    print("\n测试 Redis 连接...")
    print("-" * 50)

    redis_url = os.getenv("REDIS_URL")

    if not redis_url:
        print_warning("REDIS_URL 未配置（可选）")
        return None

    try:
        import redis

        r = redis.from_url(redis_url)
        r.ping()

        print_success("Redis 连接成功")
        print(f"   URL: {redis_url}")
        return True

    except ImportError:
        print_warning("redis 未安装，跳过 Redis 测试")
        return None
    except Exception as e:
        print_error(f"Redis 连接失败: {str(e)}")
        return False


def main():
    """主函数"""
    print(f"{YELLOW}AILMA API 连接测试{NC}")
    print("=" * 50)

    results = {
        "notion": test_notion_api(),
        "claude": test_claude_api(),
        "database": test_database_connection(),
        "redis": test_redis_connection(),
    }

    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)

    success_count = sum(1 for v in results.values() if v is True)
    failed_count = sum(1 for v in results.values() if v is False)
    skipped_count = sum(1 for v in results.values() if v is None)

    print(f"\n{GREEN}成功: {success_count}{NC}")
    print(f"{RED}失败: {failed_count}{NC}")
    print(f"{YELLOW}跳过: {skipped_count}{NC}")

    # 检查必需的服务
    required_services = ["notion", "claude"]
    required_failed = any(
        results.get(service) is False
        for service in required_services
    )

    if required_failed:
        print(f"\n{RED}❌ 必需的 API 连接失败{NC}")
        print("\n请检查:")
        if results.get("notion") is False:
            print("  - Notion API Key 是否正确")
            print("  - Notion Integration 是否有正确的权限")
        if results.get("claude") is False:
            print("  - Claude API Key 是否正确")
            print("  - 账户是否有足够的额度")
        print("\n详细配置指南: docs/guides/api-keys-setup.md")
        sys.exit(1)
    else:
        print(f"\n{GREEN}✅ 所有必需的 API 连接正常{NC}")
        print("\n下一步:")
        print("  1. 运行测试: ./scripts/run-tests.sh")
        print("  2. 启动应用: python -m uvicorn src.main:app --reload")
        sys.exit(0)


if __name__ == "__main__":
    main()
