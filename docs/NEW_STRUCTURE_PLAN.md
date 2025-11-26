# AILMA 文档重构计划

**目标**: 将庞大的单体文档拆分为模块化、短小、互联的文档系统

---

## 📊 当前问题分析

| 文档 | 当前行数 | 问题 |
|------|---------|------|
| PRD.md | 1,441 行 | 过长，包含太多不同类型的内容 |
| ARCHITECTURE-MCP.md | 1,245 行 | 混合了架构、配置、代码示例 |
| DEVELOPMENT.md | 1,021 行 | 开发指南过于详细，难以快速查找 |
| DEPLOYMENT.md | 851 行 | 部署配置混在一起 |

**核心问题**:
- ❌ 文档太长，查找困难
- ❌ 混合多种内容类型（概念、配置、代码、教程）
- ❌ 不利于扩展（新增集成需要修改大文档）
- ❌ 维护困难（修改一处影响其他）

---

## 🎯 新架构设计原则

### 1. 单一职责原则
每个文档只讲**一件事**：
- ✅ `notion/mcp-setup.md` - 只讲 Notion MCP 配置
- ✅ `google-calendar/tools-reference.md` - 只列 Google Calendar 工具
- ❌ 不要在一个文档里混合架构 + 配置 + 教程

### 2. 长度限制
- 概览类：< 150 行
- 指南类：< 200 行
- 参考类：< 100 行
- 配置类：< 150 行

### 3. 链接优先
- 用 `[查看详细配置](./integrations/notion/mcp-setup.md)` 代替内联所有内容
- 文档间互相引用，形成知识图谱

### 4. 分层架构
```
Level 1: 概览 (What & Why)
  ↓
Level 2: 指南 (How)
  ↓
Level 3: 详细配置 (Details)
  ↓
Level 4: API 参考 (Reference)
```

---

## 📂 新目录结构

```
docs/
├── INDEX.md                    # 📚 总索引（导航中枢）
│
├── overview/                   # 📖 概览层
│   ├── what-is-ailma.md       # AILMA 是什么（产品定位）
│   ├── architecture.md         # 架构概览（高层设计）
│   └── tech-stack.md           # 技术栈（技术选型）
│
├── guides/                     # 🎓 指南层
│   ├── quick-start.md         # 5分钟快速开始
│   ├── user-guide.md          # 用户使用指南
│   └── developer-guide.md     # 开发者指南
│
├── integrations/               # 🔌 集成模块
│   ├── notion/
│   │   ├── README.md          # Notion 集成概览
│   │   ├── mcp-setup.md       # MCP 配置步骤
│   │   ├── tools-reference.md # 8个工具详细说明
│   │   └── examples.md        # 使用示例
│   │
│   ├── google-calendar/
│   │   ├── README.md          # Google Calendar 概览
│   │   ├── mcp-setup.md       # MCP 配置步骤
│   │   ├── tools-reference.md # 7个工具详细说明
│   │   └── examples.md        # 使用示例
│   │
│   └── claude/
│       ├── README.md          # Claude API 概览
│       └── api-setup.md       # API Key 配置
│
├── features/                   # ⚙️ 功能模块
│   ├── calendar-management.md # 日历管理功能
│   ├── note-taking.md         # 笔记管理功能
│   ├── report-generation.md   # 报告生成功能
│   └── task-parsing.md        # 任务解析功能
│
├── deployment/                 # 🚀 部署相关
│   ├── docker.md              # Docker 部署
│   ├── kubernetes.md          # K8s 部署
│   ├── environment.md         # 环境变量详解
│   └── security.md            # 安全配置
│
├── api/                        # 📡 API 文档
│   ├── rest-api.md            # REST API 端点
│   ├── commands.md            # 命令格式
│   ├── webhooks.md            # Webhook 配置
│   └── errors.md              # 错误码参考
│
└── reference/                  # 📚 参考资料
    ├── mcp-protocol.md        # MCP 协议说明
    ├── database-schema.md     # 数据库 Schema
    ├── troubleshooting.md     # 常见问题
    ├── glossary.md            # 术语表
    └── changelog.md           # 变更日志
```

---

## 🔄 迁移映射表

### 旧文档 → 新文档拆分

