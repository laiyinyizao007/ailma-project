# AILMA 架构设计 - Notion & Google Calendar MCP 集成方案

**版本**: v3.0
**创建日期**: 2025-11-27
**最后更新**: 2025-11-27
**状态**: **推荐方案** - 使用 MCP 统一集成 Notion 和 Google Calendar

---

## 🎯 核心变更说明

### 为什么使用 Notion MCP？

| 对比项 | 直接 Notion API | Notion MCP | 优势 |
|--------|----------------|-----------|------|
| **集成复杂度** | 需要手写 API 封装代码 | 使用标准化 MCP 协议 | ✅ 降低 50% 代码量 |
| **数据格式** | JSON Blocks（复杂） | Markdown（简洁） | ✅ AI 友好，易处理 |
| **维护成本** | API 变更需手动适配 | MCP 自动兼容 | ✅ 长期稳定 |
| **功能覆盖** | 需逐个实现 | 内置完整工具集 | ✅ 开箱即用 |
| **OAuth 管理** | 需自行实现 | MCP 托管 OAuth | ✅ 安全可靠 |
| **标准化** | 私有实现 | 开放标准 (MCP) | ✅ 生态兼容 |

---

## 🏗️ 新架构设计

### 系统架构图（Notion MCP 版）

```
┌─────────────────────────────────────────────────────────┐
│                   Notion Workspace                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │  📋 指令中心 (Command Center Database)            │  │
│  │  📅 日程视图 (Calendar Database)                  │  │
│  │  📊 报告归档 (Reports Database)                   │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                            ▲
                            │ Notion MCP Protocol
                            │ (Markdown-based, OAuth2)
                            │
┌───────────────────────────▼─────────────────────────────┐
│              Backend Service (Python/FastAPI)           │
│                                                         │
│  ┌────────────────────────────────────────────────┐   │
│  │  🔄 Notion MCP Listener                        │   │
│  │  - 通过 MCP Client 监听 Notion 变更             │   │
│  │  - 使用 Webhook 或轮询模式                      │   │
│  │  - 检测新增指令并触发处理                       │   │
│  └────────────────────────────────────────────────┘   │
│                            │                            │
│                            ▼                            │
│  ┌────────────────────────────────────────────────┐   │
│  │  🧠 AI Core (核心引擎)                         │   │
│  │  ┌──────────────────────────────────────────┐ │   │
│  │  │  Task Parser (任务解析器)                │ │   │
│  │  │  - LLM 意图识别                          │ │   │
│  │  │  - 实体提取                              │ │   │
│  │  └──────────────────────────────────────────┘ │   │
│  │  ┌──────────────────────────────────────────┐ │   │
│  │  │  Task Executor (任务执行器)              │ │   │
│  │  │  - 调度 MCP Tools                        │ │   │
│  │  │  - 错误处理与重试                        │ │   │
│  │  └──────────────────────────────────────────┘ │   │
│  │  ┌──────────────────────────────────────────┐ │   │
│  │  │  Report Generator (报告生成器)           │ │   │
│  │  │  - 数据聚合                              │ │   │
│  │  │  - Markdown 格式输出                     │ │   │
│  │  └──────────────────────────────────────────┘ │   │
│  └────────────────────────────────────────────────┘   │
│                            │                            │
│                            ▼                            │
│  ┌────────────────────────────────────────────────┐   │
│  │  🔌 MCP Integration Layer (MCP 集成层)         │   │
│  │                                                 │   │
│  │  ┌─────────────────────────────────────────┐  │   │
│  │  │  Notion MCP Client                      │  │   │
│  │  │  ─────────────────────                  │  │   │
│  │  │  📋 Available MCP Tools:                │  │   │
│  │  │                                         │  │   │
│  │  │  • search_notion()                      │  │   │
│  │  │    搜索 Notion 工作区内容                │  │   │
│  │  │                                         │  │   │
│  │  │  • create_page()                        │  │   │
│  │  │    创建 Notion 页面（支持 Markdown）     │  │   │
│  │  │                                         │  │   │
│  │  │  • update_page()                        │  │   │
│  │  │    更新页面内容和属性                    │  │   │
│  │  │                                         │  │   │
│  │  │  • query_database()                     │  │   │
│  │  │    查询数据库（支持过滤和排序）          │  │   │
│  │  │                                         │  │   │
│  │  │  • create_database_item()               │  │   │
│  │  │    在数据库中添加新行                    │  │   │
│  │  │                                         │  │   │
│  │  │  • update_database_item()               │  │   │
│  │  │    更新数据库行的属性                    │  │   │
│  │  │                                         │  │   │
│  │  │  • append_blocks()                      │  │   │
│  │  │    向页面追加内容块                      │  │   │
│  │  │                                         │  │   │
│  │  │  • read_page_content()                  │  │   │
│  │  │    读取页面内容（Markdown 格式）         │  │   │
│  │  └─────────────────────────────────────────┘  │   │
│  │                                                 │   │
│  │  ┌─────────────────────────────────────────┐  │   │
│  │  │  Google Calendar MCP Client             │  │   │
│  │  │  ─────────────────────                  │  │   │
│  │  │  📅 Available MCP Tools:                │  │   │
│  │  │                                         │  │   │
│  │  │  • list_events()                        │  │   │
│  │  │    列出日历事件（支持时间范围过滤）      │  │   │
│  │  │                                         │  │   │
│  │  │  • create_event()                       │  │   │
│  │  │    创建新的日历事件                      │  │   │
│  │  │                                         │  │   │
│  │  │  • update_event()                       │  │   │
│  │  │    更新现有事件                          │  │   │
│  │  │                                         │  │   │
│  │  │  • delete_event()                       │  │   │
│  │  │    删除日历事件                          │  │   │
│  │  │                                         │  │   │
│  │  │  • search_events()                      │  │   │
│  │  │    搜索事件（按关键词、时间）            │  │   │
│  │  │                                         │  │   │
│  │  │  • get_free_busy()                      │  │   │
│  │  │    查询空闲/忙碌状态                     │  │   │
│  │  │                                         │  │   │
│  │  │  • list_calendars()                     │  │   │
│  │  │    列出所有日历                          │  │   │
│  │  └─────────────────────────────────────────┘  │   │
│  └────────────────────────────────────────────────┘   │
│                                                         │
│  ┌────────────────────────────────────────────────┐   │
│  │  💾 Database (PostgreSQL)                      │   │
│  │  - 用户配置表 (users)                           │   │
│  │  - MCP 连接配置 (mcp_connections)              │   │
│  │  - 任务日志表 (task_logs)                      │   │
│  │  - 同步状态表 (sync_status)                    │   │
│  └────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
            ┌──────────────────────────────────────────┐
            │  External Services                   │
            │  • Notion MCP Server                 │
            │    (https://mcp.notion.com)          │
            │  • Google Calendar MCP Server        │
            │    (Community MCP Implementation)    │
            │  • Anthropic Claude API              │
            └──────────────────────────────────────┘
```

