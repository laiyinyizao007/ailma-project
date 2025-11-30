# Step 4: 实现实体提取

**预计时间**: 45 分钟
**难度**: 中等
**依赖**: Step 3 (意图分类)

---

## 🎯 目标

从用户输入中提取关键实体（时间、地点、标题等）

---

## 📋 子步骤

### 4.1 定义实体模型 (10 min)

- [ ] 创建 `src/ai/models/entity.py`
- [ ] 定义各类实体的数据类

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class TimeEntity:
    start: datetime
    end: Optional[datetime] = None
    is_all_day: bool = False
    recurrence: Optional[str] = None

@dataclass
class LocationEntity:
    name: str
    address: Optional[str] = None

@dataclass
class ExtractedEntities:
    title: Optional[str] = None
    time: Optional[TimeEntity] = None
    location: Optional[LocationEntity] = None
    participants: List[str] = None
    description: Optional[str] = None
```

**检查点**: 实体模型定义完成

---

### 4.2 创建实体提取器 (15 min)

- [ ] 创建 `src/ai/extractors/entity_extractor.py`
- [ ] 实现 `extract()` 方法
- [ ] 处理 LLM 返回的结构化数据

**代码框架**:
```python
class EntityExtractor:
    def __init__(self, claude_client, prompt_manager):
        self.client = claude_client
        self.prompts = prompt_manager

    async def extract(self, user_input: str, intent: IntentType) -> ExtractedEntities:
        prompt = self.prompts.get_entity_prompt(user_input, intent)
        response = await self.client.complete(prompt)
        return self._parse_entities(response)
```

**检查点**: 提取器类创建完成

---

### 4.3 实现实体验证 (10 min)

- [ ] 验证时间实体合理性
- [ ] 验证必填字段
- [ ] 处理缺失实体

**检查点**: 验证逻辑实现

---

### 4.4 组合 Parser (10 min)

- [ ] 创建 `src/ai/task_parser.py`
- [ ] 组合意图分类和实体提取
- [ ] 返回完整解析结果

```python
class TaskParser:
    async def parse(self, user_input: str) -> ParseResult:
        intent = await self.intent_classifier.classify(user_input)
        entities = await self.entity_extractor.extract(user_input, intent.type)
        return ParseResult(intent=intent, entities=entities)
```

**检查点**: TaskParser 组合完成

---

## ✅ 完成标准

- [ ] 实体模型定义完整
- [ ] EntityExtractor 实现
- [ ] 实体验证逻辑
- [ ] TaskParser 组合类

---

## 🔗 链接

- **上一步**: [Step 3 - 意图分类](./step-3-intent.md)
- **下一步**: [Step 5 - 时间解析器](./step-5-time.md)
