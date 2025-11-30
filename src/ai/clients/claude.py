"""
Claude API 客户端
"""

import anthropic
from typing import Optional, Dict, Any
import asyncio
from functools import wraps

from src.config import settings


def retry_on_rate_limit(max_retries: int = 3):
    """重试装饰器"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except anthropic.RateLimitError as e:
                    if attempt == max_retries - 1:
                        raise
                    wait_time = 2**attempt  # 指数退避
                    await asyncio.sleep(wait_time)
                except anthropic.AuthenticationError:
                    raise  # 认证错误不重试
            return None

        return wrapper

    return decorator


class ClaudeClient:
    """Claude API 客户端封装"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.anthropic_api_key
        self.model = model or settings.llm_model
        self.client = anthropic.Anthropic(api_key=self.api_key)

    @retry_on_rate_limit(max_retries=3)
    async def complete(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        system: Optional[str] = None,
    ) -> str:
        """
        调用 Claude API 生成文本

        Args:
            prompt: 用户提示
            max_tokens: 最大生成 token 数
            temperature: 温度参数 (0-1)
            system: 系统提示

        Returns:
            生成的文本
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system if system else None,
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text
        except Exception as e:
            raise RuntimeError(f"Claude API 调用失败: {str(e)}")

    async def complete_json(
        self, prompt: str, max_tokens: int = 1024, system: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        调用 Claude API 并解析 JSON 响应

        Args:
            prompt: 用户提示
            max_tokens: 最大生成 token 数
            system: 系统提示

        Returns:
            解析后的 JSON 对象
        """
        import json

        response = await self.complete(
            prompt=prompt, max_tokens=max_tokens, temperature=0, system=system
        )

        # 尝试提取 JSON (处理可能的 markdown 代码块)
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()

        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"无法解析 JSON 响应: {str(e)}\n原始响应: {response}")
