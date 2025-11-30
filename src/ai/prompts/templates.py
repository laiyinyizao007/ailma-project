"""
Prompt 模板定义
"""

# 意图分类 Prompt
INTENT_CLASSIFICATION_PROMPT = """你是一个意图分类器。分析用户的自然语言指令，识别用户想要执行的操作类型。

支持的意图类型:
1. calendar_create - 创建新的日历事件
   示例: "明天下午3点开会"、"下周五约午餐"

2. calendar_query - 查询日程安排
   示例: "我明天有什么安排"、"下周的会议有哪些"

3. calendar_update - 修改已有事件
   示例: "把明天的会议改到后天"、"会议时间延长1小时"

4. calendar_delete - 删除事件
   示例: "取消明天的会议"、"删除周五的约会"

5. notion_create_page - 创建 Notion 页面
   示例: "记录今天的想法"、"创建项目笔记"

6. notion_create_todo - 创建待办事项
   示例: "添加待办：买菜"、"创建任务清单"

7. generate_report - 生成数据报告
   示例: "生成本周工作总结"、"总结上个月的日程"

8. update_settings - 修改设置
   示例: "切换到工作日历"、"修改默认提醒时间"

用户指令: "{user_input}"

请返回 JSON 格式:
{{
  "intent": "意图类型",
  "confidence": 0.0-1.0,
  "explanation": "为什么识别为这个意图"
}}
"""

# 实体提取 Prompt
ENTITY_EXTRACTION_PROMPT = """你是一个实体提取器。从用户指令中提取关键信息。

用户指令: "{user_input}"
意图类型: "{intent_type}"

请提取以下实体（如果存在）:
1. title - 事件/任务的标题
2. description - 详细描述
3. time - 时间信息
   - start: 开始时间 (ISO 8601 格式)
   - end: 结束时间 (如果有)
   - is_all_day: 是否全天事件
   - recurrence: 重复规则 (RRULE 格式, 如果有)
4. location - 地点信息
   - name: 地点名称
   - address: 详细地址 (如果有)
5. participants - 参与者列表
   - name: 姓名
   - email: 邮箱 (如果有)
6. tags - 标签列表
7. priority - 优先级 (high/medium/low)

当前时间: {current_time}
时区: {timezone}

返回 JSON 格式，只返回存在的字段:
{{
  "title": "string",
  "description": "string",
  "time": {{
    "start": "ISO 8601",
    "end": "ISO 8601",
    "is_all_day": false,
    "recurrence": "RRULE"
  }},
  "location": {{
    "name": "string",
    "address": "string"
  }},
  "participants": [
    {{
      "name": "string",
      "email": "string"
    }}
  ],
  "tags": ["tag1", "tag2"],
  "priority": "medium"
}}
"""

# 时间解析 Prompt (辅助)
TIME_PARSING_SYSTEM = """你是时间解析专家。
- 理解相对时间: "明天"、"下周三"、"3天后"
- 理解模糊时间: "早上"、"下午"、"晚上"
- 理解中文日期: "春节"、"周末"
- 始终返回 ISO 8601 格式
- 如果没有指定具体时间，使用合理的默认值
"""


class PromptManager:
    """Prompt 模板管理器"""

    @staticmethod
    def get_intent_prompt(user_input: str) -> str:
        """获取意图分类 prompt"""
        return INTENT_CLASSIFICATION_PROMPT.format(user_input=user_input)

    @staticmethod
    def get_entity_prompt(
        user_input: str, intent_type: str, current_time: str, timezone: str
    ) -> str:
        """获取实体提取 prompt"""
        return ENTITY_EXTRACTION_PROMPT.format(
            user_input=user_input,
            intent_type=intent_type,
            current_time=current_time,
            timezone=timezone,
        )

    @staticmethod
    def get_time_parsing_system() -> str:
        """获取时间解析系统 prompt"""
        return TIME_PARSING_SYSTEM
