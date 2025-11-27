# Step 4: 安装 MCP Server

**耗时**: 10 分钟 | **状态**: 📋 待开始

---

## 🎯 目标

安装 Google Calendar MCP Server，提供 MCP 协议接口。

---

## 📋 子步骤

### 4.1 检查 Node.js (1 分钟)

```bash
node --version
# 需要 >= 18.0.0
```

- [ ] Node.js 版本 >= 18

**如果版本过低**:
```bash
# 使用 nvm 安装
nvm install 18
nvm use 18
```

---

### 4.2 选择 MCP 实现 (2 分钟)

**推荐**: [nspady/google-calendar-mcp](https://github.com/nspady/google-calendar-mcp)

- [ ] 阅读 GitHub README
- [ ] 确认支持所需功能

**备选**:
- goldk3y/google-calendar-mcp
- deciduus/calendar-mcp

---

### 4.3 克隆仓库 (2 分钟)

```bash
# 在项目外创建目录
mkdir -p ~/mcp-servers
cd ~/mcp-servers

# 克隆 MCP Server
git clone https://github.com/nspady/google-calendar-mcp.git
cd google-calendar-mcp
```

- [ ] 仓库已克隆

---

### 4.4 安装依赖 (3 分钟)

```bash
npm install
```

- [ ] 依赖安装完成

---

### 4.5 配置凭证 (2 分钟)

```bash
# 复制凭证文件到 MCP Server 目录
cp ~/projects/ailma-project/credentials.json ./

# 或者设置环境变量
export GOOGLE_CREDENTIALS_PATH=~/projects/ailma-project/credentials.json
```

- [ ] 凭证已配置

---

### 4.6 首次运行授权 (2 分钟)

```bash
npm start
```

- [ ] 浏览器打开授权页面
- [ ] 登录并授权
- [ ] 看到 "Authorization successful"

**检查点**: `token.json` 生成成功

---

## ✅ 完成标准

- [ ] Node.js >= 18 已安装
- [ ] MCP Server 已克隆
- [ ] 依赖已安装
- [ ] OAuth 授权完成
- [ ] MCP Server 可以启动

---

## 🔗 链接

- **上一步**: [配置 OAuth](./step-3-oauth.md)
- **下一步**: [编写文档](./step-5-docs.md)
- **返回**: [Google Calendar MCP 任务索引](./INDEX.md)

---

**最后更新**: 2025-11-27
