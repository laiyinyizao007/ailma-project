# Step 6: 单元测试

**预计时间**: 30 分钟
**难度**: 简单
**依赖**: Step 1-5

---

## 🎯 目标

为 Task Parser 模块编写完整的单元测试

---

## 📋 子步骤

### 6.1 创建测试目录 (2 min)

- [ ] 创建 `tests/ai/` 目录
- [ ] 创建 `conftest.py` 配置 fixtures

**检查点**: 测试目录结构完成

---

### 6.2 测试意图分类 (10 min)

- [ ] 创建 `tests/ai/test_intent_classifier.py`
- [ ] Mock Claude API 响应
- [ ] 测试各种意图类型

**测试用例**:
```python
@pytest.mark.parametrize("input,expected", [
    ("明天下午3点开会", IntentType.CALENDAR_CREATE),
    ("我下周有什么安排", IntentType.CALENDAR_QUERY),
    ("取消明天的会议", IntentType.CALENDAR_DELETE),
    ("生成本周报告", IntentType.GENERATE_REPORT),
])
async def test_intent_classification(input, expected):
    result = await classifier.classify(input)
    assert result.type == expected
```

**检查点**: 意图分类测试通过

---

### 6.3 测试实体提取 (10 min)

- [ ] 创建 `tests/ai/test_entity_extractor.py`
- [ ] 测试时间实体提取
- [ ] 测试标题实体提取

**测试用例**:
```python
async def test_extract_calendar_entities():
    result = await extractor.extract(
        "明天下午3点在会议室A开产品会议",
        IntentType.CALENDAR_CREATE
    )
    assert result.title == "产品会议"
    assert result.location.name == "会议室A"
    assert result.time.start.hour == 15
```

**检查点**: 实体提取测试通过

---

### 6.4 测试时间解析器 (5 min)

- [ ] 创建 `tests/ai/test_time_parser.py`
- [ ] 测试相对时间
- [ ] 测试模糊时间

**检查点**: 时间解析测试通过

---

### 6.5 运行测试覆盖率 (3 min)

- [ ] `pytest --cov=src/ai tests/ai/`
- [ ] 确保覆盖率 ≥ 80%

**检查点**: 覆盖率达标

---

## ✅ 完成标准

- [ ] 测试目录结构完成
- [ ] 意图分类测试 (≥5 用例)
- [ ] 实体提取测试 (≥5 用例)
- [ ] 时间解析测试 (≥5 用例)
- [ ] 覆盖率 ≥ 80%

---

## 🔗 链接

- **上一步**: [Step 5 - 时间解析器](./step-5-time.md)
- **模块索引**: [Task Parser INDEX](./INDEX.md)
- **阶段**: [Phase 2](../../phases/phase-2.md)
