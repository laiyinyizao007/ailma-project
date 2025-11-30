# API Keys 获取和配置指南

本文档提供详细的 API Keys 获取步骤，帮助你快速配置 AILMA 项目。

---

## 📋 需要的 API Keys 清单

| API | 必需性 | 用途 | 预计时间 |
|-----|-------|------|----------|
| ✅ **Notion API** | 必需 | 连接 Notion 工作区 | 5 分钟 |
| ✅ **Claude API** | 必需 | AI 意图识别和实体提取 | 5 分钟 |
| ⚠️ **Google Calendar** | 推荐 | 日历事件管理 | 10-15 分钟 |
| 📊 **PostgreSQL** | 可选 | 数据持久化（可用 SQLite） | - |
| 📦 **Redis** | 可选 | 缓存（可禁用） | - |

---

## 1️⃣ Notion API Key

### 步骤 1: 创建 Notion Integration

1. 访问 **[Notion Integrations](https://www.notion.so/my-integrations)**
2. 点击 **"+ New integration"**
3. 填写信息：
   - **Name**: `AILMA Development` （或任意名称）
   - **Associated workspace**: 选择你的工作区
   - **Type**: Internal integration
4. 设置权限（Capabilities）：
   - ✅ **Read content**
   - ✅ **Update content**
   - ✅ **Insert content**
   - ⚠️ 不需要 "Read user information"（除非你需要）
5. 点击 **"Submit"**

### 步骤 2: 复制 Integration Token

1. 在 Integration 页面，找到 **"Internal Integration Token"**
2. 点击 **"Show"** 并复制 token
3. Token 格式：`secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 步骤 3: 分享页面/数据库给 Integration

**重要**：必须将你的 Notion 页面或数据库分享给 Integration，否则无法访问。

1. 打开你要使用的 Notion 页面/数据库
2. 点击右上角 **"..."** → **"Add connections"**
3. 搜索并选择你刚创建的 Integration（如 `AILMA Development`）
4. 点击 **"Confirm"**

### 步骤 4: 配置到 .env

```bash
# 编辑 .env 文件
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 步骤 5: 获取数据库 ID（可选）

如果你需要配置特定数据库：

1. 打开 Notion 数据库页面
2. 复制页面 URL，格式：
   ```
   https://www.notion.so/workspace/database-id?v=view-id
                                    ^^^^^^^^^^^^^^^^
   ```
3. 提取 `database-id` 部分（32位字符）
4. 配置到 .env：
   ```bash
   COMMAND_CENTER_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## 2️⃣ Claude API Key (Anthropic)

### 步骤 1: 注册 Anthropic 账号

1. 访问 **[Anthropic Console](https://console.anthropic.com/)**
2. 使用 Google/Email 注册账号
3. 验证邮箱

### 步骤 2: 创建 API Key

1. 登录后访问 **[API Keys](https://console.anthropic.com/settings/keys)**
2. 点击 **"Create Key"**
3. 填写信息：
   - **Name**: `AILMA Development`
   - **Workspace**: 选择默认 workspace
4. 点击 **"Create Key"**
5. **立即复制 API Key**（只显示一次！）

### 步骤 3: 配置到 .env

```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 步骤 4: 配置额度（可选）

1. 访问 **[Billing](https://console.anthropic.com/settings/billing)**
2. 添加支付方式
3. 推荐设置用量限制：
   - **Daily limit**: $5-10（开发测试足够）
   - **Monthly limit**: $50-100

### 可用模型

AILMA 默认使用 `claude-3-sonnet-20240229`，你也可以选择：

| 模型 | 性能 | 成本 | 推荐场景 |
|------|------|------|----------|
| `claude-3-opus-20240229` | 最强 | 最高 | 生产环境 |
| `claude-3-sonnet-20240229` | 均衡 | 中等 | **开发推荐** ✅ |
| `claude-3-haiku-20240307` | 快速 | 最低 | 简单任务 |

```bash
# 在 .env 中配置
LLM_MODEL=claude-3-sonnet-20240229
```

---

## 3️⃣ Google Calendar API（可选但推荐）

### 方式 1: 使用社区 MCP Server（推荐）

**优势**：无需自己处理 OAuth，MCP Server 帮你管理

1. 克隆 MCP Server：
   ```bash
   git clone https://github.com/nspady/google-calendar-mcp.git
   cd google-calendar-mcp
   npm install
   ```

2. 配置 Google OAuth（参考该项目 README）

3. 启动 MCP Server：
   ```bash
   npm start
   # 默认运行在 http://localhost:3000/mcp
   ```

4. 配置到 .env：
   ```bash
   GOOGLE_CALENDAR_MCP_SERVER_URL=http://localhost:3000/mcp
   ```

### 方式 2: 直接使用 Google Calendar API

如果你想自己管理 OAuth：

#### 步骤 1: 创建 Google Cloud 项目

1. 访问 **[Google Cloud Console](https://console.cloud.google.com/)**
2. 创建新项目：
   - **Project name**: `AILMA`
   - **Organization**: 个人账号留空
3. 点击 **"Create"**

#### 步骤 2: 启用 Google Calendar API

1. 在项目中，访问 **[API Library](https://console.cloud.google.com/apis/library)**
2. 搜索 **"Google Calendar API"**
3. 点击并启用

#### 步骤 3: 创建 OAuth 2.0 Credentials

1. 访问 **[Credentials](https://console.cloud.google.com/apis/credentials)**
2. 点击 **"Create Credentials"** → **"OAuth client ID"**
3. 如果提示配置同意屏幕：
   - User Type: **External**
   - App name: `AILMA`
   - Support email: 你的邮箱
   - Scopes: 添加 `.../auth/calendar`
4. 创建 OAuth Client：
   - Application type: **Desktop app**
   - Name: `AILMA Desktop Client`
5. 下载 credentials.json

#### 步骤 4: 配置到 .env

```bash
GOOGLE_CLIENT_ID=xxxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxxxxxxxxxx
```

#### 步骤 5: 首次运行获取 OAuth Token

运行应用时会自动打开浏览器进行授权，授权后 token 会自动保存。

---

## 4️⃣ 数据库配置（可选）

### PostgreSQL（生产推荐）

**使用 Docker Compose（最简单）**：

```bash
# docker-compose.yml 已包含 PostgreSQL
docker-compose up -d postgres

# 连接字符串已配置
DATABASE_URL=postgresql://ailma:password@localhost:5432/ailma
```

**本地安装**：

```bash
# Ubuntu/Debian
sudo apt-get install postgresql

# macOS
brew install postgresql

# 创建数据库
createdb ailma

# 配置 .env
DATABASE_URL=postgresql://username:password@localhost:5432/ailma
```

### Redis（缓存，可选）

**使用 Docker Compose**：

```bash
docker-compose up -d redis

# 连接字符串已配置
REDIS_URL=redis://localhost:6379/0
```

**本地安装**：

```bash
# Ubuntu/Debian
sudo apt-get install redis

# macOS
brew install redis

# 启动
redis-server
```

---

## 5️⃣ 安全配置

### 生成 SECRET_KEY

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# 或 OpenSSL
openssl rand -base64 32
```

配置到 .env：
```bash
SECRET_KEY=your-generated-secret-key-here
```

### 生成 ENCRYPTION_KEY

```bash
# 生成 32 字节的 base64 密钥
python -c "import base64, os; print(base64.b64encode(os.urandom(32)).decode())"
```

配置到 .env：
```bash
ENCRYPTION_KEY=your-base64-encoded-32-byte-key
```

---

## ✅ 验证配置

### 最小可运行配置

只需要这 2 个 API Keys 就可以运行基础功能：

```bash
# .env 最小配置
NOTION_API_KEY=secret_xxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxx

# 其他使用默认值
DEBUG=True
ENVIRONMENT=development
PORT=8000
LOG_LEVEL=INFO
```

### 完整配置检查脚本

创建验证脚本 `scripts/check-config.sh`：

```bash
#!/bin/bash
echo "检查环境变量配置..."

# 检查必需的 API Keys
if [ -z "$NOTION_API_KEY" ]; then
    echo "❌ NOTION_API_KEY 未设置"
else
    echo "✅ NOTION_API_KEY 已设置"
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ ANTHROPIC_API_KEY 未设置"
else
    echo "✅ ANTHROPIC_API_KEY 已设置"
fi

# 检查可选配置
if [ -z "$GOOGLE_CALENDAR_MCP_SERVER_URL" ]; then
    echo "⚠️  GOOGLE_CALENDAR_MCP_SERVER_URL 未设置（可选）"
else
    echo "✅ GOOGLE_CALENDAR_MCP_SERVER_URL 已设置"
fi
```

运行验证：
```bash
source venv/bin/activate
source .env
bash scripts/check-config.sh
```

### Python 验证脚本

```python
# scripts/test-api-connections.py
import os
from dotenv import load_dotenv

load_dotenv()

def test_notion():
    from notion_client import Client
    notion = Client(auth=os.getenv("NOTION_API_KEY"))
    try:
        notion.users.me()
        print("✅ Notion API 连接成功")
    except Exception as e:
        print(f"❌ Notion API 连接失败: {e}")

def test_claude():
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print("✅ Claude API 连接成功")
    except Exception as e:
        print(f"❌ Claude API 连接失败: {e}")

if __name__ == "__main__":
    print("测试 API 连接...\n")
    test_notion()
    test_claude()
```

运行：
```bash
python scripts/test-api-connections.py
```

---

## 🔒 安全最佳实践

### 1. 永远不要提交 .env 文件

`.gitignore` 已包含 `.env`，但请再次确认：

```bash
# 检查 .env 是否在 .gitignore 中
grep ".env" .gitignore
```

### 2. 使用环境变量管理工具

生产环境推荐使用：
- **Docker Secrets**（Docker Swarm）
- **Kubernetes Secrets**（K8s）
- **AWS Secrets Manager**（AWS）
- **HashiCorp Vault**（企业级）

### 3. API Key 权限最小化

- Notion: 只授权必要的页面/数据库
- Claude: 设置用量限制
- Google: 只请求必要的 scopes

### 4. 定期轮换 Keys

- 开发环境：每月轮换
- 生产环境：每周轮换
- 泄露后：立即撤销并重新生成

---

## 📞 获取帮助

### API Keys 相关问题

- **Notion**: [Notion 开发者文档](https://developers.notion.com/)
- **Claude**: [Anthropic 支持](https://support.anthropic.com/)
- **Google Calendar**: [Google Calendar API 文档](https://developers.google.com/calendar/api)

### 项目相关问题

- 查看 [故障排查](../reference/troubleshooting.md)
- 提交 [GitHub Issue](https://github.com/laiyinyizao007/ailma-project/issues)

---

## 📊 成本估算

### 开发/测试阶段（每月）

| 服务 | 免费额度 | 预计成本 |
|------|---------|---------|
| **Notion API** | 无限制 | $0 |
| **Claude API** | - | $10-20 |
| **Google Calendar** | 无限制 | $0 |
| **PostgreSQL** | Docker 本地 | $0 |
| **Redis** | Docker 本地 | $0 |
| **总计** | - | **$10-20** |

### 生产环境（每月，100 活跃用户）

| 服务 | 预计成本 |
|------|---------|
| **Claude API** | $50-100 |
| **数据库托管** | $10-20 |
| **Redis 托管** | $10-15 |
| **服务器** | $20-50 |
| **总计** | **$90-185** |

---

**最后更新**: 2025-11-30
**版本**: v1.0
