"""
时间解析器测试
"""

import pytest
from datetime import datetime, timedelta

from src.ai.parsers.time_parser import TimeParser


def test_parse_relative_dates():
    """测试相对日期解析"""
    parser = TimeParser()
    reference = datetime(2025, 11, 27, 10, 0, 0)  # 周三 10:00

    # 今天下午3点 (应该是15点)
    result = parser.parse("今天下午3点", reference)
    assert result.day == 27
    assert result.hour == 15  # 下午3点 = 15:00

    # 明天
    result = parser.parse("明天早上9点", reference)
    assert result.day == 28
    assert result.hour == 9

    # 后天
    result = parser.parse("后天", reference)
    assert result.day == 29


def test_parse_weekdays():
    """测试星期解析"""
    parser = TimeParser()
    reference = datetime(2025, 11, 27, 10, 0, 0)  # 周三

    # 下周一
    result = parser.parse("下周一", reference)
    assert result.weekday() == 0  # 周一
    assert result > reference + timedelta(days=7)

    # 本周五
    result = parser.parse("本周五", reference)
    assert result.weekday() == 4  # 周五
    assert result.day == 28


def test_parse_fuzzy_time():
    """测试模糊时间"""
    parser = TimeParser()
    reference = datetime(2025, 11, 27, 0, 0, 0)

    # 早上
    result = parser.parse("早上", reference)
    assert result.hour == 8

    # 下午
    result = parser.parse("下午", reference)
    assert result.hour == 15

    # 晚上
    result = parser.parse("晚上", reference)
    assert result.hour == 19


def test_parse_duration():
    """测试持续时间解析"""
    parser = TimeParser()

    # 1小时
    duration = parser.parse_duration("1小时")
    assert duration == timedelta(hours=1)

    # 30分钟
    duration = parser.parse_duration("30分钟")
    assert duration == timedelta(minutes=30)

    # 半天
    duration = parser.parse_duration("半天")
    assert duration == timedelta(hours=4)

    # 全天
    duration = parser.parse_duration("全天")
    assert duration == timedelta(hours=24)


def test_extract_time_of_day():
    """测试提取具体时间"""
    parser = TimeParser()
    base = datetime(2025, 11, 27, 0, 0, 0)

    # 3点
    result = parser._extract_time_of_day("3点", base)
    assert result.hour == 3

    # 15点30分
    result = parser._extract_time_of_day("15点30分", base)
    assert result.hour == 15
    assert result.minute == 30
