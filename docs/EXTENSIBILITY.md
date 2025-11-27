# 🔧 AILMA 可扩展性指南

**为快速增长设计的扩展架构**

---

## 🎯 设计目标

支持**快速添加新功能**，保持：
- ✅ **零耦合** - 新功能不影响现有功能
- ✅ **标准化** - 统一的开发模板和流程
- ✅ **自动化** - 减少重复劳动
- ✅ **可追踪** - 实时查看项目进度

---

## 📐 扩展架构原则

### 1. 插件化设计

**每个功能都是独立插件**，遵循统一接口：

```python
# backend/plugins/base.py
class FeaturePlugin(ABC):
    """所有功能插件的基类"""

    name: str              # 功能名称
    version: str           # 版本号
    dependencies: List[str] # 依赖的其他插件

    @abstractmethod
    async def initialize(self):
        """初始化插件"""
        pass

    @abstractmethod
    async def handle_intent(self, intent: str, entities: Dict) -> Result:
        """处理用户意图"""
        pass

    @abstractmethod
    def get_supported_intents(self) -> List[str]:
        """返回支持的意图列表"""
        pass
```

**示例：报告生成插件**

```python
# backend/plugins/report_generator.py
class ReportGeneratorPlugin(FeaturePlugin):
    name = "report_generator"
    version = "1.0.0"
    dependencies = ["notion_mcp", "google_calendar_mcp"]

    async def initialize(self):
        self.notion = get_plugin("notion_mcp")
        self.calendar = get_plugin("google_calendar_mcp")

    async def handle_intent(self, intent: str, entities: Dict) -> Result:
        if intent == "generate_weekly_report":
            return await self._generate_weekly_report(entities)
        elif intent == "generate_monthly_report":
            return await self._generate_monthly_report(entities)

    def get_supported_intents(self) -> List[str]:
        return ["generate_weekly_report", "generate_monthly_report"]
```

**优势**:
- ✅ 新增功能只需创建新插件
- ✅ 禁用功能只需移除插件注册
- ✅ 插件可以独立测试和部署

---

### 2. 集成模板化

**添加新集成的标准流程** - 只需 3 步：

#### Step 1: 使用模板创建目录

```bash
# 自动化脚本
./scripts/create-integration.sh slack

# 自动生成：
docs/integrations/slack/
├── README.md              # 从模板生成
├── mcp-setup.md           # 从模板生成
├── tools-reference.md     # 从模板生成
└── examples.md            # 从模板生成

backend/adapters/
└── slack_mcp_client.py    # 从模板生成

tests/mcp_integration/slack/
└── test_connection.py     # 从模板生成
```

#### Step 2: 填充配置

```python
# backend/adapters/slack_mcp_client.py (自动生成的骨架)
class SlackMCPClient(MCPClientBase):
    """Slack MCP 客户端"""

    # TODO: 填写 MCP Server URL
    server_url = "http://localhost:3001/mcp"

    # TODO: 定义工具
    async def send_message(self, channel: str, text: str):
        return await self.call_tool("send_message",
                                     channel=channel, text=text)
```

#### Step 3: 注册插件

```python
# backend/plugins/__init__.py
from .slack_integration import SlackPlugin

AVAILABLE_PLUGINS = [
    NotionMCPPlugin(),
    GoogleCalendarMCPPlugin(),
    ReportGeneratorPlugin(),
    SlackPlugin(),  # ← 添加一行即可
]
```

**耗时**: 新增一个集成 **< 30 分钟**（包括文档）

---

### 3. 意图可扩展

**意图注册机制**：

```python
# backend/core/intent_registry.py
class IntentRegistry:
    """中央意图注册表"""

    _registry: Dict[str, FeaturePlugin] = {}

    @classmethod
    def register(cls, plugin: FeaturePlugin):
        """注册插件支持的意图"""
        for intent in plugin.get_supported_intents():
            cls._registry[intent] = plugin

    @classmethod
    async def handle(cls, intent: str, entities: Dict) -> Result:
        """路由意图到对应插件"""
        plugin = cls._registry.get(intent)
        if not plugin:
            raise IntentNotSupportedError(intent)
        return await plugin.handle_intent(intent, entities)
```

**添加新意图** - 只需在插件中声明：

```python
class EmailPlugin(FeaturePlugin):
    def get_supported_intents(self) -> List[str]:
        return [
            "send_email",           # ← 新意图
            "schedule_email",       # ← 新意图
            "search_emails"         # ← 新意图
        ]
```

**AI Parser 自动识别新意图**（无需重新训练）

---

## 📋 快速扩展模板

### 模板 1: 新集成（MCP）

**位置**: `templates/integration-mcp/`

