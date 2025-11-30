# AILMA Notion 数据库结构设计

本文档详细说明 AILMA 项目需要的 3 个 Notion 数据库结构。

---

## 📋 数据库概览

AILMA 需要 3 个 Notion 数据库来完成完整的工作流：

| 数据库 | 用途 | 重要性 |
|--------|------|--------|
| **指令中心** | 接收和处理用户的自然语言指令 | ✅ 必需 |
| **日历事件** | 存储和管理日历事件记录 | ✅ 必需 |
| **工作报告** | 存储自动生成的周报/月报 | ⚠️ 推荐 |

---

## 1️⃣ 指令中心 (Command Center)

### 用途
- 用户在此输入自然语言指令
- AILMA 监听此数据库，处理 `pending` 状态的指令
- 处理完成后更新状态和结果

### 数据库属性

| 属性名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| **指令** | Title | 用户输入的自然语言命令 | "明天下午3点开会" |
| **状态** | Select | 指令处理状态 | pending, processing, completed, failed |
| **意图类型** | Select | AI识别的意图类型 | calendar_create, notion_create_page 等 |
| **置信度** | Number(%) | AI识别的置信度 | 95% |
| **执行结果** | Rich Text | 执行结果描述 | "已创建日历事件：产品评审会" |
| **错误信息** | Rich Text | 失败时的错误详情 | "缺少事件标题" |
| **创建时间** | Created Time | 指令创建时间 | 自动生成 |
| **处理时间** | Date | 实际处理时间 | 2025-11-30 15:00 |

### 状态选项

```
pending (黄色) - 等待处理
processing (蓝色) - 处理中
completed (绿色) - 已完成
failed (红色) - 失败
```

### 意图类型选项

```
calendar_create (蓝色) - 创建日历事件
calendar_query (紫色) - 查询日程
calendar_update (橙色) - 更新事件
calendar_delete (红色) - 删除事件
notion_create_page (绿色) - 创建笔记
notion_create_todo (黄色) - 创建待办
generate_report (粉色) - 生成报告
unknown (灰色) - 未识别
```

### 使用示例

**输入指令**:
```
指令: 明天下午3点在会议室A开产品评审会
状态: pending
```

**AILMA 处理后**:
```
指令: 明天下午3点在会议室A开产品评审会
状态: completed
意图类型: calendar_create
置信度: 95%
执行结果: 已创建日历事件：产品评审会
         时间: 2025-12-01 15:00
         地点: 会议室A
         Google Calendar ID: event123456
```

---

## 2️⃣ 日历事件 (Calendar Events)

### 用途
- 记录所有通过 AILMA 创建/管理的日历事件
- 作为 Google Calendar 的本地镜像
- 便于在 Notion 中查看和管理日程

### 数据库属性

| 属性名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| **事件标题** | Title | 事件名称 | "产品评审会" |
| **开始时间** | Date | 事件开始时间（支持时间段） | 2025-12-01 15:00 → 16:00 |
| **地点** | Rich Text | 事件地点 | "会议室A" |
| **参与者** | Multi-Select | 参与人员 | 张三, 李四 |
| **事件类型** | Select | 事件分类 | 会议, 个人, 团队活动 等 |
| **状态** | Select | 事件状态 | 已计划, 进行中, 已完成, 已取消 |
| **Google Calendar ID** | Rich Text | 对应的 Google Calendar 事件 ID | event123456 |
| **Meet 链接** | URL | Google Meet 视频链接 | https://meet.google.com/xxx |
| **描述** | Rich Text | 事件详细描述 | "讨论 Q4 产品规划" |
| **创建时间** | Created Time | 记录创建时间 | 自动生成 |

### 事件类型选项

```
会议 (蓝色)
个人 (绿色)
团队活动 (紫色)
培训 (橙色)
其他 (灰色)
```

### 状态选项

```
已计划 (黄色)
进行中 (蓝色)
已完成 (绿色)
已取消 (红色)
```

### 使用示例

```
事件标题: 产品评审会
开始时间: 2025-12-01 15:00 → 16:00
地点: 会议室A
参与者: 张三, 李四, 王五
事件类型: 会议
状态: 已计划
Google Calendar ID: evt_abc123xyz
Meet 链接: https://meet.google.com/abc-defg-hij
描述: 讨论 Q4 产品路线图，评审新功能提案
```

---

## 3️⃣ 工作报告 (Reports)

### 用途
- 存储 AILMA 自动生成的工作报告
- 支持日报、周报、月报等多种类型
- 包含 AI 生成的摘要和数据分析

### 数据库属性

| 属性名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| **报告标题** | Title | 报告名称 | "2025年11月工作周报" |
| **报告类型** | Select | 报告类别 | 周报, 月报 等 |
| **时间范围** | Date | 报告覆盖的时间段 | 2025-11-25 → 2025-12-01 |
| **事件统计** | Number | 时间段内的事件总数 | 12 |
| **会议时长** | Number | 总会议时长（分钟） | 480 |
| **生成时间** | Created Time | 报告生成时间 | 自动生成 |
| **状态** | Select | 报告状态 | 草稿, 已完成, 已归档 |
| **标签** | Multi-Select | 报告标签 | 重要, 团队, 个人 |

### 报告类型选项

```
日报 (蓝色)
周报 (绿色)
月报 (紫色)
季度报告 (橙色)
年度总结 (红色)
```

### 状态选项

```
草稿 (黄色)
已完成 (绿色)
已归档 (灰色)
```

