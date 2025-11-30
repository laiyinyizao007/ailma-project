# AILMA 开发环境设置指南

本文档提供详细的开发环境设置步骤。

---

## 📋 前置要求

- Python 3.10+
- Git
- 虚拟环境（venv）

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/laiyinyizao007/ailma-project.git
cd ailma-project
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

**重要**: 如果你的系统配置了代理，可能需要使用 `--proxy=""` 参数：

```bash
# 标准安装
pip install -r requirements.txt

# 如果遇到代理错误，使用以下命令：
pip install --proxy="" -r requirements.txt
```

### 4. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API Keys
```

必需的环境变量：
- `NOTION_API_KEY` - Notion Integration Token
- `ANTHROPIC_API_KEY` - Claude API Key
- `GOOGLE_CALENDAR_MCP_SERVER_URL` - Google Calendar MCP Server URL

### 5. 运行测试

```bash
# 使用 pytest 直接运行
pytest tests/

# 或使用提供的脚本
./scripts/run-tests.sh

# 运行特定类型的测试
pytest tests/ai/                    # 只运行 AI 模块测试
pytest tests/integration/           # 只运行集成测试
pytest tests/e2e/                   # 只运行 E2E 测试

# 查看测试覆盖率
pytest tests/ --cov=src --cov-report=html
```

### 6. 启动应用

```bash
# 开发模式
python -m uvicorn src.main:app --reload

# 或使用 Docker
docker-compose up -d
```

---

## 🔧 常见问题

### 问题 1: pip 安装失败（代理错误）

**错误信息**:
```
OSError: Failed to parse: [user-passwd@]127.0.0.1:63196
```

**解决方案**:
```bash
pip install --proxy="" -r requirements.txt
```

### 问题 2: 测试无法找到 src 模块

**错误信息**:
```
ModuleNotFoundError: No module named 'src'
```

**解决方案**:
项目已包含 `pytest.ini` 配置文件，会自动将项目根目录添加到 Python 路径。如果问题仍然存在：

```bash
# 手动设置 PYTHONPATH
export PYTHONPATH=/path/to/ailma-project
pytest tests/
```

### 问题 3: MCP 包找不到

**解决方案**:
MCP (Model Context Protocol) 包现在可以从 PyPI 安装：
```bash
pip install --proxy="" mcp
```

---

## 📦 已安装的关键包

| 包名 | 版本 | 用途 |
|------|------|------|
| fastapi | 0.122.0 | Web 框架 |
| anthropic | 0.75.0 | Claude API 客户端 |
| langchain | 1.1.0 | LLM 框架 |
| mcp | 1.22.0 | Model Context Protocol SDK |
| pytest | 9.0.1 | 测试框架 |
| pydantic | 2.12.5 | 数据验证 |
| sqlalchemy | 2.0.44 | ORM |
| redis | 7.1.0 | 缓存客户端 |
| celery | 5.5.3 | 异步任务队列 |

完整列表见 `requirements.txt`

---

## 🐳 Docker 部署

### 使用 Docker Compose（推荐）

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f ailma

# 停止服务
docker-compose down
```

### 单独使用 Docker

```bash
# 构建镜像
docker build -t ailma:latest .

# 运行容器
docker run -d \
  --name ailma \
  -p 8000:8000 \
  --env-file .env \
  ailma:latest
```

---

## 📝 开发工作流

### 1. 创建新功能分支

```bash
git checkout -b feature/your-feature-name
```

### 2. 开发和测试

```bash
# 运行测试
pytest tests/

# 代码格式化
black src/ tests/
ruff check src/ tests/

# 类型检查
mypy src/
```

### 3. 提交代码

```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

### 4. 创建 Pull Request

访问 GitHub 仓库创建 PR

---

## 🧪 测试覆盖率

当前测试覆盖率：**34%**

目标：**80%+**

查看详细覆盖率报告：
```bash
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
```

---

## 📚 相关文档

- [README.md](./README.md) - 项目概述
- [PROGRESS.md](./PROGRESS.md) - 项目进度
- [docs/INDEX.md](./docs/INDEX.md) - 完整文档索引
- [CONTRIBUTING.md](./CONTRIBUTING.md) - 贡献指南

---

## 🆘 获取帮助

- 查看文档: [docs/](./docs/)
- 提交 Issue: [GitHub Issues](https://github.com/laiyinyizao007/ailma-project/issues)
- 查看故障排查: [docs/reference/troubleshooting.md](./docs/reference/troubleshooting.md)

---

**最后更新**: 2025-11-30