---

## 📦 Notion MCP 工具详解

### 1. search_notion()
**功能**: 全文搜索 Notion 工作区

```python
# MCP Tool 定义
{
  "name": "search_notion",
  "description": "搜索 Notion 工作区中的页面和数据库",
  "parameters": {
    "query": "string",  # 搜索关键词
    "filter": {
      "object": "page | database",
      "property": "title"
    },
    "sort": {
      "direction": "ascending | descending",
      "timestamp": "last_edited_time"
    }
  }
}

# 使用示例
result = await mcp_client.call_tool(
    "search_notion",
    query="团队会议",
    filter={"object": "page"}
)
# 返回: [{"id": "abc", "title": "团队会议纪要", ...}, ...]
```

---

### 2. create_page()
**功能**: 创建 Notion 页面（支持 Markdown）

```python
# MCP Tool 定义
{
  "name": "create_page",
  "description": "创建新的 Notion 页面",
  "parameters": {
    "parent_id": "string",  # 父页面或数据库 ID
    "title": "string",
    "content": "string",  # **Markdown 格式**
    "icon": "string",  # emoji 或 URL
    "cover": "string"  # 封面图 URL
  }
}

# 使用示例
page = await mcp_client.call_tool(
    "create_page",
    parent_id=REPORTS_DB_ID,
    title="2025-W48 工作总结",
    content="""
# 📊 本周工作总结

## 完成事项
- [x] 完成用户研究
- [x] 发布 v2.0

## 下周计划
- [ ] 客户演示
    """,
    icon="📊"
)
# 返回: {"id": "page_123", "url": "https://notion.so/..."}
```

