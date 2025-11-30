"""
实体模型定义
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class TimeEntity:
    """时间实体"""

    start: datetime
    end: Optional[datetime] = None
    is_all_day: bool = False
    recurrence: Optional[str] = None  # RRULE format
    timezone: str = "Asia/Shanghai"


@dataclass
class LocationEntity:
    """地点实体"""

    name: str
    address: Optional[str] = None
    url: Optional[str] = None


@dataclass
class PersonEntity:
    """人员实体"""

    name: str
    email: Optional[str] = None


@dataclass
class ExtractedEntities:
    """提取的所有实体"""

    title: Optional[str] = None
    description: Optional[str] = None
    time: Optional[TimeEntity] = None
    location: Optional[LocationEntity] = None
    participants: List[PersonEntity] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    priority: Optional[str] = None  # high, medium, low
    metadata: dict = field(default_factory=dict)