**包含**:
```
templates/integration-mcp/
├── README.md.template
├── mcp-setup.md.template
├── tools-reference.md.template
├── examples.md.template
├── client.py.template
└── test_connection.py.template
```

**使用**:
```bash
./scripts/create-integration.sh <integration_name>
```

**自动完成**:
- ✅ 创建 4 个文档（从模板）
- ✅ 创建 MCP Client 骨架
- ✅ 创建测试文件
- ✅ 更新 INDEX.md
- ✅ 更新 PROGRESS.md

---

### 模板 2: 新功能（Feature）

**位置**: `templates/feature/`

**包含**:
```
templates/feature/
├── feature-doc.md.template
├── plugin.py.template
└── test_feature.py.template
```

**使用**:
```bash
./scripts/create-feature.sh <feature_name>
```

**示例**:
```bash
./scripts/create-feature.sh task_reminder

# 自动生成：
docs/features/task-reminder.md
backend/plugins/task_reminder.py
tests/plugins/test_task_reminder.py

# 自动更新：
docs/INDEX.md (添加功能链接)
PROGRESS.md (添加任务追踪)
```

---

### 模板 3: 新 API 端点

**位置**: `templates/api-endpoint/`

**使用**:
```bash
./scripts/create-api.sh <resource_name>

# 示例
./scripts/create-api.sh notifications

# 自动生成：
backend/api/routes/notifications.py
backend/api/schemas/notifications.py
tests/api/test_notifications.py
docs/api/notifications.md
```

---

## 🤖 自动化工具

### 工具 1: 集成生成器

**脚本**: `scripts/create-integration.sh`

```bash
#!/bin/bash
# 用法: ./scripts/create-integration.sh <name>

INTEGRATION_NAME=$1

echo "🚀 创建新集成: $INTEGRATION_NAME"

# 1. 创建文档目录
mkdir -p docs/integrations/$INTEGRATION_NAME

# 2. 从模板生成文档
for template in README mcp-setup tools-reference examples; do
    sed "s/{{INTEGRATION_NAME}}/$INTEGRATION_NAME/g" \
        templates/integration-mcp/$template.md.template \
        > docs/integrations/$INTEGRATION_NAME/$template.md
    echo "✅ 创建文档: $template.md"
done

# 3. 生成 MCP Client
sed "s/{{INTEGRATION_NAME}}/$INTEGRATION_NAME/g" \
    templates/integration-mcp/client.py.template \
    > backend/adapters/${INTEGRATION_NAME}_mcp_client.py
echo "✅ 创建 MCP Client"

# 4. 生成测试
mkdir -p tests/mcp_integration/$INTEGRATION_NAME
sed "s/{{INTEGRATION_NAME}}/$INTEGRATION_NAME/g" \
    templates/integration-mcp/test_connection.py.template \
    > tests/mcp_integration/$INTEGRATION_NAME/test_connection.py
echo "✅ 创建测试文件"

# 5. 更新 INDEX.md
python scripts/update_index.py --add-integration $INTEGRATION_NAME
echo "✅ 更新 INDEX.md"

# 6. 更新进度跟踪
python scripts/update_progress.py --add-task "集成: $INTEGRATION_NAME"
echo "✅ 更新 PROGRESS.md"

echo ""
echo "🎉 集成创建完成！"
echo "📁 文档: docs/integrations/$INTEGRATION_NAME/"
echo "💻 代码: backend/adapters/${INTEGRATION_NAME}_mcp_client.py"
echo "🧪 测试: tests/mcp_integration/$INTEGRATION_NAME/"
echo ""
echo "📝 下一步:"
echo "1. 编辑 docs/integrations/$INTEGRATION_NAME/mcp-setup.md"
echo "2. 实现 backend/adapters/${INTEGRATION_NAME}_mcp_client.py"
echo "3. 运行测试: pytest tests/mcp_integration/$INTEGRATION_NAME/"
```

---

### 工具 2: 功能生成器

**脚本**: `scripts/create-feature.sh`