**优势**:
- ✅ 直接写 Markdown，无需转换为 Notion Blocks
- ✅ AI 生成的内容可无缝写入
- ✅ 支持所有 Markdown 语法（标题、列表、代码块等）

---

### 3. query_database()
**功能**: 查询 Notion 数据库

```python
# MCP Tool 定义
{
  "name": "query_database",
  "description": "查询 Notion 数据库内容",
  "parameters": {
    "database_id": "string",
    "filter": {
      "property": "状态",
      "select": {"equals": "⏳ Pending"}
    },
    "sorts": [
      {
        "property": "创建时间",
        "direction": "descending"
      }
    ]
  }
}

# 使用示例：查询待处理指令
commands = await mcp_client.call_tool(
    "query_database",
    database_id=COMMAND_CENTER_DB_ID,
    filter={
        "property": "状态",
        "select": {"equals": "⏳ Pending"}
    }
)
# 返回: [
#   {
#     "id": "item_1",
#     "properties": {
#       "指令": "生成本周工作报告",
#       "状态": "⏳ Pending"
#     }
#   },
#   ...
# ]
```

---

### 4. update_database_item()
**功能**: 更新数据库行

```python
# 使用示例：更新指令状态
await mcp_client.call_tool(
    "update_database_item",
    database_id=COMMAND_CENTER_DB_ID,
    item_id="item_1",
    properties={
        "状态": {"select": {"name": "✅ Done"}},
        "结果": {"rich_text": [{"text": {"content": "✅ 已成功创建事件"}}]},
        "处理时长": {"number": 2.5}
    }
)
```

---

### 5. read_page_content()
**功能**: 读取页面内容（Markdown 格式）

```python
# 使用示例：读取报告内容
content = await mcp_client.call_tool(
    "read_page_content",
    page_id="page_123"
)
# 返回: Markdown 字符串
"""
# 📊 本周工作总结

## 完成事项
- 完成用户研究
...
"""
```

**优势**:
- ✅ 直接返回 Markdown，无需解析 Notion Blocks
- ✅ AI 可直接分析内容
- ✅ 便于报告总结和知识提取

---

## 📅 Google Calendar MCP 工具详解

### 为什么使用 Google Calendar MCP？

| 对比项 | 直接 Google Calendar API | Google Calendar MCP | 优势 |
|--------|-------------------------|---------------------|------|
| **集成复杂度** | 需要手写 OAuth 流程和 API 封装 | 使用标准化 MCP 协议 | ✅ 降低 60% 代码量 |
| **认证管理** | 自己实现 OAuth 2.0 + refresh token | MCP 托管 OAuth | ✅ 零维护 |
| **自然语言支持** | 需要手动解析时间和日期 | MCP 内置智能解析 | ✅ "明天下午3点" 直接可用 |
| **多日历支持** | 需要循环调用多个 calendar ID | MCP 一次性获取 | ✅ 更高效 |
| **错误处理** | 需手动处理 API 限流和重试 | MCP 自动处理 | ✅ 更稳定 |

---

### 1. list_events()
**功能**: 列出日历事件

```python
# MCP Tool 定义
{
  "name": "list_events",
  "description": "列出指定时间范围内的日历事件",
  "parameters": {
    "calendar_id": "string",  # 日历 ID（可选，默认主日历）
    "time_min": "string",     # ISO 8601 格式或自然语言
    "time_max": "string",
    "max_results": "integer",  # 最多返回数量
    "single_events": "boolean"  # 是否展开重复事件
  }
}

# 使用示例
events = await gcal_mcp.call_tool(
    "list_events",
    time_min="today",           # 支持自然语言！
    time_max="next week",
    max_results=50
)
# 返回: [
#   {
#     "id": "event_123",
#     "summary": "团队会议",
#     "start": "2025-11-28T15:00:00+08:00",
#     "end": "2025-11-28T16:00:00+08:00",
#     "attendees": ["user@example.com"]
#   },
#   ...
# ]
```

---

### 2. create_event()
**功能**: 创建日历事件

