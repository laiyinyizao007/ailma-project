# Step 3: 配置 OAuth

**耗时**: 15 分钟 | **状态**: ⏳ 进行中

---

## 🎯 目标

配置 OAuth 2.0 凭证，用于授权访问用户日历。

---

## 📋 子步骤

### 3.1 配置 OAuth 同意屏幕 (5 分钟)

- [ ] 进入 "APIs & Services" → "OAuth consent screen"
- [ ] 选择 User Type: "External"
- [ ] 点击 "Create"

**填写信息**:
- [ ] App name: `AILMA`
- [ ] User support email: 你的邮箱
- [ ] Developer contact: 你的邮箱
- [ ] 点击 "Save and Continue"

**检查点**: 同意屏幕配置完成

---

### 3.2 添加 Scopes (3 分钟)

- [ ] 在 Scopes 页面点击 "Add or Remove Scopes"
- [ ] 搜索并勾选:
  - `https://www.googleapis.com/auth/calendar`
  - `https://www.googleapis.com/auth/calendar.events`
- [ ] 点击 "Update"
- [ ] 点击 "Save and Continue"

**检查点**: Scopes 已添加

---

### 3.3 添加测试用户 (2 分钟)

- [ ] 在 Test users 页面
- [ ] 点击 "Add Users"
- [ ] 添加你的 Google 邮箱
- [ ] 点击 "Save and Continue"

**检查点**: 测试用户已添加

---

### 3.4 创建 OAuth Client (5 分钟)

- [ ] 进入 "APIs & Services" → "Credentials"
- [ ] 点击 "Create Credentials" → "OAuth client ID"
- [ ] Application type: "Desktop app"
- [ ] Name: `AILMA Desktop`
- [ ] 点击 "Create"

**检查点**: 看到 Client ID 和 Client Secret

---

### 3.5 下载凭证 (1 分钟)

- [ ] 点击下载按钮（JSON 文件）
- [ ] 保存为 `credentials.json`
- [ ] 放到项目根目录（不要提交到 Git！）

**检查点**: `credentials.json` 已保存

---

### 3.6 配置环境变量 (1 分钟)

- [ ] 打开 `.env`
- [ ] 添加以下配置:

```bash
GOOGLE_CLIENT_ID=xxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxx
```

**检查点**: 环境变量已配置

---

## ⚠️ 注意事项

- ❌ 不要将 `credentials.json` 提交到 Git
- ✅ 确保 `.gitignore` 包含 `credentials.json`
- ⚠️ 测试环境下，Token 7 天后过期
- 💡 发布到生产前需要提交验证申请

---

## ✅ 完成标准

- [ ] OAuth 同意屏幕已配置
- [ ] Scopes 已添加
- [ ] 测试用户已添加
- [ ] OAuth Client 已创建
- [ ] `credentials.json` 已下载
- [ ] 环境变量已配置

---

## 🔗 链接

- **上一步**: [启用 Calendar API](./step-2-enable-api.md)
- **下一步**: [安装 MCP Server](./step-4-mcp-server.md)
- **返回**: [Google Calendar MCP 任务索引](./INDEX.md)

---

**最后更新**: 2025-11-27
