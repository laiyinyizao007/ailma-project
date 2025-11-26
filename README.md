# AILMA - AI Life Management Assistant

**AI 智能生活管理助手**

一款基于自然语言交互的智能生活管理中枢，通过 AI 驱动的任务解析和自动化执行，帮助用户高效管理跨平台的日程、笔记和数据总结。

---

## 🎯 核心特性

- ✅ **自然语言交互**: 用口语化指令完成所有操作
- ✅ **Notion 作为前端**: 零 UI 开发，利用 Notion 强大的数据库能力
- ✅ **Notion MCP 集成**: 使用 Model Context Protocol 实现标准化、高效的 Notion 集成
- ✅ **智能任务解析**: AI 自动识别意图，无需记忆复杂命令
- ✅ **多平台集成**: 统一管理 Google Calendar、Notion 等服务
- ✅ **自动化报告生成**: AI 驱动的数据分析和结构化报告
- ✅ **Markdown 原生支持**: 报告和笔记使用 Markdown 格式，AI 友好

---

## 📖 快速导航

- **[项目状态报告](./STATUS.md)** 🆕 - 当前进度和下一步行动
- **[产品需求文档 (PRD)](./docs/PRD.md)** - 完整的产品定义和功能需求
- **[Notion MCP 架构设计](./docs/ARCHITECTURE-MCP.md)** ⭐ **推荐** - 使用 MCP 的现代化架构
- **[Notion 连接测试](./tests/mcp_integration/QUICKSTART.md)** 🧪 - 测试 Notion 集成
- **[项目结构说明](./docs/PROJECT-STRUCTURE.md)** - 代码组织和模块设计（旧方案参考）
- **[开发指南](./docs/DEVELOPMENT.md)** - 环境搭建和开发流程（待创建）
- **[API 文档](./docs/API.md)** - RESTful API 接口说明（待创建）
- **[部署指南](./docs/DEPLOYMENT.md)** - 生产环境部署步骤（待创建）

---

## 🚀 快速开始

### 前置要求

- Python 3.11+
- Docker 24.0+
- PostgreSQL 15+
- Redis 7+

### 1. 克隆项目

```bash
git clone https://github.com/your-org/ailma-project.git
cd ailma-project
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填写以下关键配置：
# - ANTHROPIC_API_KEY (Claude API Key)
# - NOTION_DEFAULT_TOKEN (Notion Integration Token)
# - GOOGLE_CLIENT_ID 和 GOOGLE_CLIENT_SECRET
nano .env
```

### 3. 启动服务

```bash
# 使用 Docker Compose 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f backend
```

### 4. 访问应用

- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health
- **Notion 工作区**: 在您的 Notion 中使用预配置的数据库

---

## 📋 使用示例

### 在 Notion 中创建指令

1. 打开您的 **AILMA 指令中心** 数据库
2. 新增一行，输入指令：

```
指令: 帮我把明天下午3点的团队会议加到日历
状态: Pending
```

3. 等待 30 秒（轮询周期），后端会自动处理
4. 状态更新为 `Done`，结果字段显示：`✅ 已成功创建事件：团队会议`

### 生成周报

```
指令: 生成本周工作总结报告
状态: Pending
```

系统会自动：
1. 从 Google Calendar 获取本周所有日程
2. 从 Notion 获取本周完成的任务
3. 使用 AI 生成结构化报告
4. 创建新的 Notion 页面并保存报告
5. 在结果字段返回页面链接

---

## 🏗️ 架构概览（Notion MCP 版）

```
┌─────────────────────────────┐
│   Notion Workspace          │
│   • 指令中心 Database        │
│   • 日程视图 Database        │
│   • 报告归档 Database        │
└────────────┬────────────────┘
             │ Notion MCP Protocol
             │ (Markdown-based)
             ▼
┌─────────────────────────────┐
│   Backend Service           │
│   • Notion MCP Client       │
│   • AI Core (Task Parser)   │
│   • Task Executor           │
│   • Report Generator        │
│   • Calendar Adapter        │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│   External Services         │
│   • Notion MCP Server       │
│   • Google Calendar API     │
│   • Anthropic Claude API    │
└─────────────────────────────┘
```

