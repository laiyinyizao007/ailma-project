# Step 1: 设计 Prompt 模板

**预计时间**: 30 分钟
**难度**: 中等
**依赖**: 无

---

## 🎯 目标

设计用于意图分类和实体提取的 Prompt 模板

---

## 📋 子步骤

### 1.1 创建 prompts 目录 (2 min)

- [ ] 创建 `src/ai/prompts/` 目录
- [ ] 创建 `__init__.py`

**检查点**: 目录结构存在

---

### 1.2 设计意图分类 Prompt (10 min)

- [ ] 定义支持的意图类型列表
- [ ] 编写 few-shot 示例
- [ ] 定义输出 JSON 格式

**示例**:
```python
INTENT_PROMPT = """
你是一个意图分类器。分析用户指令，返回意图类型。

支持的意图:
- calendar_create: 创建日历事件
- calendar_query: 查询日程
- calendar_update: 修改事件
- calendar_delete: 删除事件
- notion_create_page: 创建 Notion 页面
- notion_create_todo: 创建待办
- generate_report: 生成报告

用户指令: {user_input}

返回 JSON: {"intent": "...", "confidence": 0.0-1.0}
"""
```

**检查点**: Prompt 模板可以正确格式化

---

### 1.3 设计实体提取 Prompt (10 min)

- [ ] 定义实体类型 (时间、地点、标题等)
- [ ] 编写提取规则
- [ ] 定义输出格式

**检查点**: 实体提取 Prompt 完成

---

### 1.4 创建 Prompt 管理类 (8 min)

- [ ] 创建 `PromptManager` 类
- [ ] 实现模板加载方法
- [ ] 实现变量替换方法

**文件**: `src/ai/prompts/manager.py`

---

## ✅ 完成标准

- [ ] prompts 目录创建完成
- [ ] 意图分类 Prompt 设计完成
- [ ] 实体提取 Prompt 设计完成
- [ ] PromptManager 类实现

---

## 🔗 链接

- **下一步**: [Step 2 - 集成 Claude API](./step-2-claude.md)
- **索引**: [Task Parser INDEX](./INDEX.md)
