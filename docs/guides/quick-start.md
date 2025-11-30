# 🚀 AILMA 快速开始指南

5 分钟快速部署和使用 AILMA

---

## 前置条件

- Python 3.11+
- Docker & Docker Compose (可选)
- Notion 账号
- Google 账号
- Anthropic API Key

---

## 步骤 1: 克隆项目

```bash
cd ~/projects
git clone <your-repo-url> ailma-project
cd ailma-project
```

---

## 步骤 2: 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填写以下信息
vim .env
```

### 必填配置

```bash
# Notion
NOTION_API_KEY=secret_your_notion_token
COMMAND_CENTER_DB_ID=your_database_id

# Claude
ANTHROPIC_API_KEY=sk-ant-your_key

# Google Calendar
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your_secret
```

---

## 步骤 3: 启动服务

### 选项 A: Docker (推荐)

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f ailma

# 检查服务状态
curl http://localhost:8000/health
```

### 选项 B: 本地运行

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 步骤 4: 配置 Notion Command Center

### 4.1 创建数据库

在 Notion 中创建一个新数据库，命名为 "AILMA Command Center"

### 4.2 添加必需属性

| 属性名 | 类型 | 说明 |
|--------|------|------|
| Command | Title | 用户指令 |
| Status | Select | pending, processing, completed, failed, needs_clarification |
| Result | Text | 执行结果 |
| Error | Text | 错误信息 |
| Created | Date | 创建时间 |
| Updated | Date | 更新时间 |

### 4.3 共享数据库给 Integration

1. 打开数据库
2. 点击右上角 "•••"
3. 选择 "Add connections"
4. 选择你的 AILMA Integration

---

## 步骤 5: 测试

### 测试 1: 健康检查

```bash
curl http://localhost:8000/health
```

期望输出:
```json
{
  "status": "healthy",
  "components": {
    "listener": true,
    "last_check": "2025-11-27T10:00:00"
  }
}
```

### 测试 2: 手动解析指令

```bash
curl -X POST http://localhost:8000/api/parse \
  -H "Content-Type: application/json" \
  -d '{"text": "明天下午3点开会"}'
```

期望输出:
```json
{
  "intent": {
    "type": "calendar_create",
    "confidence": 0.95
  },
  "entities": {
    "title": "开会",
    "time": {
      "start": "2025-11-28T15:00:00",
      "is_all_day": false
    }
  }
}
```

### 测试 3: 在 Notion 中创建指令

1. 在 Command Center 数据库中添加新行
2. Command 列输入: "明天下午3点团队会议"
3. Status 设置为: pending
4. 等待 30 秒（默认轮询间隔）
5. 观察 Status 变化: pending → processing → completed
6. 检查 Google Calendar 是否创建了事件

---

## 常见问题

### Q: Listener 没有轮询？

**A**: 检查日志:
```bash
docker-compose logs ailma | grep "Notion Listener"
```

### Q: 无法连接 Google Calendar？

**A**: 确保 Google Calendar MCP Server 已启动:
```bash
# 检查 MCP Server 状态
curl http://localhost:3000/health
```

### Q: Notion 权限错误？

**A**: 确保:
1. Integration 已创建
2. 数据库已共享给 Integration
3. NOTION_API_KEY 正确

---

## 下一步

- [用户使用指南](./user-guide.md) - 详细功能说明
- [Notion MCP 配置](../integrations/notion/README.md) - Notion 集成详解
- [Google Calendar MCP 配置](../integrations/google-calendar/README.md) - 日历集成详解

---

**最后更新**: 2025-11-27