```python
# MCP Tool 定义
{
  "name": "create_event",
  "description": "创建新的日历事件",
  "parameters": {
    "calendar_id": "string",
    "summary": "string",        # 事件标题
    "description": "string",    # 事件描述（Markdown 支持）
    "start": "string",          # 开始时间（ISO 8601 或自然语言）
    "end": "string",            # 结束时间
    "attendees": ["string"],    # 参会者邮箱列表
    "location": "string",       # 地点
    "reminders": {
      "useDefault": false,
      "overrides": [
        {"method": "popup", "minutes": 30}
      ]
    }
  }
}

# 使用示例
event = await gcal_mcp.call_tool(
    "create_event",
    summary="产品设计评审",
    description="讨论 Q1 产品路线图",
    start="tomorrow 3pm",        # 自然语言！
    end="tomorrow 4:30pm",
    attendees=["team@example.com"],
    location="会议室 A",
    reminders={
        "overrides": [
            {"method": "popup", "minutes": 30},
            {"method": "email", "minutes": 60}
        ]
    }
)
# 返回: {
#   "id": "event_456",
#   "htmlLink": "https://calendar.google.com/event?eid=...",
#   "hangoutLink": "https://meet.google.com/..."  # 自动生成 Meet 链接
# }
```

**优势**:
- ✅ 自然语言时间解析："明天下午3点" → ISO 8601
- ✅ 自动生成 Google Meet 链接
- ✅ Markdown 描述支持

---

### 3. update_event()
**功能**: 更新现有事件

```python
# 使用示例：修改会议时间
await gcal_mcp.call_tool(
    "update_event",
    event_id="event_456",
    start="tomorrow 4pm",  # 推迟1小时
    end="tomorrow 5:30pm",
    description="**更新**: 增加产品 Demo 环节"
)
```

---

### 4. search_events()
**功能**: 搜索事件

```python
# 使用示例：查找本周所有团队会议
meetings = await gcal_mcp.call_tool(
    "search_events",
    query="团队会议",
    time_min="this week",
    time_max="next week"
)
```

---

### 5. get_free_busy()
**功能**: 查询空闲/忙碌状态

```python
# 使用示例：查找团队成员的空闲时间
free_busy = await gcal_mcp.call_tool(
    "get_free_busy",
    calendars=["user1@example.com", "user2@example.com"],
    time_min="tomorrow 9am",
    time_max="tomorrow 6pm"
)
# 返回: {
#   "user1@example.com": {
#     "busy": [
#       {"start": "2025-11-28T10:00:00+08:00", "end": "2025-11-28T11:00:00+08:00"}
#     ]
#   },
#   ...
# }
```

**应用场景**: 智能会议安排 - 自动找到所有人都空闲的时间段

---

### 6. delete_event()
**功能**: 删除事件

```python
# 使用示例
await gcal_mcp.call_tool(
    "delete_event",
    event_id="event_123",
    send_updates="all"  # 通知所有参会者
)
```

---

### 7. list_calendars()
**功能**: 列出所有日历

```python
# 使用示例：获取用户所有日历
calendars = await gcal_mcp.call_tool("list_calendars")
# 返回: [
#   {
#     "id": "primary",
#     "summary": "我的日历",
#     "timeZone": "Asia/Shanghai"
#   },
#   {
#     "id": "team@example.com",
#     "summary": "团队日历",
#     "accessRole": "writer"
#   }
# ]
```

---

## 🔧 技术实现

### 1. Notion MCP Client 配置

#### 方式A：使用官方 Notion MCP Server（推荐）

```python
# backend/adapters/notion_mcp_client.py

from mcp import MCPClient
from typing import Dict, Any, List

class NotionMCPClient:
    """Notion MCP 客户端封装"""

    def __init__(self, workspace_token: str):
        self.client = MCPClient(
            server_url="https://mcp.notion.com/mcp",
            auth_token=workspace_token  # OAuth token
        )

    async def search(self, query: str, **kwargs) -> List[Dict]:
        """搜索 Notion 内容"""
        return await self.client.call_tool(
            "search_notion",
            query=query,
            **kwargs
        )

    async def create_page(
        self,
        parent_id: str,
        title: str,
        content: str,  # Markdown
        **kwargs
    ) -> Dict:
        """创建页面"""
        return await self.client.call_tool(
            "create_page",
            parent_id=parent_id,
            title=title,
            content=content,
            **kwargs
        )

    async def query_database(
        self,
        database_id: str,
        filter: Dict = None,
        sorts: List[Dict] = None
    ) -> List[Dict]:
        """查询数据库"""
        return await self.client.call_tool(
            "query_database",
            database_id=database_id,
            filter=filter,
            sorts=sorts
        )

    async def update_item(
        self,
        database_id: str,
        item_id: str,
        properties: Dict
    ) -> Dict:
        """更新数据库行"""
        return await self.client.call_tool(
            "update_database_item",
            database_id=database_id,
            item_id=item_id,
            properties=properties
        )

    async def append_content(
        self,
        page_id: str,
        content: str  # Markdown
    ) -> Dict:
        """追加内容到页面"""
        return await self.client.call_tool(
            "append_blocks",
            page_id=page_id,
            content=content
        )
```