#### PRD.md (1,441行) → 拆分为 9 个文档
| 原章节 | 新文档 | 行数估计 |
|--------|--------|---------|
| 产品定位 | `overview/what-is-ailma.md` | ~80 |
| 用户故事 | `guides/user-guide.md` | ~100 |
| 功能需求 FR1-FR4 | `features/*.md` (4个文件) | ~150/个 |
| 技术架构 | `overview/architecture.md` | ~120 |
| 数据库设计 | `reference/database-schema.md` | ~100 |
| Notion Database | `integrations/notion/README.md` | ~80 |
| 路线图 | `reference/changelog.md` | ~60 |

#### ARCHITECTURE-MCP.md (1,245行) → 拆分为 6 个文档
| 原章节 | 新文档 | 行数估计 |
|--------|--------|---------|
| 架构设计图 | `overview/architecture.md` | ~100 |
| Notion MCP 工具 | `integrations/notion/tools-reference.md` | ~180 |
| Google Calendar MCP | `integrations/google-calendar/tools-reference.md` | ~180 |
| Notion MCP 配置 | `integrations/notion/mcp-setup.md` | ~150 |
| Google Calendar 配置 | `integrations/google-calendar/mcp-setup.md` | ~150 |
| 完整工作流程 | `guides/developer-guide.md` | ~120 |

#### DEVELOPMENT.md (1,021行) → 拆分为 4 个文档
| 原章节 | 新文档 | 行数估计 |
|--------|--------|---------|
| 环境搭建 | `guides/quick-start.md` | ~100 |
| 开发工作流 | `guides/developer-guide.md` | ~150 |
| 数据库迁移 | `reference/database-schema.md` | ~80 |
| 代码示例 | `integrations/*/examples.md` | ~120/个 |

#### DEPLOYMENT.md (851行) → 拆分为 4 个文档
| 原章节 | 新文档 | 行数估计 |
|--------|--------|---------|
| Docker 部署 | `deployment/docker.md` | ~150 |
| K8s 部署 | `deployment/kubernetes.md` | ~180 |
| 环境变量 | `deployment/environment.md` | ~120 |
| 安全配置 | `deployment/security.md` | ~100 |

---

## 📝 文档模板

### 模板 1: 集成模块 README

```markdown
# {集成名称} 集成

**版本**: v1.0
**协议**: MCP (Model Context Protocol)

---

## 🎯 概述

简短描述（2-3句话）

---

## ✨ 核心特性

- 特性 1
- 特性 2
- 特性 3

---

## 🚀 快速开始

1. [配置步骤](./mcp-setup.md)
2. [工具参考](./tools-reference.md)
3. [使用示例](./examples.md)

---

## 📚 相关文档

- [上级文档链接]
- [相关集成链接]

---

**长度**: < 100 行
```

### 模板 2: 工具参考文档

```markdown
# {集成名称} MCP 工具参考

**共 {N} 个工具**

---

## 工具 1: tool_name()

**功能**: 一句话描述

**参数**:
```python
{
  "param1": "type",
  "param2": "type"
}
```

**示例**:
```python
result = await mcp.call_tool("tool_name", ...)
```

**返回**: 返回值说明

---

(重复 N 个工具)

---

**相关**: [配置文档](./mcp-setup.md) | [示例](./examples.md)
```

---

## ✅ 实施步骤

1. **创建新目录结构** (保留旧文档)
2. **拆分 ARCHITECTURE-MCP.md** → 6 个小文档
3. **拆分 PRD.md** → 9 个小文档
4. **拆分 DEVELOPMENT.md** → 4 个小文档
5. **拆分 DEPLOYMENT.md** → 4 个小文档
6. **创建 docs/INDEX.md** 总索引
7. **更新 README.md** 为简洁导航页
8. **移动旧文档到 docs/legacy/**
9. **更新所有内部链接**
10. **验证所有链接有效**

---

## 🎯 预期成果

- ✅ 每个文档 < 200 行
- ✅ 清晰的 3 层导航（索引 → 分类 → 具体文档）
- ✅ 模块化，易于扩展（新增集成只需加 1 个文件夹）
- ✅ 便于维护（修改单个模块不影响其他）
- ✅ 快速查找（通过 INDEX.md 快速定位）

---

**创建时间**: 2025-11-27
**状态**: 待实施
