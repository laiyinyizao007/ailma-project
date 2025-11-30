"""
意图分类器测试
"""

import pytest
from unittest.mock import Mock, AsyncMock

from src.ai.classifiers.intent_classifier import IntentClassifier
from src.ai.models.intent import IntentType


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_input,expected_intent",
    [
        ("明天下午3点开会", IntentType.CALENDAR_CREATE),
        ("我下周有什么安排", IntentType.CALENDAR_QUERY),
        ("取消明天的会议", IntentType.CALENDAR_DELETE),
        ("把周五的会改到周六", IntentType.CALENDAR_UPDATE),
        ("生成本周工作总结", IntentType.GENERATE_REPORT),
        ("记录今天的想法", IntentType.NOTION_CREATE_PAGE),
        ("创建待办：买菜", IntentType.NOTION_CREATE_TODO),
    ],
)
async def test_intent_classification(user_input, expected_intent):
    """测试意图分类"""
    # Mock Claude 客户端
    mock_client = Mock()
    mock_client.complete_json = AsyncMock(
        return_value={"intent": expected_intent.value, "confidence": 0.95, "explanation": "测试"}
    )

    # Mock Prompt Manager
    mock_prompt_manager = Mock()
    mock_prompt_manager.get_intent_prompt = Mock(return_value="test prompt")

    # 创建分类器
    classifier = IntentClassifier(mock_client, mock_prompt_manager)

    # 执行分类
    result = await classifier.classify(user_input)

    # 断言
    assert result.type == expected_intent
    assert result.confidence >= 0.7
    assert result.is_confident()


@pytest.mark.asyncio
async def test_low_confidence_returns_unknown():
    """测试低置信度返回 UNKNOWN"""
    mock_client = Mock()
    mock_client.complete_json = AsyncMock(
        return_value={"intent": "calendar_create", "confidence": 0.3, "explanation": "不确定"}
    )

    mock_prompt_manager = Mock()
    mock_prompt_manager.get_intent_prompt = Mock(return_value="test prompt")

    classifier = IntentClassifier(mock_client, mock_prompt_manager, confidence_threshold=0.7)

    result = await classifier.classify("不清楚的指令")

    assert result.type == IntentType.UNKNOWN
    assert not result.is_confident()


@pytest.mark.asyncio
async def test_invalid_intent_returns_unknown():
    """测试无效意图返回 UNKNOWN"""
    mock_client = Mock()
    mock_client.complete_json = AsyncMock(
        return_value={"intent": "invalid_intent", "confidence": 0.95, "explanation": "无效"}
    )

    mock_prompt_manager = Mock()
    mock_prompt_manager.get_intent_prompt = Mock(return_value="test prompt")

    classifier = IntentClassifier(mock_client, mock_prompt_manager)

    result = await classifier.classify("测试输入")

    assert result.type == IntentType.UNKNOWN
