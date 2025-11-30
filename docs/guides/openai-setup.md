# OpenAI API 配置指南

AILMA 支持使用 OpenAI API (GPT-4o, GPT-4o-mini 等) 作为 LLM 提供商，替代 Claude API。

---

## 🔐 安全警告

**重要**: 永远不要在以下地方暴露你的 API Key：
- ❌ GitHub Issues / Pull Requests
- ❌ 聊天对话 / Discord / Slack
- ❌ 公开的代码仓库
- ❌ 截图 / 日志文件

**如果你的 API Key 已经暴露**：
1. 立即前往 https://platform.openai.com/api-keys
2. 撤销（删除）暴露的密钥
3. 创建新密钥

---

## 📋 前置条件

1. **OpenAI 账户**
   - 注册: https://platform.openai.com/signup

2. **充值余额**
   - 前往: https://platform.openai.com/account/billing
   - 推荐最少充值: $5 (可用很久)

3. **创建 API Key**
   - 前往: https://platform.openai.com/api-keys
   - 点击 "Create new secret key"
   - 命名: "AILMA Production"
   - 权限: All (默认)
   - **立即复制密钥** (只显示一次！)

---

## 🚀 快速配置

### 方式 1: 自动配置脚本 (推荐)

```bash
# 运行配置向导
chmod +x scripts/configure-openai.sh
./scripts/configure-openai.sh
```

脚本会：
- ✅ 引导你安全输入 API Key
- ✅ 自动更新 .env 文件
- ✅ 测试 API 连接
- ✅ 备份原配置

### 方式 2: 手动配置

1. **编辑 .env 文件**:
   ```bash
   nano .env
   ```

2. **设置以下变量**:
   ```bash
   # LLM Provider 选择
   LLM_PROVIDER=openai

   # OpenAI API Key (替换为你的密钥)
   OPENAI_API_KEY=sk-proj-your_actual_key_here

   # 模型选择
   LLM_MODEL=gpt-4o-mini
   ```

3. **保存并退出** (Ctrl+O, Enter, Ctrl+X)

---

## ✅ 验证配置

### 1. 测试 OpenAI 配置

```bash
source venv/bin/activate
python scripts/test-openai-config.py
```

**期望输出**:
```
✅ LLM Provider: openai
✅ Model: gpt-4o-mini
✅ API Key: sk-proj-ab...xyz
✅ OpenAI 客户端初始化成功
✅ API 调用成功
响应: AILMA 是一个智能生活管理助手...
```

### 2. 验证完整配置

```bash
./scripts/check-config.sh
```

应该显示所有配置项通过。

---

## 🎯 模型选择

### 推荐模型

| 模型 | 用途 | 成本 | 速度 |
|------|------|------|------|
| **gpt-4o-mini** | 日常使用 ⭐ | 最低 | 最快 |
| **gpt-4o** | 高质量输出 | 中等 | 快 |
| **gpt-4-turbo** | 复杂任务 | 高 | 慢 |

### 成本对比 (每 1M tokens)

| 模型 | 输入 | 输出 |
|------|------|------|
| gpt-4o-mini | $0.15 | $0.60 |
| gpt-4o | $2.50 | $10.00 |
| gpt-4-turbo | $10.00 | $30.00 |

### AILMA 典型用量

**每天 10 次操作**:
- 意图识别: ~200 tokens
- 实体提取: ~300 tokens
- 报告生成: ~1000 tokens

**月成本估算 (gpt-4o-mini)**:
```
10 次/天 × 30 天 × 1500 tokens × ($0.15 + $0.60) / 1M ≈ $0.34/月
```

💰 **非常便宜！**

---

## 🔄 切换回 Claude

如果想切换回 Claude API:

1. **编辑 .env**:
   ```bash
   LLM_PROVIDER=claude
   ANTHROPIC_API_KEY=sk-ant-your_claude_key
   LLM_MODEL=claude-3-sonnet-20240229
   ```

2. **重启服务**:
   ```bash
   docker-compose restart
   ```

---

## 🐛 故障排查

### 问题 1: "AuthenticationError: Invalid API Key"

**原因**: API Key 无效或已撤销

**解决**:
1. 检查 .env 中的 OPENAI_API_KEY 是否正确
2. 确认密钥在 https://platform.openai.com/api-keys 中有效
3. 重新创建密钥

### 问题 2: "RateLimitError: Rate limit exceeded"

**原因**: 请求太频繁或余额不足

**解决**:
1. 检查账户余额: https://platform.openai.com/account/billing
2. 升级到付费计划
3. 等待几分钟后重试

### 问题 3: "模块导入失败"

**原因**: openai 库未安装

**解决**:
```bash
source venv/bin/activate
pip install --proxy="" openai>=1.0.0
```

### 问题 4: API 调用很慢

**原因**: 使用了较慢的模型或网络问题

**解决**:
1. 切换到 gpt-4o-mini (更快)
2. 检查网络连接
3. 考虑使用代理

---

## 📊 性能对比

### OpenAI vs Claude

| 指标 | OpenAI (gpt-4o-mini) | Claude (Sonnet) |
|------|---------------------|-----------------|
| 响应速度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 成本 | $0.15-0.60/1M | $3-15/1M |
| 中文理解 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| JSON 解析 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 可用性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

**推荐**:
- 🚀 日常使用: OpenAI gpt-4o-mini (快速且便宜)
- 🎯 高质量: Claude Sonnet (更好的中文理解)

---

## 💡 最佳实践

1. **开发环境使用 gpt-4o-mini**
   - 快速迭代
   - 降低成本

2. **生产环境根据需求选择**
   - 高频操作 → gpt-4o-mini
   - 关键任务 → gpt-4o 或 Claude

3. **设置使用限额**
   - 在 OpenAI Dashboard 设置月度限额
   - 避免意外高额账单

4. **监控使用量**
   - 定期检查: https://platform.openai.com/account/usage

---

## 🔗 相关链接

- [OpenAI API 文档](https://platform.openai.com/docs)
- [定价详情](https://openai.com/pricing)
- [使用指南](https://platform.openai.com/docs/guides)
- [API 参考](https://platform.openai.com/docs/api-reference)

---

**最后更新**: 2025-11-30
**维护者**: AILMA Team
