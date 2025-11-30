"""
AI 客户端工厂
根据配置自动选择 OpenAI 或 Claude
"""

from typing import Union
from src.config import settings


class AIClientFactory:
    """AI 客户端工厂"""

    @staticmethod
    def create():
        """
        根据配置创建 AI 客户端

        Returns:
            OpenAIClient 或 ClaudeClient 实例
        """
        provider = settings.llm_provider.lower()

        if provider == "openai":
            from src.ai.clients.openai_client import OpenAIClient

            return OpenAIClient(
                api_key=settings.openai_api_key, model=settings.llm_model
            )

        elif provider == "claude":
            from src.ai.clients.claude import ClaudeClient

            return ClaudeClient(
                api_key=settings.anthropic_api_key, model=settings.llm_model
            )

        else:
            raise ValueError(
                f"不支持的 LLM provider: {provider}. 请使用 'openai' 或 'claude'"
            )

    @staticmethod
    def get_recommended_model(provider: str) -> str:
        """
        获取推荐的模型

        Args:
            provider: LLM provider ("openai" 或 "claude")

        Returns:
            推荐的模型名称
        """
        recommendations = {
            "openai": {
                "fast": "gpt-4o-mini",  # 快速且便宜，适合日常使用
                "balanced": "gpt-4o",  # 平衡性能和成本
                "powerful": "gpt-4-turbo",  # 最强性能
            },
            "claude": {
                "fast": "claude-3-haiku-20240307",  # 最快
                "balanced": "claude-3-sonnet-20240229",  # 平衡
                "powerful": "claude-3-opus-20240229",  # 最强
            },
        }

        if provider not in recommendations:
            raise ValueError(f"未知的 provider: {provider}")

        return recommendations[provider]["fast"]  # 默认返回快速模型
