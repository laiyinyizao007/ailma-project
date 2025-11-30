"""
任务解析器 - 组合意图分类和实体提取
"""

from dataclasses import dataclass
from src.ai.models.intent import IntentResult
from src.ai.models.entity import ExtractedEntities
from src.ai.classifiers.intent_classifier import IntentClassifier
from src.ai.extractors.entity_extractor import EntityExtractor


@dataclass
class ParseResult:
    """解析结果"""

    intent: IntentResult
    entities: ExtractedEntities
    raw_input: str

    def is_valid(self) -> bool:
        """判断解析结果是否有效"""
        return self.intent.is_confident() and self.intent.type.value != "unknown"

    def needs_clarification(self) -> bool:
        """判断是否需要澄清"""
        return not self.intent.is_confident()


class TaskParser:
    """任务解析器 - AI 核心组件"""

    def __init__(
        self, intent_classifier: IntentClassifier, entity_extractor: EntityExtractor
    ):
        self.intent_classifier = intent_classifier
        self.entity_extractor = entity_extractor

    async def parse(self, user_input: str) -> ParseResult:
        """
        解析用户输入

        Args:
            user_input: 用户自然语言输入

        Returns:
            解析结果 (意图 + 实体)
        """
        # Step 1: 意图分类
        intent = await self.intent_classifier.classify(user_input)

        # Step 2: 实体提取
        entities = await self.entity_extractor.extract(user_input, intent.type)

        return ParseResult(intent=intent, entities=entities, raw_input=user_input)