**为什么使用 Notion MCP？**
- ✅ **Markdown 原生支持** - AI 生成内容可直接写入，无需复杂转换
- ✅ **降低 50% 代码量** - 标准化协议替代手写 API 封装
- ✅ **OAuth 托管** - 无需自行管理认证逻辑
- ✅ **开放标准** - 生态兼容，长期稳定

详细架构请参考 **[Notion MCP 架构文档](./docs/ARCHITECTURE-MCP.md)**。

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| **后端框架** | Python 3.11 + FastAPI |
| **AI/NLP** | LangChain + Anthropic Claude API |
| **Notion 集成** | **Notion MCP (Model Context Protocol)** ⭐ |
| **数据库** | PostgreSQL 15 |
| **缓存** | Redis 7 |
| **任务队列** | Celery |
| **容器化** | Docker + Docker Compose |
| **外部集成** | Notion MCP Server, Google Calendar API |

---

## 📦 项目结构

```
ailma-project/
├── backend/               # 后端服务
│   ├── api/              # FastAPI 路由
│   ├── core/             # 核心业务逻辑
│   │   ├── ai/           # AI 模块（Task Parser, Report Generator）
│   │   └── executor.py   # 任务执行器
│   ├── adapters/         # 外部服务适配器
│   ├── listeners/        # Notion 监听器
│   ├── models/           # 数据模型
│   └── main.py           # 应用入口
├── tests/                # 测试文件
├── docs/                 # 文档
│   ├── PRD.md           # 产品需求文档
│   └── PROJECT-STRUCTURE.md
├── docker-compose.yml    # Docker 编排
├── requirements.txt      # Python 依赖
└── README.md            # 本文件
```

完整结构说明：[PROJECT-STRUCTURE.md](./docs/PROJECT-STRUCTURE.md)

---

## 🧪 开发

### 安装开发依赖

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements-dev.txt
```

### 运行测试

```bash
# 运行所有测试
pytest

# 生成覆盖率报告
pytest --cov=backend --cov-report=html
```

### 代码格式化

```bash
# 格式化代码
black backend/
isort backend/

# 代码检查
flake8 backend/
mypy backend/
```

---

## 📊 开发路线图

### Phase 1: MVP (4-6 周) ✅ 当前阶段

- [x] 项目初始化和架构设计
- [ ] 数据库 Schema 和模型
- [ ] Notion/Calendar 基础集成
- [ ] AI 核心（Task Parser）
- [ ] 日历事件 CRUD
- [ ] 周报生成功能

### Phase 2: 功能完善 (6-8 周)

- [ ] Outlook Calendar 支持
- [ ] 多日历账户管理
- [ ] 月报和项目报告模板
- [ ] 性能优化（缓存、异步）
- [ ] 用户体验优化

### Phase 3: 生态扩展 (8-12 周)

- [ ] Todoist 集成
- [ ] Slack 通知
- [ ] Trello/Asana 集成
- [ ] 智能建议系统
- [ ] 企业版功能

详细路线图：[PRD.md - 路线图](./docs/PRD.md#路线图)

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 📞 联系方式

- **项目主页**: https://github.com/your-org/ailma-project
- **问题反馈**: https://github.com/your-org/ailma-project/issues
- **邮箱**: ailma-support@example.com

---

## 🙏 致谢

感谢以下开源项目和服务：

- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://python.langchain.com/)
- [Anthropic Claude](https://www.anthropic.com/)
- [Notion MCP](https://developers.notion.com/docs/mcp)
- [Model Context Protocol](http://blog.modelcontextprotocol.io/)
- [Google Calendar API](https://developers.google.com/calendar)

---

**Built with ❤️ by the AILMA Team**

---

## 📚 相关资源

- [Notion MCP 官方文档](https://developers.notion.com/docs/mcp)
- [Model Context Protocol 规范](http://blog.modelcontextprotocol.io/)
- [Google Calendar API 指南](https://developers.google.com/calendar/api/guides/overview)
- [Claude API 文档](https://docs.anthropic.com/)
- [FastAPI 教程](https://fastapi.tiangolo.com/tutorial/)
- [Python Notion MCP 实现](https://github.com/pbohannon/notion-api-mcp)
