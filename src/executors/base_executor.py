"""
任务执行器基类
"""

from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any
from datetime import datetime


class ExecutionStatus(str, Enum):
    """执行状态"""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRY = "retry"


@dataclass
class ExecutionResult:
    """执行结果"""

    status: ExecutionStatus
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def is_success(self) -> bool:
        return self.status == ExecutionStatus.SUCCESS

    def needs_retry(self) -> bool:
        return self.status == ExecutionStatus.RETRY


class BaseExecutor(ABC):
    """执行器基类"""

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    @abstractmethod
    async def execute(self, *args, **kwargs) -> ExecutionResult:
        """执行任务"""
        pass

    async def execute_with_retry(self, *args, **kwargs) -> ExecutionResult:
        """带重试的执行"""
        last_result = None

        for attempt in range(self.max_retries):
            try:
                result = await self.execute(*args, **kwargs)

                if result.is_success():
                    return result

                if not result.needs_retry():
                    return result

                last_result = result

            except Exception as e:
                last_result = ExecutionResult(
                    status=ExecutionStatus.FAILED,
                    message=f"执行失败 (第 {attempt + 1} 次尝试)",
                    error=str(e),
                )

        return last_result or ExecutionResult(
            status=ExecutionStatus.FAILED,
            message="达到最大重试次数",
        )
