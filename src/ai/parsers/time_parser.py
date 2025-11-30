"""
时间解析器
将自然语言时间表达式转换为 datetime 对象
"""

from datetime import datetime, timedelta
from dateutil import parser as dateutil_parser
from typing import Optional
import re


class TimeParser:
    """时间解析器"""

    # 模糊时间映射 (小时)
    FUZZY_TIME_MAP = {
        "凌晨": 1,
        "早上": 8,
        "上午": 10,
        "中午": 12,
        "午后": 14,
        "下午": 15,
        "傍晚": 17,
        "晚上": 19,
        "深夜": 22,
    }

    # 相对日期映射
    RELATIVE_DAY_MAP = {
        "今天": 0,
        "明天": 1,
        "后天": 2,
        "大后天": 3,
    }

    # 星期映射
    WEEKDAY_MAP = {
        "周一": 0,
        "周二": 1,
        "周三": 2,
        "周四": 3,
        "周五": 4,
        "周六": 5,
        "周日": 6,
        "星期一": 0,
        "星期二": 1,
        "星期三": 2,
        "星期四": 3,
        "星期五": 4,
        "星期六": 5,
        "星期日": 6,
    }

    def parse(
        self, time_str: str, reference: Optional[datetime] = None
    ) -> datetime:
        """
        解析时间字符串

        Args:
            time_str: 时间字符串
            reference: 参考时间 (默认为当前时间)

        Returns:
            解析后的 datetime 对象
        """
        if not time_str:
            return datetime.now()

        reference = reference or datetime.now()

        # 尝试解析相对时间
        result = self._parse_relative_date(time_str, reference)
        if result:
            return result

        # 尝试解析模糊时间
        result = self._parse_fuzzy_time(time_str, reference)
        if result:
            return result

        # 尝试标准日期解析
        try:
            return dateutil_parser.parse(time_str, default=reference)
        except:
            # 失败则返回参考时间
            return reference

    def _parse_relative_date(
        self, time_str: str, reference: datetime
    ) -> Optional[datetime]:
        """解析相对日期 (今天、明天等)"""
        for keyword, days in self.RELATIVE_DAY_MAP.items():
            if keyword in time_str:
                result = reference + timedelta(days=days)
                # 解析时间部分
                result = self._extract_time_of_day(time_str, result)
                return result

        # 解析 "X天后"
        match = re.search(r"(\d+)天后", time_str)
        if match:
            days = int(match.group(1))
            result = reference + timedelta(days=days)
            return self._extract_time_of_day(time_str, result)

        # 解析 "下周X"
        if "下周" in time_str:
            for weekday_name, weekday in self.WEEKDAY_MAP.items():
                if weekday_name in time_str:
                    days_ahead = weekday - reference.weekday()
                    if days_ahead <= 0:
                        days_ahead += 7
                    days_ahead += 7  # 下周
                    result = reference + timedelta(days=days_ahead)
                    return self._extract_time_of_day(time_str, result)

        # 解析 "这周X" / "本周X"
        if "这周" in time_str or "本周" in time_str:
            for weekday_name, weekday in self.WEEKDAY_MAP.items():
                if weekday_name in time_str:
                    days_ahead = weekday - reference.weekday()
                    if days_ahead < 0:
                        days_ahead += 7
                    result = reference + timedelta(days=days_ahead)
                    return self._extract_time_of_day(time_str, result)

        return None

    def _parse_fuzzy_time(
        self, time_str: str, reference: datetime
    ) -> Optional[datetime]:
        """解析模糊时间 (早上、下午等)"""
        for keyword, hour in self.FUZZY_TIME_MAP.items():
            if keyword in time_str:
                return reference.replace(hour=hour, minute=0, second=0, microsecond=0)
        return None

    def _extract_time_of_day(self, time_str: str, base_date: datetime) -> datetime:
        """从字符串中提取具体时间"""
        # 首先检查是否有具体小时 "X点"（优先级最高）
        match = re.search(r"(\d{1,2})点", time_str)
        if match:
            hour = int(match.group(1))
            # 如果有"下午"、"晚上"等关键词，且小时<12，则加12
            if 0 <= hour <= 12:
                for keyword in ["下午", "傍晚", "晚上"]:
                    if keyword in time_str and hour < 12:
                        hour += 12
                        break
            if 0 <= hour <= 23:
                base_date = base_date.replace(hour=hour, minute=0, second=0, microsecond=0)
        else:
            # 没有具体小时，使用模糊时间
            for keyword, hour in self.FUZZY_TIME_MAP.items():
                if keyword in time_str:
                    base_date = base_date.replace(
                        hour=hour, minute=0, second=0, microsecond=0
                    )
                    break

        # 尝试提取分钟 "X点Y分"
        match = re.search(r"(\d{1,2})点(\d{1,2})分?", time_str)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                base_date = base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)

        return base_date

    def parse_duration(self, duration_str: str) -> timedelta:
        """
        解析持续时间

        Args:
            duration_str: 持续时间字符串 (如 "1小时", "30分钟", "半天")

        Returns:
            timedelta 对象
        """
        # 小时
        match = re.search(r"(\d+(?:\.\d+)?)小时", duration_str)
        if match:
            hours = float(match.group(1))
            return timedelta(hours=hours)

        # 分钟
        match = re.search(r"(\d+)分钟?", duration_str)
        if match:
            minutes = int(match.group(1))
            return timedelta(minutes=minutes)

        # 半天
        if "半天" in duration_str:
            return timedelta(hours=4)

        # 全天
        if "全天" in duration_str or "整天" in duration_str:
            return timedelta(hours=24)

        # 默认 1 小时
        return timedelta(hours=1)
