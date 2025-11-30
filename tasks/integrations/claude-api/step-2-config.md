# Step 2: 配置环境变量

**耗时**: 5 分钟 | **状态**: 📋 待开始

---

## 🎯 目标

把 Claude API Key 安全地注入到项目环境，供后续客户端使用。

---

## 📋 子步骤

### 2.1 更新 `.env` 文件 (3 分钟)

- [ ] 确认项目根目录存在 `.env`
- [ ] 在 `AI` 配置段添加：

```bash
# Claude
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
ANTHROPIC_MODEL=claude-3-sonnet-20240229
ANTHROPIC_MAX_TOKENS=1024
```

- [ ] 保存文件，不要提交 Key

**检查点**: `.env` 包含 Claude 相关配置

---

### 2.2 更新示例文件 (1 分钟)

- [ ] 打开 `.env.example`
- [ ] 添加同样的字段，但 Key 置空或使用 `your_key_here`
- [ ] 在注释中说明去 Anthropic 控制台获取

**检查点**: 示例文件指导团队成员配置

---

### 2.3 验证读取 (1 分钟)

- [ ] 在虚拟环境内运行：

```bash
python - <<'PY'
import os
print("ANTHROPIC_API_KEY:", "set" if os.getenv("ANTHROPIC_API_KEY") else "missing")
print("ANTHROPIC_MODEL:", os.getenv("ANTHROPIC_MODEL"))
PY
```

- [ ] 确认输出 `set`

**检查点**: Python 可以读取到环境变量

---

## ⚠️ 常见问题

### Key 泄露到 Git

**原因**: `.env` 未列入 `.gitignore`  
**解决**: 检查 `.gitignore`，必要时添加并删除历史敏感信息。

### 多环境切换错误

**原因**: 使用多个 `.env` 文件但忘记同步  
**解决**: 在 `.env.example` 中标明必填字段，确保 CI 读取一致配置。

---

## ✅ 完成标准

- [ ] `.env` 已包含 Claude 配置
- [ ] `.env.example` 有对应字段
- [ ] Python 可读取 Key

---

## 🔗 链接

- **上一步**: [Step 1 - 获取 API Key](./step-1-get-key.md)
- **下一步**: [Step 3 - 测试 Claude 调用](./step-3-test.md)
- **返回**: [Claude API 集成任务](./INDEX.md)

---

**最后更新**: 2025-11-27