---

#### 方式B：使用社区 Notion MCP 实现

如果需要更多控制或自定义功能，可以使用 Python 社区实现：

```bash
# 安装社区 MCP 客户端
pip install notion-mcp-client
# 或
pip install git+https://github.com/pbohannon/notion-api-mcp.git
```

```python
# 配置示例
from notion_api_mcp import NotionMCPServer

# 初始化 MCP 服务器
server = NotionMCPServer(
    notion_api_key=os.getenv("NOTION_API_KEY"),
    parent_page_id=os.getenv("NOTION_PARENT_PAGE_ID")
)

# 使用工具
result = await server.create_todo_item(
    title="完成月度报告",
    due_date="2025-11-30",
    priority="高"
)
```

---

###  2. Google Calendar MCP Client 配置

#### 方式A：使用社区 Google Calendar MCP Server（推荐）

基于前面的搜索结果，有多个优秀的 Google Calendar MCP 实现可供选择：

```bash
# 安装 Google Calendar MCP 客户端
# 选项1: nspady/google-calendar-mcp (功能最全面)
npm install @nspady/google-calendar-mcp

# 选项2: goldk3y/google-calendar-mcp (简洁稳定)
npm install @goldk3y/google-calendar-mcp
```

```python
# backend/adapters/gcal_mcp_client.py

from mcp import MCPClient
from typing import Dict, Any, List
import os

class GoogleCalendarMCPClient:
    """Google Calendar MCP 客户端封装"""

    def __init__(self, credentials_path: str = None):
        # 使用社区 MCP Server
        self.client = MCPClient(
            server_url="http://localhost:3000/mcp",  # 本地 MCP Server
            auth_token=self._get_oauth_token()
        )

    def _get_oauth_token(self) -> str:
        """获取 OAuth Token (MCP Server 托管)"""
        # MCP Server 会处理 OAuth 流程
        return os.getenv("GOOGLE_CALENDAR_OAUTH_TOKEN")

    async def list_events(
        self,
        time_min: str = "today",
        time_max: str = "next week",
        max_results: int = 50,
        calendar_id: str = "primary"
    ) -> List[Dict]:
        """列出日历事件"""
        return await self.client.call_tool(
            "list_events",
            calendar_id=calendar_id,
            time_min=time_min,  # 支持自然语言！
            time_max=time_max,
            max_results=max_results,
            single_events=True
        )

    async def create_event(
        self,
        summary: str,
        start: str,
        end: str,
        description: str = None,
        attendees: List[str] = None,
        location: str = None,
        **kwargs
    ) -> Dict:
        """创建日历事件"""
        return await self.client.call_tool(
            "create_event",
            summary=summary,
            start=start,  # 支持自然语言："tomorrow 3pm"
            end=end,
            description=description,
            attendees=attendees,
            location=location,
            **kwargs
        )

    async def update_event(
        self,
        event_id: str,
        **updates
    ) -> Dict:
        """更新事件"""
        return await self.client.call_tool(
            "update_event",
            event_id=event_id,
            **updates
        )

    async def delete_event(
        self,
        event_id: str,
        send_updates: str = "all"
    ) -> bool:
        """删除事件"""
        return await self.client.call_tool(
            "delete_event",
            event_id=event_id,
            send_updates=send_updates
        )

    async def search_events(
        self,
        query: str,
        time_min: str = None,
        time_max: str = None
    ) -> List[Dict]:
        """搜索事件"""
        return await self.client.call_tool(
            "search_events",
            query=query,
            time_min=time_min,
            time_max=time_max
        )

    async def get_free_busy(
        self,
        calendars: List[str],
        time_min: str,
        time_max: str
    ) -> Dict:
        """查询空闲/忙碌状态"""
        return await self.client.call_tool(
            "get_free_busy",
            calendars=calendars,
            time_min=time_min,
            time_max=time_max
        )

    async def list_calendars(self) -> List[Dict]:
        """列出所有日历"""
        return await self.client.call_tool("list_calendars")
```

