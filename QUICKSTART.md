# AILMA 快速开始指南

10 分钟内启动 AILMA 项目！

---

## 🚀 3 步快速开始

### 步骤 1: 安装依赖（2 分钟）

```bash
# 克隆项目
cd /home/averyubuntu/projects/ailma-project

# 激活虚拟环境
source venv/bin/activate

# 依赖已安装 ✅
# 如需重新安装: pip install --proxy="" -r requirements.txt
```

### 步骤 2: 配置 API Keys（5 分钟）

```bash
# 1. 复制环境变量模板（已完成 ✅）
# cp .env.example .env

# 2. 编辑 .env 文件
nano .env  # 或使用你喜欢的编辑器
```

**最小配置（只需这 2 个）**：

```bash
# 获取 Notion API Key: https://www.notion.so/my-integrations
NOTION_API_KEY=secret_your_actual_token_here

# 获取 Claude API Key: https://console.anthropic.com/settings/keys
ANTHROPIC_API_KEY=sk-ant-your_actual_key_here
```

**详细配置指南**：查看 [docs/guides/api-keys-setup.md](./docs/guides/api-keys-setup.md)

### 步骤 3: 验证配置（1 分钟）

```bash
# 检查配置
./scripts/check-config.sh

# 测试 API 连接
python scripts/test-api-connections.py
```

---

## ✅ 启动应用

### 方式 1: 直接运行（开发推荐）

```bash
source venv/bin/activate
python -m uvicorn src.main:app --reload
```

访问: http://localhost:8000

### 方式 2: Docker（生产推荐）

```bash
docker-compose up -d
```

访问: http://localhost:8000

---

## 🧪 运行测试

```bash
# 运行所有测试
./scripts/run-tests.sh

# 或直接使用 pytest
pytest tests/

# 查看覆盖率报告
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

---

## 📖 下一步

### 配置 Notion

1. 创建 Notion Integration: https://www.notion.so/my-integrations
2. 创建 3 个数据库:
   - **指令中心** - 接收用户命令
   - **日历数据库** - 存储事件记录
   - **报告数据库** - 存储生成的报告
3. 将 Integration 分享给这些数据库

详见: [docs/integrations/notion/mcp-setup.md](./docs/integrations/notion/mcp-setup.md)

### 配置 Google Calendar

两种方式:
1. **使用 MCP Server**（推荐）: 克隆 [google-calendar-mcp](https://github.com/nspady/google-calendar-mcp)
2. **直接集成**: 在 Google Cloud Console 创建 OAuth 凭据

详见: [docs/integrations/google-calendar/mcp-setup.md](./docs/integrations/google-calendar/mcp-setup.md)

---

## 🐛 常见问题

### 问题 1: pip 安装失败

```bash
# 使用 --proxy="" 参数
pip install --proxy="" -r requirements.txt
```

### 问题 2: 测试找不到模块

```bash
# pytest.ini 已配置，应该可以直接运行
pytest tests/

# 如果还有问题:
export PYTHONPATH=/home/averyubuntu/projects/ailma-project
pytest tests/
```

### 问题 3: API 连接失败

```bash
# 检查配置
./scripts/check-config.sh

# 测试连接
python scripts/test-api-connections.py
```

---

## 📚 完整文档

- **项目概览**: [README.md](./README.md)
- **开发环境设置**: [SETUP.md](./SETUP.md)
- **API Keys 配置**: [docs/guides/api-keys-setup.md](./docs/guides/api-keys-setup.md)
- **所有文档**: [docs/INDEX.md](./docs/INDEX.md)

---

## 🎯 项目状态

- ✅ Phase 1-2 完成（MVP）
- ✅ 20 个 Python 模块
- ✅ 25 个测试用例
- ✅ 40+ 文档页面
- ✅ Docker 部署就绪

---

## 🆘 获取帮助

- **文档**: [docs/](./docs/)
- **Issues**: [GitHub Issues](https://github.com/laiyinyizao007/ailma-project/issues)
- **故障排查**: [docs/reference/troubleshooting.md](./docs/reference/troubleshooting.md)

---

**开始使用 AILMA！** 🚀

**最后更新**: 2025-11-30