### 报告内容结构

AILMA 会在 Notion 页面中生成以下格式的报告：

```markdown
# 周报 - 2025-11-25 到 2025-12-01

## AI 生成摘要

本周共有 12 个事件，总时长 8 小时。
主要活动包括团队会议（5次）、产品评审（2次）、客户沟通（3次）。

## 重点事件

1. 周三的产品发布会 - 成功发布 v2.0
2. 周五的客户演示 - 获得积极反馈
3. 团队建设活动 - 增强凝聚力

## 时间分配

- 会议: 60% (480 分钟)
- 个人工作: 30% (240 分钟)
- 其他: 10% (80 分钟)

## 下周建议

- 减少会议时长
- 增加深度工作时间
- 优先处理 Q4 规划
```

---

## 🚀 快速创建数据库

### 方式 1: 使用自动化脚本（推荐）

我们提供了自动创建脚本：

```bash
# 1. 确保 Notion API Key 已配置
source venv/bin/activate

# 2. 安装 notion-client（如果还没有）
pip install --proxy="" notion-client

# 3. 运行创建脚本
python scripts/create-notion-databases.py
```

**脚本会自动**：
- 在你的父页面下创建 3 个数据库
- 配置所有属性和选项
- 更新 .env 文件中的数据库 ID
- 显示创建结果和访问链接

### 方式 2: 手动创建

如果你想手动创建数据库：

#### 步骤 1: 在 Notion 中创建数据库

1. 打开父页面: https://www.notion.so/2bb84b1a1c798051a616de266920ab4e
2. 点击 **"New"** → **"Database - Full page"**
3. 命名数据库（如 "📋 AILMA 指令中心"）

#### 步骤 2: 添加属性

按照上面的表格添加每个属性：
- 点击数据库右上角的 **"+"** 添加属性
- 选择正确的属性类型
- 配置 Select/Multi-Select 的选项

#### 步骤 3: 配置 Select 选项

为 Select 类型属性添加选项：
1. 点击属性名
2. 点击 **"Edit property"**
3. 添加选项和颜色

#### 步骤 4: 获取数据库 ID

1. 打开数据库页面
2. 复制 URL，格式：
   ```
   https://www.notion.so/database-id?v=view-id
   ```
3. 提取 `database-id` 部分

#### 步骤 5: 分享给 Integration

1. 点击数据库右上角 **"..."**
2. 选择 **"Add connections"**
3. 选择你的 Integration
4. 点击 **"Confirm"**

#### 步骤 6: 更新 .env 文件

```bash
COMMAND_CENTER_DB_ID=你的指令中心数据库ID
CALENDAR_DB_ID=你的日历事件数据库ID
REPORTS_DB_ID=你的工作报告数据库ID
```

---

## 🔍 数据库关系图

```
┌─────────────────────────────────────────┐
│     Notion 父页面 (Parent Page)          │
│  https://www.notion.so/2bb84b1a...      │
└─────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ 指令中心  │  │ 日历事件  │  │ 工作报告  │
│ Command  │  │ Calendar │  │ Reports  │
│ Center   │  │ Events   │  │          │
└──────────┘  └──────────┘  └──────────┘
     │              │              │
     └──────────────┴──────────────┘
                    │
                    ▼
            ┌───────────────┐
            │  AILMA 后端    │
            │  (监听、处理)  │
            └───────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│ Google       │        │ Claude API   │
│ Calendar API │        │ (AI 解析)    │
└──────────────┘        └──────────────┘
```

---

## 📝 使用建议

### 1. 视图设置

为每个数据库创建多个视图：

**指令中心**:
- 📋 所有指令（Table 视图）
- ⏳ 待处理（Filter: status = pending）
- ✅ 已完成（Filter: status = completed）
- 📅 按日期（Calendar 视图，按创建时间）

**日历事件**:
- 📅 日历视图（Calendar 视图，按开始时间）
- 📋 列表视图（Table 视图）
- 🔜 即将到来（Filter: 开始时间 > 今天）
- ✅ 已完成（Filter: status = 已完成）

**工作报告**:
- 📊 全部报告（Table 视图）
- 📅 按时间（Timeline 视图）
- 🏷️ 按类型（Group by 报告类型）

### 2. 模板设置

为常用指令创建模板：

**指令中心模板**:
```
指令: [在此输入你的指令]
状态: pending
创建时间: [自动]
```

### 3. 自动化建议

使用 Notion 内置自动化：
- 当状态改为 `completed` 时，添加 ✅ emoji
- 当状态改为 `failed` 时，添加 ❌ emoji

---

## 🆘 故障排查

### 问题 1: 脚本运行失败

**错误**: `notion-client 未安装`

**解决**:
```bash
pip install --proxy="" notion-client
```

### 问题 2: API 返回 401 Unauthorized

**原因**: Integration 未分享给页面

**解决**:
1. 打开父页面
2. 点击右上角 **"..."** → **"Add connections"**
3. 选择你的 Integration

### 问题 3: 找不到父页面

**检查**:
```bash
# 确认 .env 中的 ID 正确
grep COMMAND_CENTER_DB_ID .env
```

---

## 📚 相关文档

- [Notion MCP 配置](./mcp-setup.md)
- [API Keys 获取指南](../../guides/api-keys-setup.md)
- [Notion API 文档](https://developers.notion.com/docs)

---

**最后更新**: 2025-11-30
**版本**: v1.0
