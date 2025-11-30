"""
应用配置管理
从环境变量加载配置
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""

    # Notion 配置
    notion_api_key: str = "test_key"
    notion_workspace_id: Optional[str] = None
    command_center_db_id: str = "test_db_id"
    calendar_db_id: str = "test_calendar_id"
    reports_db_id: str = "test_reports_id"
    notion_mcp_server_url: str = "https://mcp.notion.com/mcp"

    # LLM 配置
    llm_provider: str = "openai"  # "openai" 或 "claude"

    # Claude API 配置
    anthropic_api_key: str = "test_anthropic_key"

    # OpenAI API 配置
    openai_api_key: str = "test_openai_key"
    openai_base_url: Optional[str] = None  # 自定义 API endpoint (用于代理服务)

    # 模型配置 (根据 provider 自动选择)
    llm_model: str = "gpt-4o-mini"  # OpenAI: gpt-4o-mini, gpt-4o; Claude: claude-3-sonnet-20240229

    # Google Calendar 配置
    google_calendar_mcp_server_url: str = "http://localhost:3000/mcp"
    google_client_id: str = "test_client_id"
    google_client_secret: str = "test_client_secret"
    google_calendar_oauth_token: Optional[str] = None
    google_calendar_default_id: str = "primary"
    google_calendar_timezone: str = "Asia/Shanghai"

    # 数据库配置
    database_url: str = "postgresql://ailma:password@localhost:5432/ailma"
    redis_url: str = "redis://localhost:6379/0"

    # 安全配置
    secret_key: str = "test_secret_key"
    encryption_key: str = "test_encryption_key"

    # 应用配置
    debug: bool = False
    environment: str = "production"
    poll_interval_seconds: int = 30
    max_workers: int = 4
    port: int = 8000

    # 日志配置
    log_level: str = "INFO"
    log_format: str = "json"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


# 全局配置实例
settings = Settings()
