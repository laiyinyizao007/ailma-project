# AILMA - AI 智能生活管理助手

**用自然语言管理你的日历和笔记**

---

## 🎯 这是什么？

在 **Notion** 中输入：
```
"明天下午3点和团队开会讨论Q1规划"
```

**AILMA 自动**：
- ✅ 在 Google Calendar 创建事件
- ✅ 在 Notion 生成会议纪要页面
- ✅ 生成 Google Meet 链接
- ✅ 10秒完成

---

## ⚡ 核心特性

- **自然语言交互** - 不需要学习命令，用口语即可
- **Notion 作为界面** - 零 UI 开发，利用 Notion 强大功能
- **MCP 驱动集成** - Notion + Google Calendar 双 MCP
- **AI 生成报告** - 自动生成周报、月报
- **高度可扩展** - 模块化架构，易于添加新集成

---

## 📖 文档导航

### 🚀 快速开始（5分钟）
1. [什么是 AILMA？](./docs/overview/what-is-ailma.md) - 产品介绍
2. [快速开始指南](./docs/guides/quick-start.md) - 立即运行
3. [用户使用指南](./docs/guides/user-guide.md) - 学习使用

### 📚 完整文档
访问 **[文档总索引](./docs/INDEX.md)** 查找所有文档

### 🔗 快速链接
| 你想... | 访问 |
|---------|------|
| 了解产品 | [产品概览](./docs/overview/what-is-ailma.md) |
| 运行项目 | [快速开始](./docs/guides/quick-start.md) |
| 配置 Notion | [Notion MCP 配置](./docs/integrations/notion/mcp-setup.md) |
| 配置 Google Calendar | [Google Calendar MCP 配置](./docs/integrations/google-calendar/mcp-setup.md) |
| 理解架构 | [架构设计](./docs/overview/architecture.md) |
| 部署上线 | [Docker 部署](./docs/deployment/docker.md) |
| 解决问题 | [故障排查](./docs/reference/troubleshooting.md) |

---

## 🏗️ 架构速览

```
Notion (前端)
    ↓ MCP
Backend (FastAPI + AI)
    ↓ MCP
Google Calendar + Notion (数据)
```

**详细**: [完整架构文档](./docs/overview/architecture.md)

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Notion Workspace |
| 后端 | Python 3.11 + FastAPI |
| AI | LangChain + Claude API |
| 集成 | MCP (Notion + Google Calendar) |
| 数据库 | PostgreSQL 15 + Redis 7 |
| 部署 | Docker + Kubernetes |

**详细**: [技术栈文档](./docs/overview/tech-stack.md)

---

## 📦 项目结构

```
ailma-project/
├── docs/                  # 📚 模块化文档（30+ 小文档）
│   ├── INDEX.md           # 总索引
│   ├── overview/          # 产品概览
│   ├── guides/            # 使用指南
│   ├── integrations/      # 集成配置
│   ├── features/          # 功能说明
│   ├── deployment/        # 部署文档
│   └── reference/         # 参考资料
│
├── backend/               # Python 后端代码
│   ├── adapters/          # MCP 客户端
│   ├── core/              # AI 核心
│   └── api/               # REST API
│
├── tests/                 # 测试代码
│   └── mcp_integration/   # MCP 集成测试
│
├── docker/                # Docker 配置
├── .env.example           # 环境变量模板
└── README.md              # 本文件
```

---

## 🚀 5 分钟快速开始

### 1. 克隆项目
```bash
git clone https://github.com/your-org/ailma-project.git
cd ailma-project
```

### 2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 填入你的 API Keys
```

### 3. 启动服务
```bash
docker-compose up -d
```

### 4. 测试连接
```bash
# 测试 Notion 连接
python tests/mcp_integration/notion/test_connection.py

# 测试 Google Calendar 连接
python tests/mcp_integration/google_calendar/test_connection.py
```

### 5. 开始使用
在 Notion "指令中心"输入指令，AILMA 自动执行！

**详细步骤**: [完整快速开始指南](./docs/guides/quick-start.md)

---

## 💡 使用示例

### 创建日历事件
```
# 在 Notion 输入
"明天下午3点和产品团队开会"

# AILMA 自动创建
✅ Google Calendar 事件
✅ Notion 会议纪要页面
✅ Google Meet 链接
```

### 生成工作报告
```
# 在 Notion 输入
"生成本周工作报告"

# AILMA 自动生成
📊 包含会议统计、任务完成度、时间分析的 Markdown 报告
```

**更多示例**:
- [Notion 使用示例](./docs/integrations/notion/examples.md)
- [Google Calendar 使用示例](./docs/integrations/google-calendar/examples.md)

---

## 🤝 贡献

我们欢迎贡献！请查看：
- [贡献指南](./CONTRIBUTING.md)
- [开发者指南](./docs/guides/developer-guide.md)

---

## 📄 许可证

MIT License - 详见 [LICENSE](./LICENSE)

---

## 🔗 相关资源

### MCP 生态
- [Notion MCP](https://github.com/pbohannon/notion-api-mcp)
- [Google Calendar MCP](https://github.com/nspady/google-calendar-mcp)
- [MCP 协议](https://modelcontextprotocol.io/)

### API 文档
- [Claude API](https://docs.anthropic.com/)
- [FastAPI](https://fastapi.tiangolo.com/)

---

## 📞 联系我们

- 📧 Email: support@ailma.ai
- 💬 Discord: [加入社区](https://discord.gg/ailma)
- 🐛 Issues: [GitHub Issues](https://github.com/your-org/ailma-project/issues)

---

**Built with ❤️ by the AILMA Team**

**文档版本**: v2.0 (模块化架构)
**最后更新**: 2025-11-27

