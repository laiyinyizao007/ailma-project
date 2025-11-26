# 📚 AILMA 文档索引

**快速导航** - 通过这个索引快速找到你需要的文档

---

## 🚀 快速开始

**新用户从这里开始**：

1. [什么是 AILMA？](./overview/what-is-ailma.md) - 了解产品定位
2. [5分钟快速开始](./guides/quick-start.md) - 立即运行项目
3. [用户使用指南](./guides/user-guide.md) - 学习如何使用

---

## 📖 文档分类

### 概览层 - 理解 AILMA

| 文档 | 内容 | 时长 |
|------|------|------|
| [产品概览](./overview/what-is-ailma.md) | AILMA 是什么，解决什么问题 | 3 分钟 |
| [架构设计](./overview/architecture.md) | 系统架构图和核心组件 | 5 分钟 |
| [技术栈](./overview/tech-stack.md) | 技术选型和理由 | 3 分钟 |

---

### 🎓 指南层 - 学习使用

| 文档 | 适合人群 | 时长 |
|------|---------|------|
| [快速开始](./guides/quick-start.md) | 所有人 | 5 分钟 |
| [用户指南](./guides/user-guide.md) | 终端用户 | 10 分钟 |
| [开发者指南](./guides/developer-guide.md) | 开发者 | 15 分钟 |

---

### 🔌 集成模块 - 配置外部服务

#### Notion 集成 (MCP)

| 文档 | 内容 | 行数 |
|------|------|------|
| [Notion 概览](./integrations/notion/README.md) | Notion MCP 特性和优势 | ~80 |
| [MCP 配置](./integrations/notion/mcp-setup.md) | OAuth 和 MCP Server 配置 | ~150 |
| [工具参考](./integrations/notion/tools-reference.md) | 8个 MCP 工具详细说明 | ~180 |
| [使用示例](./integrations/notion/examples.md) | 实际代码示例 | ~120 |

#### Google Calendar 集成 (MCP)

| 文档 | 内容 | 行数 |
|------|------|------|
| [Google Calendar 概览](./integrations/google-calendar/README.md) | Google Calendar MCP 特性 | ~80 |
| [MCP 配置](./integrations/google-calendar/mcp-setup.md) | OAuth 和 MCP Server 配置 | ~150 |
| [工具参考](./integrations/google-calendar/tools-reference.md) | 7个 MCP 工具详细说明 | ~180 |
| [使用示例](./integrations/google-calendar/examples.md) | 实际代码示例 | ~120 |

#### Claude API 集成

| 文档 | 内容 | 行数 |
|------|------|------|
| [Claude API 配置](./integrations/claude/api-setup.md) | API Key 获取和配置 | ~80 |

---

### ⚙️ 功能模块 - 核心功能详解

| 文档 | 功能 | 行数 |
|------|------|------|
| [日历管理](./features/calendar-management.md) | 日历事件 CRUD，智能时间解析 | ~150 |
| [笔记管理](./features/note-taking.md) | Notion 笔记创建，Markdown 支持 | ~150 |
| [报告生成](./features/report-generation.md) | 周报、月报自动生成 | ~150 |
| [任务解析](./features/task-parsing.md) | NLP 意图识别，实体提取 | ~150 |

---

### 🚀 部署层 - 上线生产环境

| 文档 | 内容 | 行数 |
|------|------|------|
| [Docker 部署](./deployment/docker.md) | Docker Compose 配置 | ~150 |
| [Kubernetes 部署](./deployment/kubernetes.md) | K8s manifests | ~180 |
| [环境变量](./deployment/environment.md) | 所有环境变量详解 | ~120 |
| [安全配置](./deployment/security.md) | HTTPS, 加密，权限 | ~100 |

---

### 📡 API 参考 - 接口文档

| 文档 | 内容 | 行数 |
|------|------|------|
| [REST API](./api/rest-api.md) | 所有 HTTP 端点 | ~150 |
| [命令格式](./api/commands.md) | 自然语言命令规范 | ~100 |
| [Webhooks](./api/webhooks.md) | Webhook 配置 | ~80 |
| [错误码](./api/errors.md) | 错误码参考表 | ~80 |

---

### 📚 参考资料 - 深入了解

| 文档 | 内容 | 行数 |
|------|------|------|
| [MCP 协议](./reference/mcp-protocol.md) | Model Context Protocol 说明 | ~100 |
| [数据库 Schema](./reference/database-schema.md) | PostgreSQL 表结构 | ~100 |
| [故障排查](./reference/troubleshooting.md) | 常见问题和解决方案 | ~150 |
| [术语表](./reference/glossary.md) | 专业术语解释 | ~60 |
| [变更日志](./reference/changelog.md) | 版本历史 | ~80 |

---

## 🗺️ 学习路径

### 路径 1: 终端用户（5分钟）

```
1. 产品概览 → 2. 快速开始 → 3. 用户指南
```

### 路径 2: 开发者（30分钟）

```
1. 产品概览 → 2. 架构设计 → 3. 快速开始
   ↓
4. 开发者指南 → 5. Notion MCP 配置 → 6. Google Calendar MCP 配置
```

### 路径 3: DevOps（20分钟）

```
1. 快速开始 → 2. 环境变量 → 3. Docker 部署
   ↓
4. 安全配置 → 5. K8s 部署（可选）
```

### 路径 4: 贡献者（1小时）

```
1. 架构设计 → 2. 技术栈 → 3. 开发者指南
   ↓
4. 所有集成模块 → 5. API 参考 → 6. 数据库 Schema
```

---

## 🔍 按需查找

### 我想...

- **配置 Notion** → [Notion MCP 配置](./integrations/notion/mcp-setup.md)
- **配置 Google Calendar** → [Google Calendar MCP 配置](./integrations/google-calendar/mcp-setup.md)
- **部署到生产** → [Docker 部署](./deployment/docker.md)
- **了解 API** → [REST API 文档](./api/rest-api.md)
- **解决错误** → [故障排查](./reference/troubleshooting.md)
- **理解架构** → [架构设计](./overview/architecture.md)
- **查看示例** → [Notion 示例](./integrations/notion/examples.md) | [Calendar 示例](./integrations/google-calendar/examples.md)

---

## 📦 旧文档（归档）

大型单体文档已拆分为小模块，旧版本保存在 [`legacy/`](./legacy/) 目录：

- [PRD.md (旧)](./legacy/PRD.md) - 已拆分为 overview + features
- [ARCHITECTURE-MCP.md (旧)](./legacy/ARCHITECTURE-MCP.md) - 已拆分为 overview + integrations
- [DEVELOPMENT.md (旧)](./legacy/DEVELOPMENT.md) - 已拆分为 guides
- [DEPLOYMENT.md (旧)](./legacy/DEPLOYMENT.md) - 已拆分为 deployment

---

## 💡 文档规范

所有新文档遵循以下规范：

- ✅ **长度**: 每个文档 < 200 行
- ✅ **职责**: 每个文档只讲一件事
- ✅ **链接**: 相关文档互相链接
- ✅ **模板**: 使用统一模板格式
- ✅ **更新**: 修改日期在文档末尾

---

**最后更新**: 2025-11-27
**文档版本**: v2.0 (模块化重构)
**总文档数**: 30+ 个小文档

