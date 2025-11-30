# Step 3: 测试 Claude 调用

**耗时**: 20 分钟 | **状态**: 📋 待开始

---

## 🎯 目标

通过最小脚本验证 Claude API Key、网络连通性和 Python 客户端配置。

---

## 📋 子步骤

### 3.1 安装依赖 (2 分钟)

- [ ] 激活虚拟环境：`source venv/bin/activate`
- [ ] 安装 SDK：`pip install anthropic>=0.18.0`
- [ ] 把依赖写入 `requirements-mcp-test.txt` 或新建 `requirements.txt`

**检查点**: `pip show anthropic` 成功

---

### 3.2 创建测试脚本 (8 分钟)

- [ ] 在 `scripts/` 下创建 `claude_smoke_test.py`
- [ ] 代码示例：

```python
import os
import asyncio
import anthropic

async def main():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY missing")

    client = anthropic.AsyncAnthropic(api_key=api_key)
    resp = await client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229"),
        max_tokens=int(os.getenv("ANTHROPIC_MAX_TOKENS", "256")),
        temperature=0.2,
        messages=[{"role": "user", "content": "Respond with OK if you can read this."}],
    )
    print("Claude:", resp.content[0].text.strip())

if __name__ == "__main__":
    asyncio.run(main())
```

- [ ] 提供 CLI 参数（可选）切换模型/提示

**检查点**: 文件保存成功

---

### 3.3 运行脚本 (5 分钟)

- [ ] 确保 `.env` 已加载（`source .env` 或使用 `direnv`）
- [ ] 执行：

```bash
python scripts/claude_smoke_test.py
```

- [ ] 日志应打印 `Claude: OK`

**检查点**: API 返回成功

---

### 3.4 追加错误处理 (5 分钟)

- [ ] 捕获 `anthropic.APIStatusError`、`RateLimitError`
- [ ] 对 401/403/429 给出提示
- [ ] 对 `TimeoutError` 增加重试或反馈
- [ ] 在脚本末尾返回非零退出码便于 CI

**检查点**: 错误时脚本提示明确

---

## ⚠️ 常见问题

### 报错 401 Unauthorized

**原因**: Key 错误或未激活  
**解决**: 在控制台重新生成 Key，并确认 `.env` 已重新加载。

### 报错 429 Rate Limit

**原因**: 触发调用频率限制  
**解决**: 减少并发测试，或在控制台申请更高限额。

### 超时或网络错误

**原因**: 代理/网络限制  
**解决**: 配置 `HTTPS_PROXY`，或更换网络后重试。

---

## ✅ 完成标准

- [ ] `anthropic` 依赖安装完成
- [ ] `claude_smoke_test.py` 可运行
- [ ] 实际调用 Claude 成功并输出响应
- [ ] 错误处理覆盖常见异常

---

## 🔗 链接

- **上一步**: [Step 2 - 配置环境变量](./step-2-config.md)
- **返回**: [Claude API 集成任务](./INDEX.md)

---

**最后更新**: 2025-11-27