```bash
#!/bin/bash
# 用法: ./scripts/create-feature.sh <feature_name>

FEATURE_NAME=$1

echo "🚀 创建新功能: $FEATURE_NAME"

# 1. 创建功能文档
sed "s/{{FEATURE_NAME}}/$FEATURE_NAME/g" \
    templates/feature/feature-doc.md.template \
    > docs/features/$FEATURE_NAME.md
echo "✅ 创建功能文档"

# 2. 创建插件骨架
sed "s/{{FEATURE_NAME}}/$FEATURE_NAME/g" \
    templates/feature/plugin.py.template \
    > backend/plugins/$FEATURE_NAME.py
echo "✅ 创建插件代码"

# 3. 创建测试
sed "s/{{FEATURE_NAME}}/$FEATURE_NAME/g" \
    templates/feature/test_feature.py.template \
    > tests/plugins/test_$FEATURE_NAME.py
echo "✅ 创建测试文件"

# 4. 更新文档索引
python scripts/update_index.py --add-feature $FEATURE_NAME
echo "✅ 更新 INDEX.md"

# 5. 添加到进度跟踪
python scripts/update_progress.py --add-task "功能: $FEATURE_NAME" --category "features"
echo "✅ 更新 PROGRESS.md"

echo ""
echo "🎉 功能创建完成！"
echo "📝 文档: docs/features/$FEATURE_NAME.md"
echo "💻 代码: backend/plugins/$FEATURE_NAME.py"
echo "🧪 测试: tests/plugins/test_$FEATURE_NAME.py"
```

---

### 工具 3: 进度更新器

**脚本**: `scripts/update_progress.py`

```python
#!/usr/bin/env python3
"""自动更新 PROGRESS.md"""

import argparse
from datetime import datetime

def update_progress(task: str, category: str, status: str = "⏳ 进行中"):
    """添加或更新任务到 PROGRESS.md"""

    # 读取当前进度
    with open("PROGRESS.md", "r") as f:
        lines = f.readlines()

    # 找到分类章节
    category_found = False
    insert_index = -1

    for i, line in enumerate(lines):
        if f"### {category}" in line:
            category_found = True
        elif category_found and line.startswith("- "):
            insert_index = i
            break

    # 插入新任务
    new_task = f"- {status} **{task}** - 创建于 {datetime.now().strftime('%Y-%m-%d')}\n"

    if insert_index > 0:
        lines.insert(insert_index, new_task)

    # 写回文件
    with open("PROGRESS.md", "w") as f:
        f.writelines(lines)

    print(f"✅ 已添加任务到进度跟踪: {task}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--add-task", required=True)
    parser.add_argument("--category", default="最近任务")
    parser.add_argument("--status", default="⏳ 进行中")

    args = parser.parse_args()
    update_progress(args.add_task, args.category, args.status)
```

---

## 📊 进度跟踪系统

### 1. PROGRESS.md - 实时进度

**位置**: `/PROGRESS.md`

**自动维护**:
- ✅ 每次创建新功能/集成时自动更新
- ✅ 显示完成度百分比
- ✅ 按类别分组
- ✅ 时间戳记录

**示例**:
```markdown
# 📊 AILMA 项目进度

**最后更新**: 2025-11-27 14:30

---

## 总体进度

| 模块 | 计划 | 完成 | 进行中 | 待开始 | 完成率 |
|------|------|------|--------|--------|--------|
| **集成** | 5 | 2 | 1 | 2 | 40% |
| **功能** | 8 | 3 | 2 | 3 | 37.5% |
| **文档** | 32 | 6 | 4 | 22 | 18.75% |
| **总计** | 45 | 11 | 7 | 27 | 24.4% |

---

## 集成模块 (40% 完成)

### ✅ 已完成 (2)
- ✅ **Notion MCP** - 2025-11-27
- ✅ **Google Calendar MCP** - 2025-11-27

### ⏳ 进行中 (1)
- ⏳ **Claude API** - 开始于 2025-11-27

### 📋 待开始 (2)
- 📋 **Slack MCP** - 计划于 Week 3
- 📋 **GitHub MCP** - 计划于 Week 4

---

## 功能模块 (37.5% 完成)

### ✅ 已完成 (3)
- ✅ **任务解析** - 2025-11-26
- ✅ **日历管理** - 2025-11-27
- ✅ **笔记管理** - 2025-11-27

### ⏳ 进行中 (2)
- ⏳ **报告生成** - 开始于 2025-11-27
- ⏳ **智能提醒** - 开始于 2025-11-27

### 📋 待开始 (3)
- 📋 **邮件集成** - 计划于 Week 3
- 📋 **任务分配** - 计划于 Week 4
- 📋 **数据分析** - 计划于 Week 5
```

---

### 2. 项目仪表板 - 可视化进度

**位置**: `/docs/DASHBOARD.md`

**包含**:
- 📊 进度条（ASCII 艺术）
- 📈 趋势图（文本）
- ⏱️ 里程碑时间线
- 🏆 近期成就

**自动生成**:
```bash
# 每次 commit 后自动运行
python scripts/generate_dashboard.py
```

---

### 3. 周报自动生成

**脚本**: `scripts/generate_weekly_report.py`

