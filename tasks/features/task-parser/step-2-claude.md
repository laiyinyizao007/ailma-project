# Step 2: 集成 Claude API

**预计时间**: 15 分钟
**难度**: 简单
**依赖**: Step 1 (Prompt 模板)

---

## 🎯 目标

集成 Anthropic Claude API 用于 NLP 处理

---

## 📋 子步骤

### 2.1 安装依赖 (2 min)

- [ ] `pip install anthropic`
- [ ] 更新 `requirements.txt`

```bash
anthropic>=0.18.0
```

**检查点**: `pip list | grep anthropic` 显示已安装

---

### 2.2 创建 Claude 客户端 (5 min)

- [ ] 创建 `src/ai/clients/claude.py`
- [ ] 从环境变量读取 API Key
- [ ] 实现基础调用方法

**代码框架**:
```python
import anthropic
import os

class ClaudeClient:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    async def complete(self, prompt: str) -> str:
        message = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
```

**检查点**: 客户端类创建完成

---

### 2.3 添加错误处理 (5 min)

- [ ] 处理 API 超时
- [ ] 处理 Rate Limit
- [ ] 处理认证失败

**检查点**: 错误处理逻辑完成

---

### 2.4 验证连接 (3 min)

- [ ] 编写简单测试脚本
- [ ] 验证 API 响应

```python
# test_claude.py
client = ClaudeClient()
response = await client.complete("Say hello")
print(response)
```

**检查点**: API 调用成功返回

---

## ✅ 完成标准

- [ ] anthropic 依赖安装
- [ ] ClaudeClient 类实现
- [ ] 错误处理完成
- [ ] API 调用验证通过

---

## 🔗 链接

- **上一步**: [Step 1 - Prompt 模板](./step-1-prompt.md)
- **下一步**: [Step 3 - 意图分类](./step-3-intent.md)
