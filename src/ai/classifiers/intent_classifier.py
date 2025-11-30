"""
意图分类器
"""

from typing import Dict, Any
from functools import lru_cache

from src.ai.models.intent import IntentType, IntentResult
from src.ai.clients.claude import ClaudeClient
from src.ai.prompts.templates import PromptManager


class IntentClassifier:
    """意图分类器"""

    def __init__(
        self,
        claude_client: ClaudeClient,
        prompt_manager: PromptManager,
        confidence_threshold: float = 0.7,
    ):
        self.client = claude_client
        self.prompts = prompt_manager
        self.confidence_threshold = confidence_threshold

    @lru_cache(maxsize=128)
    def _cache_key(self, user_input: str) -> str:
        """生成缓存键"""
        return user_input.strip().lower()

    async def classify(self, user_input: str) -> IntentResult:
        """
        分类用户意图

        Args:
            user_input: 用户输入的自然语言指令

        Returns:
            意图识别结果
        """
        # 生成 prompt
        prompt = self.prompts.get_intent_prompt(user_input)

        # 调用 LLM
        try:
            response = await self.client.complete_json(prompt=prompt, max_tokens=256)

            # 解析响应
            intent_str = response.get("intent", "unknown")
            confidence = float(response.get("confidence", 0.0))
            explanation = response.get("explanation", "")

            # 转换为枚举
            try:
                intent_type = IntentType(intent_str)
            except ValueError:
                intent_type = IntentType.UNKNOWN
                confidence = 0.0

            # 置信度检查
            if confidence < self.confidence_threshold:
                intent_type = IntentType.UNKNOWN

            return IntentResult(
                type=intent_type,
                confidence=confidence,
                raw_input=user_input,
                explanation=explanation,
            )

        except Exception as e:
            # 错误处理：返回 UNKNOWN
            return IntentResult(
                type=IntentType.UNKNOWN,
                confidence=0.0,
                raw_input=user_input,
                explanation=f"分类失败: {str(e)}",
            )

    def is_ambiguous(self, result: IntentResult) -> bool:
        """判断意图是否模糊"""
        return result.confidence < self.confidence_threshold
