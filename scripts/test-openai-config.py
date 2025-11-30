#!/usr/bin/env python3
"""
测试 OpenAI 配置
"""

import os
import sys
import asyncio
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


async def test_openai_config():
    """测试 OpenAI 配置"""

    print(f"{YELLOW}AILMA OpenAI 配置测试{NC}")
    print("=" * 60)
    print()

    # 1. 检查环境变量
    print_info("检查环境变量...")

    openai_key = os.getenv("OPENAI_API_KEY")
    llm_provider = os.getenv("LLM_PROVIDER")
    llm_model = os.getenv("LLM_MODEL")

    if not openai_key or openai_key == "your_new_openai_key_here":
        print_error("OPENAI_API_KEY 未配置")
        print()
        print("请运行: ./scripts/configure-openai.sh")
        return False

    if llm_provider != "openai":
        print_error(f"LLM_PROVIDER 设置为 '{llm_provider}'，应该是 'openai'")
        return False

    print_success(f"LLM Provider: {llm_provider}")
    print_success(f"Model: {llm_model}")
    print_success(f"API Key: {openai_key[:10]}...{openai_key[-4:]}")
    print()

    # 2. 测试 OpenAI 客户端导入
    print_info("测试 OpenAI 客户端...")

    try:
        from src.ai.clients.openai_client import OpenAIClient

        client = OpenAIClient()
        print_success("OpenAI 客户端初始化成功")
    except Exception as e:
        print_error(f"客户端初始化失败: {str(e)}")
        return False

    print()

    # 3. 测试 AI 客户端工厂
    print_info("测试 AI 客户端工厂...")

    try:
        from src.ai.clients.factory import AIClientFactory

        ai_client = AIClientFactory.create()
        print_success(f"工厂创建客户端: {type(ai_client).__name__}")
    except Exception as e:
        print_error(f"工厂创建失败: {str(e)}")
        return False

    print()

    # 4. 测试 API 调用
    print_info("测试 OpenAI API 调用...")

    try:
        response = await client.complete(
            prompt="请用一句话介绍 AILMA 项目",
            max_tokens=50,
            temperature=0.7,
        )

        print_success("API 调用成功")
        print(f"{BLUE}响应:{NC} {response[:100]}...")
    except Exception as e:
        print_error(f"API 调用失败: {str(e)}")
        print()
        print("可能的原因:")
        print("  1. API Key 无效")
        print("  2. OpenAI 账户余额不足")
        print("  3. 网络连接问题")
        print("  4. API Key 权限不足")
        return False

    print()

    # 5. 测试 JSON 模式
    print_info("测试 JSON 解析...")

    try:
        json_response = await client.complete_json(
            prompt='请返回 JSON: {"status": "ok", "message": "测试成功"}',
            max_tokens=50,
        )

        print_success("JSON 解析成功")
        print(f"{BLUE}JSON 响应:{NC} {json_response}")
    except Exception as e:
        print_error(f"JSON 解析失败: {str(e)}")
        # JSON 模式失败不是致命问题
        print(f"{YELLOW}⚠️  JSON 模式测试失败，但基础功能正常{NC}")

    print()
    print("=" * 60)
    print_success("OpenAI 配置测试通过！")
    print()
    print("下一步:")
    print("  1. 验证 Notion 数据库: python scripts/verify-raw-api.py")
    print("  2. 测试完整配置: ./scripts/check-config.sh")
    print("  3. 启动 AILMA: python -m src.main")

    return True


async def main():
    try:
        success = await test_openai_config()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print()
        print_error("测试中断")
        sys.exit(1)
    except Exception as e:
        print()
        print_error(f"未预期的错误: {str(e)}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
