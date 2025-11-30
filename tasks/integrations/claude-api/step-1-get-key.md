# Step 1: 获取 Claude API Key

**耗时**: 5 分钟 | **状态**: 📋 待开始

---

## 🎯 目标

在 Anthropic 控制台创建可用的 Claude API Key，并准备好在本地使用。

---

## 📋 子步骤

### 1.1 登录 Anthropic 控制台 (2 分钟)

- [ ] 打开 https://console.anthropic.com
- [ ] 使用允许访问 Claude API 的账号登录
- [ ] 确认可访问侧边栏中的 **API Keys** 菜单

**检查点**: 看到 API Keys 页面

---

### 1.2 创建新的 API Key (2 分钟)

- [ ] 点击 **Create Key**
- [ ] 命名为 `AILMA Development`
- [ ] 设置 `Expires` 为 `Never`（后续可以在面板中轮换）
- [ ] 点击 **Create Key**

**检查点**: 页面显示新生成的 Key

---

### 1.3 记录并安全存储 (1 分钟)

- [ ] 复制整段 Key（格式 `sk-ant-...`）
- [ ] 暂存到安全的密码管理器
- [ ] 不要存入仓库或聊天

**检查点**: Key 已安全保存

---

## ⚠️ 常见问题

### 无法访问 API Keys 页面

**原因**: 账号未获批 Claude API 权限  
**解决**: 填写申请表或换用已获批账号，再尝试登录。

### Key 遗失

**原因**: 离开页面后无法再次查看  
**解决**: 删除旧 Key，重新创建新的 Key 并更新环境变量。

---

## ✅ 完成标准

- [ ] 成功登录 Anthropic 控制台
- [ ] 创建 `AILMA Development` API Key
- [ ] 将 Key 安全保存

---

## 🔗 链接

- **下一步**: [Step 2 - 配置环境变量](./step-2-config.md)
- **返回**: [Claude API 集成任务](./INDEX.md)

---

**最后更新**: 2025-11-27