---

#### 方式B：直接使用 Google Calendar API (不推荐)

如果不使用 MCP，需要手动处理 OAuth 和 API 调用：

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class GoogleCalendarAPIClient:
    """直接 API 方式（不推荐）"""

    def __init__(self, credentials: Credentials):
        self.service = build('calendar', 'v3', credentials=credentials)

    def list_events(self, time_min, time_max):
        # 需要手动转换时间格式
        # 需要手动分页
        # 需要手动错误处理
        # ~100 行代码...
        pass
```

**对比**:
- MCP 方式: ~10 行代码
- 直接 API: ~100 行代码
- **推荐使用 MCP 方式** ✅

---

### 3. MCP 配置文件

```json
// backend/config/mcp.json
{
  "mcpServers": {
    "notion": {
      "url": "https://mcp.notion.com/mcp",
      "auth": {
        "type": "oauth2",
        "token_url": "https://api.notion.com/v1/oauth/token",
        "scopes": [
          "read_content",
          "update_content",
          "create_content"
        ]
      },
      "config": {
        "workspace_id": "${NOTION_WORKSPACE_ID}",
        "command_center_db": "${COMMAND_CENTER_DB_ID}",
        "calendar_db": "${CALENDAR_DB_ID}",
        "reports_db": "${REPORTS_DB_ID}"
      }
    },
    "google_calendar": {
      "url": "http://localhost:3000/mcp",
      "auth": {
        "type": "oauth2",
        "token_url": "https://oauth2.googleapis.com/token",
        "scopes": [
          "https://www.googleapis.com/auth/calendar",
          "https://www.googleapis.com/auth/calendar.events"
        ],
        "client_id": "${GOOGLE_CLIENT_ID}",
        "client_secret": "${GOOGLE_CLIENT_SECRET}"
      },
      "config": {
        "default_calendar_id": "primary",
        "timezone": "Asia/Shanghai"
      }
    }
  }
}
```

---

### 3. Notion Listener (使用 MCP)

```python
# backend/listeners/notion_mcp_listener.py

import asyncio
from backend.adapters.notion_mcp_client import NotionMCPClient
from backend.core.executor import TaskExecutor
from backend.config import settings

class NotionMCPListener:
    """使用 MCP 协议监听 Notion 指令"""

    def __init__(
        self,
        mcp_client: NotionMCPClient,
        task_executor: TaskExecutor,
        poll_interval: int = 30
    ):
        self.mcp = mcp_client
        self.executor = task_executor
        self.poll_interval = poll_interval

    async def start(self):
        """启动监听器"""
        logger.info("Notion MCP Listener started")

        while True:
            try:
                await self._poll_commands()
            except Exception as e:
                logger.error(f"Listener error: {e}")

            await asyncio.sleep(self.poll_interval)

    async def _poll_commands(self):
        """检查待处理指令"""
        # 使用 MCP query_database 工具
        commands = await self.mcp.query_database(
            database_id=settings.COMMAND_CENTER_DB_ID,
            filter={
                "property": "状态",
                "select": {"equals": "⏳ Pending"}
            },
            sorts=[
                {
                    "property": "创建时间",
                    "direction": "ascending"
                }
            ]
        )

        for cmd in commands:
            command_id = cmd["id"]
            instruction = cmd["properties"]["指令"]["title"][0]["text"]["content"]

            # 更新为 Processing
            await self.mcp.update_item(
                database_id=settings.COMMAND_CENTER_DB_ID,
                item_id=command_id,
                properties={
                    "状态": {"select": {"name": "🔄 Processing"}}
                }
            )

            try:
                # 执行任务
                result = await self.executor.execute(instruction)

                # 回写结果（成功）
                await self._write_success(command_id, result)

            except Exception as e:
                # 回写结果（失败）
                await self._write_error(command_id, str(e))

    async def _write_success(self, command_id: str, result: Dict):
        """写入成功结果"""
        await self.mcp.update_item(
            database_id=settings.COMMAND_CENTER_DB_ID,
            item_id=command_id,
            properties={
                "状态": {"select": {"name": "✅ Done"}},
                "结果": {
                    "rich_text": [{
                        "text": {"content": result.get("message", "执行成功")}
                    }]
                },
                "相关链接": {
                    "url": result.get("link")
                } if result.get("link") else None,
                "处理时长": {
                    "number": result.get("duration_ms", 0) / 1000
                }
            }
        )

    async def _write_error(self, command_id: str, error: str):
        """写入错误结果"""
        await self.mcp.update_item(
            database_id=settings.COMMAND_CENTER_DB_ID,
            item_id=command_id,
            properties={
                "状态": {"select": {"name": "❌ Error"}},
                "结果": {
                    "rich_text": [{
                        "text": {"content": f"❌ 执行失败：{error}"}
                    }]
                }
            }
        )
