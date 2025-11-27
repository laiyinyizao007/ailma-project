# Step 2: 配置 API Key

**耗时**: 3 分钟 | **状态**: ✅ 已完成

---

## 🎯 目标

将 Notion API Key 配置到项目环境变量中。

---

## 📋 子步骤

### 2.1 创建 .env 文件 (1 分钟)

```bash
# 如果不存在，从模板创建
cp .env.example .env
```

- [ ] 确认 `.env` 文件存在

**检查点**: `.env` 文件已创建

---

### 2.2 填入 API Key (1 分钟)

- [ ] 用编辑器打开 `.env`
- [ ] 找到 `NOTION_API_KEY` 行
- [ ] 将 `secret_your_token_here` 替换为你的实际 Token

```bash
# .env
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

- [ ] 保存文件

**检查点**: API Key 已填入

---

### 2.3 配置 Workspace ID (1 分钟)

- [ ] 打开任意 Notion 页面
- [ ] 复制 URL 中的 Workspace ID
  - URL 格式: `https://www.notion.so/YOUR_WORKSPACE/...`
- [ ] 填入 `.env`:

```bash
NOTION_WORKSPACE_ID=your_workspace_id
```

**检查点**: Workspace ID 已配置

---

## ⚠️ 安全提醒

- ❌ 不要将 `.env` 提交到 Git
- ✅ 确保 `.gitignore` 包含 `.env`
- ✅ 在团队共享时使用安全渠道

---

## ✅ 完成标准

- [x] `.env` 文件已创建
- [x] `NOTION_API_KEY` 已配置
- [x] `NOTION_WORKSPACE_ID` 已配置

---

## 🔗 链接

- **上一步**: [创建 Integration](./step-1-create-integration.md)
- **下一步**: [编写文档](./step-3-write-docs.md)
- **返回**: [Notion MCP 任务索引](./INDEX.md)

---

**最后更新**: 2025-11-27
