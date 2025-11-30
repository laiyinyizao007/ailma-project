"""
OpenAI API 客户端 (替代 Claude)
"""

from openai import AsyncOpenAI, RateLimitError, AuthenticationError
from typing import Optional, Dict, Any
import asyncio
from functools import wraps
import json

from src.config import settings


def retry_on_rate_limit(max_retries: int = 3):
    """重试装饰器"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except RateLimitError as e:
                    if attempt == max_retries - 1:
                        raise
                    wait_time = 2**attempt  # 指数退避
                    await asyncio.sleep(wait_time)
                except AuthenticationError:
                    raise  # 认证错误不重试
            return None

        return wrapper

    return decorator


class OpenAIClient:
    """OpenAI API 客户端封装"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.llm_model or "gpt-4o-mini"  # 默认使用 gpt-4o-mini (便宜且快)

        # 初始化 OpenAI 客户端 (新版 API)
        self.client = AsyncOpenAI(api_key=self.api_key)

    @retry_on_rate_limit(max_retries=3)
    async def complete(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        system: Optional[str] = None,
    ) -> str:
        """
        调用 OpenAI API 生成文本

        Args:
            prompt: 用户提示
            max_tokens: 最大生成 token 数
            temperature: 温度参数 (0-1)
            system: 系统提示

        Returns:
            生成的文本
        """
        try:
            messages = []

            # 添加系统消息
            if system:
                messages.append({"role": "system", "content": system})

            # 添加用户消息
            messages.append({"role": "user", "content": prompt})

            # 调用 OpenAI API (新版 SDK)
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            return response.choices[0].message.content

        except Exception as e:
            raise RuntimeError(f"OpenAI API 调用失败: {str(e)}")

    async def complete_json(
        self, prompt: str, max_tokens: int = 1024, system: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        调用 OpenAI API 并解析 JSON 响应

        Args:
            prompt: 用户提示
            max_tokens: 最大生成 token 数
            system: 系统提示

        Returns:
            解析后的 JSON 对象
        """
        # 添加 JSON 格式提示
        json_system = (system or "") + "\n\n请以有效的 JSON 格式返回结果，不要包含任何其他文本。"

        response = await self.complete(
            prompt=prompt, max_tokens=max_tokens, temperature=0, system=json_system
        )

        # 尝试提取 JSON (处理可能的 markdown 代码块)
        response_text = response.strip()

        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"无法解析 JSON 响应: {str(e)}\n原始响应: {response_text}")
