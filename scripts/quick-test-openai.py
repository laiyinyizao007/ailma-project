#!/usr/bin/env python3
"""
快速测试 OpenAI API 连接
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


def main():
    print(f"{YELLOW}OpenAI API 快速测试{NC}")
    print("=" * 60)
    print()

    # 检查环境变量
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    if not api_key or api_key == "your_new_openai_key_here":
        print(f"{RED}❌ OPENAI_API_KEY 未配置{NC}")
        sys.exit(1)

    print(f"{BLUE}ℹ️  API Key: {api_key[:10]}...{api_key[-4:]}{NC}")
    print(f"{BLUE}ℹ️  Model: {model}{NC}")
    print()

    # 测试 OpenAI API
    print(f"{BLUE}ℹ️  测试 OpenAI API 连接...{NC}")

    try:
        from openai import OpenAI, AuthenticationError

        client = OpenAI(api_key=api_key)

        # 简单测试
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "请用一句话介绍 AILMA 项目"}],
            max_tokens=100,
        )

        print(f"{GREEN}✅ OpenAI API 连接成功！{NC}")
        print()
        print(f"{BLUE}响应:{NC}")
        print(response.choices[0].message.content)
        print()
        print("=" * 60)
        print(f"{GREEN}✅ 配置测试通过！{NC}")
        print()
        print("下一步:")
        print("  1. 验证 Notion 数据库: python scripts/verify-raw-api.py")
        print("  2. 启动 AILMA: PYTHONPATH=. python -m src.main")

    except AuthenticationError:
        print(f"{RED}❌ API Key 无效{NC}")
        print()
        print("请检查:")
        print("  1. API Key 是否正确")
        print("  2. 密钥是否已撤销")
        print("  3. 前往 https://platform.openai.com/api-keys 检查")
        sys.exit(1)

    except Exception as e:
        print(f"{RED}❌ 连接失败: {str(e)}{NC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