```

---

### 4. Report Generator (使用 MCP)

```python
# backend/core/report_generator.py

class ReportGenerator:
    """报告生成器（使用 Notion MCP）"""

    def __init__(
        self,
        llm_client: LLMClient,
        mcp_client: NotionMCPClient
    ):
        self.llm = llm_client
        self.mcp = mcp_client

    async def generate_weekly_report(
        self,
        calendar_events: List[Dict],
        notion_tasks: List[Dict]
    ) -> Dict:
        """生成周报并保存到 Notion"""

        # 1. 数据聚合
        stats = self._calculate_stats(calendar_events, notion_tasks)

        # 2. 使用 LLM 生成 Markdown 报告
        report_md = await self._generate_markdown(stats, calendar_events, notion_tasks)

        # 3. 使用 MCP 创建 Notion 页面
        page = await self.mcp.create_page(
            parent_id=settings.REPORTS_DB_ID,
            title=f"📊 {stats['week_range']} 工作总结",
            content=report_md,  # 直接传入 Markdown
            icon="📊"
        )

        return {
            "message": "✅ 已生成周报",
            "link": page["url"],
            "page_id": page["id"]
        }

    async def _generate_markdown(
        self,
        stats: Dict,
        events: List[Dict],
        tasks: List[Dict]
    ) -> str:
        """使用 LLM 生成 Markdown 格式报告"""

        prompt = f"""
请根据以下数据生成一份结构化的工作周报（Markdown 格式）：

## 时间统计
- 会议总时长: {stats['meeting_hours']}小时
- 深度工作时长: {stats['deep_work_hours']}小时

## 完成事项
{self._format_tasks(tasks)}

## 日程安排
{self._format_events(events)}

要求：
1. 使用 Markdown 格式
2. 包含 emoji 图标
3. 突出关键成果
4. 提供改进建议
        """

        return await self.llm.complete(prompt)
```

---

## 📝 数据库 Schema 更新

```sql
-- 新增 MCP 连接配置表
CREATE TABLE mcp_connections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,  -- 'notion', 'google', etc.
    server_url VARCHAR(255),
    oauth_token_encrypted TEXT,
    oauth_refresh_token_encrypted TEXT,
    token_expires_at TIMESTAMP,
    workspace_config JSONB,  -- 存储工作区特定配置
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_mcp_connections_user_id ON mcp_connections(user_id);
CREATE INDEX idx_mcp_connections_provider ON mcp_connections(provider);
```

---

## 🔄 完整工作流程示例

### 场景：用户创建日历事件 + 自动创建 Notion 页面

```python
# backend/core/executor.py

class TaskExecutor:
    """任务执行器"""

    def __init__(
        self,
        parser: TaskParser,
        mcp_client: NotionMCPClient,
        calendar_adapter: CalendarAdapter
    ):
        self.parser = parser
        self.mcp = mcp_client
        self.calendar = calendar_adapter

    async def execute(self, instruction: str) -> Dict:
        """执行用户指令"""

        # 1. 解析指令
        parsed = await self.parser.parse(instruction)
        intent = parsed["intent"]
        entities = parsed["entities"]

        # 2. 根据意图执行
        if intent == "calendar_create_with_note":
            # 2.1 创建日历事件
            event = await self.calendar.create_event(
                title=entities["event_title"],
                start_time=entities["start_time"],
                duration_minutes=entities.get("duration_minutes", 60)
            )

            # 2.2 使用 MCP 创建 Notion 会议纪要页面
            note_page = await self.mcp.create_page(
                parent_id=settings.MEETING_NOTES_DB_ID,
                title=f"📝 {entities['event_title']} - 会议纪要",
                content=f"""
# 📝 {entities['event_title']}

## 📅 会议信息
- **时间**: {entities['start_time']}
- **日历事件**: [查看日历]({event['link']})

## 📋 议题
1. [待补充]

## ✅ 行动项
- [ ] [待补充]

## 📌 备注
                """,
                icon="📝"
            )

            return {
                "message": f"✅ 已创建日历事件并生成会议纪要页面",
                "link": note_page["url"],
                "calendar_event": event["link"]
            }

        elif intent == "generate_report":
            # 生成报告流程...
            pass
