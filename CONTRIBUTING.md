# 贡献指南

感谢您对 AILMA 项目的关注！我们欢迎所有形式的贡献。

---

## 📋 目录

1. [贡献方式](#贡献方式)
2. [开发流程](#开发流程)
3. [代码规范](#代码规范)
4. [提交规范](#提交规范)
5. [Pull Request 流程](#pull-request-流程)
6. [问题反馈](#问题反馈)
7. [行为准则](#行为准则)

---

## 🎯 贡献方式

您可以通过以下方式为项目做出贡献：

### 1. 代码贡献
- 🐛 修复 Bug
- ✨ 实现新功能
- 🔨 重构现有代码
- ⚡ 性能优化

### 2. 文档贡献
- 📝 改进文档
- 🌍 翻译文档
- 📖 编写教程
- 💡 添加代码示例

### 3. 测试贡献
- 🧪 编写单元测试
- 🔬 编写集成测试
- 🐛 报告 Bug
- 🔍 代码审查

### 4. 其他贡献
- 💬 回答社区问题
- 🎨 设计改进
- 📢 推广项目

---

## 💻 开发流程

### 1. Fork 项目

1. 访问 [AILMA 仓库](https://github.com/your-org/ailma-project)
2. 点击右上角的 "Fork" 按钮
3. 克隆您的 Fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ailma-project.git
   cd ailma-project
   ```

### 2. 设置开发环境

```bash
# 添加上游仓库
git remote add upstream https://github.com/your-org/ailma-project.git

# 创建虚拟环境
python3.11 -m venv venv
source venv/bin/activate

# 安装开发依赖
pip install -r requirements-dev.txt

# 安装 pre-commit hooks
pre-commit install
```

### 3. 创建功能分支

```bash
# 从 main 分支创建新分支
git checkout main
git pull upstream main
git checkout -b feature/your-feature-name
```

**分支命名规范**:
- `feature/` - 新功能
- `bugfix/` - Bug 修复
- `hotfix/` - 紧急修复
- `refactor/` - 代码重构
- `docs/` - 文档更新
- `test/` - 测试相关

### 4. 开发和测试

```bash
# 编写代码
# ...

# 运行测试
pytest

# 运行代码质量检查
black backend/ tests/
isort backend/ tests/
flake8 backend/
mypy backend/

# 提交代码
git add .
git commit -m "feat: add new feature"
```

### 5. 推送和创建 PR

```bash
# 推送到您的 Fork
git push origin feature/your-feature-name

# 在 GitHub 上创建 Pull Request
```

---

## 📖 代码规范

### Python 风格指南

遵循 **PEP 8** 和 **Google Python Style Guide**。

#### 格式化工具

我们使用以下工具确保代码一致性：

- **Black**: 代码格式化
- **isort**: 导入排序
- **Flake8**: 代码检查
- **Mypy**: 类型检查

#### 命名规范

```python
# ✅ 好的做法
class NotionMCPClient:
    def __init__(self):
        self.api_key = "secret"
        self._internal_state = {}

    def create_page(self, title: str, content: str) -> Dict[str, Any]:
        """创建 Notion 页面"""
        pass

MAX_RETRY_ATTEMPTS = 3

def parse_user_instruction(text: str) -> Dict[str, Any]:
    """解析用户指令"""
    pass
```

#### 类型注解

所有函数都应该有类型注解：

```python
from typing import Dict, List, Optional

def process_command(
    command_id: str,
    user_id: str,
    timeout: int = 30
) -> Dict[str, Any]:
    """处理用户命令

    Args:
        command_id: 命令 ID
        user_id: 用户 ID
        timeout: 超时时间（秒）

    Returns:
        包含处理结果的字典

    Raises:
        TimeoutError: 处理超时
        ValueError: 参数无效
    """
    pass
```

#### 文档字符串

使用 Google Style docstrings：

```python
def complex_function(param1: int, param2: str, param3: Optional[bool] = None) -> List[str]:
    """一行简短描述

    详细描述（如果需要）。

    Args:
        param1: 第一个参数说明
        param2: 第二个参数说明
        param3: 可选参数说明。默认为 None

    Returns:
        返回值的说明

    Raises:
        ValueError: 什么情况下抛出
        TypeError: 什么情况下抛出

    Example:
        >>> result = complex_function(42, "test")
        >>> print(result)
        ['result1', 'result2']
    """
    pass
```

---

## 📝 提交规范

### Commit Message 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type (必需)

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关
- `perf`: 性能优化
- `ci`: CI/CD 相关

#### Scope (可选)

指明修改的范围，如：`api`, `core`, `adapters`, `docs` 等。

#### Subject (必需)

- 使用祈使句，现在时
- 不要大写首字母
- 不要以句号结尾
- 不超过 50 个字符

#### Body (可选)

- 详细描述修改的原因和内容
- 每行不超过 72 个字符

#### Footer (可选)

- 关闭的 Issue: `Closes #123`
- Breaking Changes: `BREAKING CHANGE: ...`

### 示例

#### 简单提交

```
feat(api): add calendar event creation endpoint
```

#### 详细提交

```
feat(api): add calendar event creation endpoint

Implement POST /api/v1/calendar/events to create calendar events
through Google Calendar API integration.

Changes:
- Add CalendarEventCreate schema for request validation
- Implement GoogleCalendarAdapter.create_event method
- Add comprehensive unit and integration tests
- Update OpenAPI documentation

Closes #123
```

#### Breaking Change

```
refactor(core)!: change task executor interface

BREAKING CHANGE: TaskExecutor.execute() now returns a Result object
instead of a dictionary. Update all calls to use result.data.

Migration guide: docs/migration/v2.md
```

---

## 🔄 Pull Request 流程

### 1. PR 检查清单

在创建 PR 之前，请确保：

- [ ] 代码通过所有测试 (`pytest`)
- [ ] 代码通过格式检查 (`black`, `isort`, `flake8`)
- [ ] 代码通过类型检查 (`mypy`)
- [ ] 添加了必要的测试
- [ ] 更新了相关文档
- [ ] Commit 遵循提交规范
- [ ] PR 描述清晰完整

### 2. PR 模板

创建 PR 时，请使用以下模板：

```markdown
## 变更说明
简要描述这个 PR 的目的和变更内容。

## 变更类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 重构
- [ ] 文档更新
- [ ] 其他（请说明）

## 测试
描述如何测试这些变更。

## 截图（如适用）
添加相关截图。

## 相关 Issue
Closes #123

## 检查清单
- [ ] 代码通过所有测试
- [ ] 代码通过格式检查
- [ ] 添加了必要的测试
- [ ] 更新了文档
- [ ] 遵循提交规范
```

### 3. 代码审查

- 所有 PR 需要至少一位维护者的审查
- 审查者会提供反馈和建议
- 请及时回应审查意见
- 可能需要多轮修改

### 4. 合并条件

PR 将在满足以下条件时被合并：

- ✅ 通过所有 CI 检查
- ✅ 获得至少一个 Approve
- ✅ 没有未解决的对话
- ✅ 与 main 分支没有冲突

---

## 🐛 问题反馈

### 报告 Bug

使用 [Issue 模板](https://github.com/your-org/ailma-project/issues/new?template=bug_report.md) 报告 Bug。

**必需信息**:
- 问题描述
- 复现步骤
- 预期行为
- 实际行为
- 环境信息（OS、Python 版本等）
- 相关日志或截图

### 功能请求

使用 [Issue 模板](https://github.com/your-org/ailma-project/issues/new?template=feature_request.md) 提出功能请求。

**必需信息**:
- 功能描述
- 使用场景
- 预期收益
- 可能的实现方案

---

## 🤝 行为准则

### 我们的承诺

为了营造开放和友好的环境，我们作为贡献者和维护者承诺：

- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

### 不可接受的行为

以下行为被视为骚扰，不会被容忍：

- 使用性化的语言或图像
- 侮辱性/贬损性评论
- 公开或私下骚扰
- 未经许可发布他人的私人信息
- 其他不道德或不专业的行为

### 执行

违反行为准则的行为可能导致：

1. 警告
2. 临时禁止参与
3. 永久禁止参与

请将违规行为报告至 conduct@ailma.example.com。

---

## 📚 资源

### 文档

- [产品需求文档](./docs/PRD.md)
- [开发指南](./docs/DEVELOPMENT.md)
- [API 文档](./docs/API.md)
- [部署指南](./docs/DEPLOYMENT.md)

### 社区

- [GitHub Discussions](https://github.com/your-org/ailma-project/discussions)
- [Discord 服务器](https://discord.gg/ailma)
- [邮件列表](mailto:dev@ailma.example.com)

### 学习资源

- [FastAPI 教程](https://fastapi.tiangolo.com/tutorial/)
- [Notion API 文档](https://developers.notion.com/)
- [MCP 规范](http://blog.modelcontextprotocol.io/)

---

## 🙏 致谢

感谢所有为 AILMA 项目做出贡献的开发者！

您的贡献将在 [CONTRIBUTORS.md](./CONTRIBUTORS.md) 中列出。

---

**感谢您的贡献！** 🎉

如有任何问题，请随时联系维护团队：
- Email: dev@ailma.example.com
- GitHub: [@ailma-org](https://github.com/your-org)
