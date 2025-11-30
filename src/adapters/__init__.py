"""
MCP Adapters - 统一的外部服务接口
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime


class BaseAdapter(ABC):
    """适配器基类"""

    @abstractmethod
    async def initialize(self) -> None:
        """初始化适配器"""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """健康检查"""
        pass