```

---

## 🚀 部署配置

### Docker Compose 更新

```yaml
# docker-compose.yml

version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: docker/Dockerfile
    environment:
      # Notion MCP 配置
      - NOTION_MCP_SERVER_URL=https://mcp.notion.com/mcp
      - NOTION_WORKSPACE_ID=${NOTION_WORKSPACE_ID}
      - NOTION_OAUTH_TOKEN=${NOTION_OAUTH_TOKEN}

      # 数据库 ID
      - COMMAND_CENTER_DB_ID=${COMMAND_CENTER_DB_ID}
      - CALENDAR_DB_ID=${CALENDAR_DB_ID}
      - REPORTS_DB_ID=${REPORTS_DB_ID}

      # 其他配置
      - DATABASE_URL=postgresql://ailma:password@db:5432/ailma
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app/backend
```

---

## 📊 性能对比

| 操作 | 直接 Notion API | Notion MCP | 性能提升 |
|------|----------------|-----------|---------|
| **创建页面** | 需转换 Markdown → Blocks (~500 行代码) | 直接传 Markdown (~10 行) | ✅ 98% 减少 |
| **读取内容** | 解析 Blocks → 文本 (~300 行) | 直接获取 Markdown | ✅ 90% 减少 |
| **搜索** | 需手动分页和过滤 | MCP 自动处理 | ✅ 更稳定 |
| **OAuth 管理** | 自己实现 refresh logic | MCP 托管 | ✅ 零维护 |

---

## 🎯 迁移建议

### 从直接 API 迁移到 MCP

1. **Phase 1**: 保留现有 Notion Adapter，新增 MCP Client
2. **Phase 2**: 新功能优先使用 MCP
3. **Phase 3**: 逐步迁移现有功能到 MCP
4. **Phase 4**: 移除旧的 Notion API 代码

### 兼容性策略

```python
class NotionIntegration:
    """统一的 Notion 集成接口"""

    def __init__(self, use_mcp: bool = True):
        if use_mcp:
            self.client = NotionMCPClient()
        else:
            self.client = NotionAPIClient()  # 旧方式

    async def create_page(self, **kwargs):
        """统一接口，自动选择实现"""
        return await self.client.create_page(**kwargs)
```

---

## 📚 相关资源

### Notion MCP
- [Notion MCP 官方文档](https://developers.notion.com/docs/mcp)
- [社区 Python MCP 实现](https://github.com/pbohannon/notion-api-mcp)
- [Notion MCP 工具目录](https://lobehub.com/mcp)

### Google Calendar MCP
- [nspady/google-calendar-mcp](https://github.com/nspady/google-calendar-mcp) - 功能最全面
- [goldk3y/google-calendar-mcp](https://github.com/goldk3y/google-calendar-mcp) - 简洁稳定
- [deciduus/calendar-mcp](https://github.com/deciduus/calendar-mcp) - Python 实现
- [markelaugust74/mcp-google-calendar](https://github.com/markelaugust74/mcp-google-calendar) - Claude 集成
- [MCP Google Calendar 目录](https://mcp.so/server/mcp-google-calendar)

### MCP 协议
- [MCP 协议规范](http://blog.modelcontextprotocol.io/)
- [Model Context Protocol 文档](https://modelcontextprotocol.io/)

---

**推荐使用此架构：双 MCP 集成（Notion + Google Calendar）替代原有的直接 API 调用方式！**

**核心优势**:
- ✅ **Notion MCP**: Markdown 原生支持，98% 代码减少
- ✅ **Google Calendar MCP**: 自然语言时间解析，60% 代码减少
- ✅ **统一 MCP 架构**: OAuth 托管，长期稳定，开放标准

**文档版本**: v3.0 (Notion + Google Calendar MCP Integration)
**最后更新**: 2025-11-27
