# Notion 集成（MCP）

**使用 Notion 作为 AILMA 的前端界面**

---

## 🎯 概述

Notion 在 AILMA 中扮演**双重角色**：
1. **前端界面** - 用户输入指令和查看结果
2. **数据存储** - 存储日程、笔记、报告

通过 **Model Context Protocol (MCP)**，我们实现了零代码的 Notion 集成。

---

## ✨ 核心特性

### 1. Markdown 原生支持 ⭐

**直接写入 Markdown**，无需转换为 Notion Blocks：

```python
await notion_mcp.call_tool(
    "create_page",
    title="会议纪要",
    content="""
# 会议纪要

## 议题
- 讨论 Q1 规划
    """
)
```

**对比**（直接 API）:
```python
# 需要手动转换为 Blocks（500+ 行代码）
blocks = [
    {"type": "heading_1", "heading_1": {"rich_text": [...]}},
    {"type": "heading_2", "heading_2": {"rich_text": [...]}},
    {"type": "bulleted_list_item", "bulleted_list_item": {...}},
    # ...
]
await notion_api.pages.create(properties={...}, children=blocks)
```

**优势**: ✅ 98% 代码减少

---

### 2. OAuth 托管

**MCP Server 自动管理 OAuth**:
- ✅ Access Token 刷新
- ✅ 过期处理
- ✅ 安全存储

你只需配置一次，之后零维护。

---

### 3. 8 个强大工具

| 工具 | 功能 | 使用场景 |
|------|------|---------|
| `search_notion()` | 全文搜索 | 查找相关页面 |
| `create_page()` | 创建页面（Markdown） | 创建笔记、报告 |
| `update_page()` | 更新页面 | 修改内容 |
| `query_database()` | 查询数据库 | 获取待处理指令 |
| `create_database_item()` | 添加行 | 添加新指令 |
| `update_database_item()` | 更新行 | 更新指令状态 |
| `append_blocks()` | 追加内容 | 添加评论、更新 |
| `read_page_content()` | 读取内容（Markdown） | AI 分析内容 |

**详细**: [工具参考](./tools-reference.md)

---

## 🏗️ Notion Workspace 结构

### 必需的 3 个数据库

#### 1. 指令中心 (Command Center)

**用途**: 用户输入自然语言指令

**属性**:
| 属性名 | 类型 | 说明 |
|--------|------|------|
| 指令 | Title | 用户输入的文字 |
| 状态 | Select | ⏳ Pending / 🔄 Processing / ✅ Done / ❌ Error |
| 结果 | Text | 执行结果说明 |
| 相关链接 | URL | Google Calendar 或 Notion 页面链接 |
| 处理时长 | Number | 执行耗时（秒） |
| 创建时间 | Created time | 自动 |

**视图**:
- 📋 全部指令
- ⏳ 待处理
- ✅ 已完成
- ❌ 失败

---

#### 2. 日历视图 (Calendar Database)

**用途**: 同步显示 Google Calendar 事件

**属性**:
| 属性名 | 类型 | 说明 |
|--------|------|------|
| 事件名称 | Title | 事件标题 |
| 开始时间 | Date | 事件开始 |
| 结束时间 | Date | 事件结束 |
| 日历来源 | Select | Google Calendar / 手动创建 |
| 参会者 | Multi-select | 参会人员 |
| 会议链接 | URL | Google Meet 链接 |

**视图**:
- 📅 日历视图
- 📋 列表视图
- ⏰ 本周日程

---

#### 3. 报告归档 (Reports Database)

**用途**: 存储 AI 生成的报告

**属性**:
| 属性名 | 类型 | 说明 |
|--------|------|------|
| 报告标题 | Title | 如"2025-W48 工作总结" |
| 类型 | Select | 周报 / 月报 / 项目报告 |
| 生成时间 | Created time | 自动 |
| 时间范围 | Date range | 报告覆盖的时间段 |
| 状态 | Select | 草稿 / 已发布 |

**视图**:
- 📊 按类型分组
- 📅 按时间排序
- ⭐ 精选报告

---

## 🚀 快速开始

### 1. 配置 Notion Integration

**详细步骤**: [MCP 配置指南](./mcp-setup.md)

**简要步骤**:
1. 访问 https://www.notion.so/my-integrations
2. 创建新 Integration
3. 复制 API Key（`secret_...`）
4. 在 Workspace 中分享数据库给 Integration

---

### 2. 环境变量配置

```bash
# .env
NOTION_API_KEY=secret_your_integration_token_here
NOTION_WORKSPACE_ID=your_workspace_id
COMMAND_CENTER_DB_ID=your_command_center_db_id
CALENDAR_DB_ID=your_calendar_db_id
REPORTS_DB_ID=your_reports_db_id
```

**详细**: [环境变量文档](../../deployment/environment.md)

---

### 3. 测试连接

```bash
cd tests/mcp_integration/notion
python test_connection.py
```

**预期输出**:
```
✅ 连接成功！
✅ 可以访问工作区
✅ 可以查询数据库
✅ 可以创建页面
```

---

## 💡 使用示例

### 示例 1: 创建页面

```python
from backend.adapters.notion_mcp_client import NotionMCPClient

mcp = NotionMCPClient(api_key=os.getenv("NOTION_API_KEY"))

# 创建会议纪要
page = await mcp.create_page(
    parent_id=MEETING_NOTES_DB_ID,
    title="团队会议 - Q1规划",
    content="""
# 📝 团队会议纪要

## 📅 会议信息
- 时间: 2025-11-28 15:00
- 参会者: @Alice, @Bob

## 📋 议题
1. Q1 OKR 设定
2. 产品路线图

## ✅ 行动项
- [ ] Alice: 完成 OKR 草稿
- [ ] Bob: 准备技术方案
    """,
    icon="📝"
)

print(f"✅ 创建成功: {page['url']}")
```

**更多示例**: [使用示例文档](./examples.md)

---

## 🔍 工作原理

### Notion Listener 工作流

```
1. [启动] 每 30 秒轮询一次
    ↓
2. [查询] query_database("指令中心", 状态="⏳ Pending")
    ↓
3. [处理] 对每条指令:
   - 更新状态为 "🔄 Processing"
   - 传递给 AI Core
   - 执行任务
   - 回写结果（状态="✅ Done" 或 "❌ Error"）
    ↓
4. [等待] 30 秒后重复
```

---

## 📚 相关文档

### 必读
- **[MCP 配置指南](./mcp-setup.md)** - 详细配置步骤
- **[工具参考](./tools-reference.md)** - 8 个工具详细说明
- **[使用示例](./examples.md)** - 实际代码示例

### 相关
- [架构设计](../../overview/architecture.md) - 系统架构
- [开发者指南](../../guides/developer-guide.md) - 开发流程
- [MCP 协议](../../reference/mcp-protocol.md) - MCP 协议说明

---

**文档**: [总索引](../../INDEX.md)
**最后更新**: 2025-11-27
