# Step 3: 实现意图分类

**预计时间**: 45 分钟
**难度**: 中等
**依赖**: Step 2 (Claude API)

---

## 🎯 目标

实现基于 LLM 的意图分类系统

---

## 📋 子步骤

### 3.1 定义意图枚举 (5 min)

- [ ] 创建 `src/ai/models/intent.py`
- [ ] 定义 IntentType 枚举

```python
from enum import Enum

class IntentType(str, Enum):
    CALENDAR_CREATE = "calendar_create"
    CALENDAR_QUERY = "calendar_query"
    CALENDAR_UPDATE = "calendar_update"
    CALENDAR_DELETE = "calendar_delete"
    NOTION_CREATE_PAGE = "notion_create_page"
    NOTION_CREATE_TODO = "notion_create_todo"
    GENERATE_REPORT = "generate_report"
    UNKNOWN = "unknown"
```

**检查点**: 枚举定义完成

---

### 3.2 创建意图分类器 (15 min)

- [ ] 创建 `src/ai/classifiers/intent_classifier.py`
- [ ] 实现 `classify()` 方法
- [ ] 解析 LLM 返回的 JSON

**代码框架**:
```python
class IntentClassifier:
    def __init__(self, claude_client, prompt_manager):
        self.client = claude_client
        self.prompts = prompt_manager

    async def classify(self, user_input: str) -> IntentResult:
        prompt = self.prompts.get_intent_prompt(user_input)
        response = await self.client.complete(prompt)
        return self._parse_response(response)

    def _parse_response(self, response: str) -> IntentResult:
        # 解析 JSON，返回 IntentResult
        pass
```

**检查点**: 分类器类创建完成

---

### 3.3 实现置信度阈值 (10 min)

- [ ] 定义最小置信度阈值 (0.7)
- [ ] 低于阈值返回 UNKNOWN
- [ ] 添加配置选项

**检查点**: 置信度逻辑实现

---

### 3.4 添加缓存机制 (10 min)

- [ ] 对相似输入缓存结果
- [ ] 使用 LRU Cache
- [ ] 设置过期时间

**检查点**: 缓存机制工作

---

### 3.5 测试常见场景 (5 min)

- [ ] 测试日历创建意图
- [ ] 测试查询意图
- [ ] 测试模糊输入

**测试用例**:
```python
test_cases = [
    ("明天下午3点开会", IntentType.CALENDAR_CREATE),
    ("我下周有什么安排", IntentType.CALENDAR_QUERY),
    ("生成本周工作总结", IntentType.GENERATE_REPORT),
]
```

**检查点**: 测试用例通过

---

## ✅ 完成标准

- [ ] IntentType 枚举定义
- [ ] IntentClassifier 实现
- [ ] 置信度阈值逻辑
- [ ] 缓存机制
- [ ] 基础测试通过

---

## 🔗 链接

- **上一步**: [Step 2 - Claude API](./step-2-claude.md)
- **下一步**: [Step 4 - 实体提取](./step-4-entity.md)