```python
#!/usr/bin/env python3
"""生成本周开发周报"""

import subprocess
from datetime import datetime, timedelta

def generate_weekly_report():
    """分析 git commits 生成周报"""

    # 获取本周 commits
    one_week_ago = datetime.now() - timedelta(days=7)
    commits = subprocess.check_output([
        "git", "log",
        f"--since={one_week_ago.isoformat()}",
        "--pretty=format:%h|%s|%an|%ad",
        "--date=short"
    ]).decode().split("\n")

    # 分析
    features = []
    docs = []
    fixes = []

    for commit in commits:
        if not commit:
            continue
        hash, msg, author, date = commit.split("|")

        if msg.startswith("feat:"):
            features.append(msg[5:].strip())
        elif msg.startswith("docs:"):
            docs.append(msg[5:].strip())
        elif msg.startswith("fix:"):
            fixes.append(msg[4:].strip())

    # 生成报告
    report = f"""# 📊 AILMA 周报 ({one_week_ago.strftime('%Y-%m-%d')} ~ {datetime.now().strftime('%Y-%m-%d')})

## 🎉 本周成就

### 新增功能 ({len(features)})
{chr(10).join(f'- {f}' for f in features)}

### 文档更新 ({len(docs)})
{chr(10).join(f'- {d}' for d in docs)}

### Bug 修复 ({len(fixes)})
{chr(10).join(f'- {f}' for f in fixes)}

## 📈 统计

- Commits: {len(commits)}
- 新增代码: {get_lines_added()} 行
- 文档更新: {get_docs_updated()} 个文件

---

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

    # 保存
    with open(f"reports/weekly-{datetime.now().strftime('%Y-W%W')}.md", "w") as f:
        f.write(report)

    print(f"✅ 周报已生成: reports/weekly-{datetime.now().strftime('%Y-W%W')}.md")

if __name__ == "__main__":
    generate_weekly_report()
```

---

## 🎯 最佳实践

### 1. 功能开发流程

```
1. 创建功能分支
   git checkout -b feature/task-reminder

2. 使用模板生成骨架
   ./scripts/create-feature.sh task_reminder

3. 实现功能
   - 编辑 backend/plugins/task_reminder.py
   - 编辑 docs/features/task-reminder.md

4. 编写测试
   - 实现 tests/plugins/test_task_reminder.py
   - 运行: pytest tests/plugins/test_task_reminder.py

5. 更新进度
   python scripts/update_progress.py \
       --add-task "任务提醒功能" \
       --category "功能" \
       --status "✅ 已完成"

6. 提交代码
   git add .
   git commit -m "feat: 添加任务提醒功能"

7. 自动生成周报（CI 自动运行）
   python scripts/generate_weekly_report.py
```

---

### 2. 集成开发流程

```
1. 创建集成
   ./scripts/create-integration.sh slack

2. 配置 MCP Server
   - 编辑 docs/integrations/slack/mcp-setup.md
   - 填写 OAuth 配置

3. 实现 MCP Client
   - 编辑 backend/adapters/slack_mcp_client.py
   - 定义工具方法

4. 测试连接
   python tests/mcp_integration/slack/test_connection.py

5. 更新进度
   自动完成（create-integration.sh 已处理）

6. 提交
   git commit -m "feat: 添加 Slack MCP 集成"
```

---

## 📁 完整文件结构

```
ailma-project/
├── docs/
│   ├── INDEX.md
│   ├── PROGRESS.md              # ← 实时进度跟踪
│   ├── DASHBOARD.md             # ← 项目仪表板
│   ├── EXTENSIBILITY.md         # ← 本文件
│   └── ...
│
├── scripts/                     # ← 自动化工具
│   ├── create-integration.sh   # 集成生成器
│   ├── create-feature.sh        # 功能生成器
│   ├── create-api.sh            # API 生成器
│   ├── update_progress.py       # 进度更新器
│   ├── update_index.py          # 索引更新器
│   └── generate_weekly_report.py # 周报生成器
│
├── templates/                   # ← 开发模板
│   ├── integration-mcp/         # MCP 集成模板
│   ├── feature/                 # 功能模板
│   └── api-endpoint/            # API 模板
│
├── reports/                     # ← 自动生成的报告
│   ├── weekly-2025-W48.md
│   └── ...
│
└── backend/
    └── plugins/                 # ← 插件目录
        ├── __init__.py          # 插件注册
        ├── base.py              # 基类
        ├── notion_mcp.py
        ├── google_calendar_mcp.py
        └── ... (新插件自动添加)
```

---

## 📚 相关文档

- **[文档总索引](./INDEX.md)** - 所有文档入口
- **[架构设计](./overview/architecture.md)** - 系统架构
- **[重构总结](./REFACTORING_SUMMARY.md)** - 文档重构说明

---

**文档**: [总索引](./INDEX.md)
**最后更新**: 2025-11-27
