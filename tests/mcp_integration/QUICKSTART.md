# 🚀 Notion MCP 连接测试 - 快速开始

## ✅ 已完成

- [x] 虚拟环境创建
- [x] 依赖安装完成
- [x] 测试脚本准备就绪

## 📝 下一步：配置 Notion Integration

### 步骤 1: 创建 Notion Integration（5分钟）

1. **访问** https://www.notion.so/my-integrations
2. **点击** "New integration"
3. **填写信息**:
   ```
   Name: AILMA Development
   Associated workspace: [选择您的工作区]
   Type: Internal
   ```
4. **Capabilities（能力）**: 勾选所有三个
   - ✅ Read content
   - ✅ Update content
   - ✅ Insert content
5. **Submit** 创建
6. **复制** Internal Integration Token
   - 格式: `secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

### 步骤 2: 创建测试数据库（可选，3分钟）

如果您想测试完整功能，在 Notion 中创建一个测试数据库：

1. **创建新页面** → 选择 "Table"
2. **重命名为**: "AILMA 指令中心（测试）"
3. **配置属性**:
   - `指令` (Title) - 默认已有
   - `状态` (Select) - 添加选项：
     - ⏳ Pending
     - 🔄 Processing
     - ✅ Done
     - ❌ Error
   - `结果` (Text)
   - `创建时间` (Created time)

4. **关键步骤 - 添加 Integration**:
   - 点击页面右上角 **"..."**
   - 选择 **"Connections"** → **"Connect to"**
   - 找到并选择 **"AILMA Development"**

5. **复制数据库 ID**:
   - 打开数据库
   - URL 格式: `https://notion.so/workspace/xxxxx?v=yyyyy`
   - 复制 `xxxxx` 部分（数据库 ID）

---

### 步骤 3: 配置环境变量（2分钟）

```bash
# 1. 进入项目目录
cd /home/averyubuntu/projects/ailma-project

# 2. 创建 .env 文件
cp .env.example .env

# 3. 编辑配置
nano .env  # 或使用您喜欢的编辑器
```

**最小配置（仅测试连接）**:
```bash
NOTION_API_KEY=secret_your_token_here
```

**完整配置（测试所有功能）**:
```bash
NOTION_API_KEY=secret_your_token_here
COMMAND_CENTER_DB_ID=your_database_id_here
```

保存并退出。

---

### 步骤 4: 运行测试（30秒）

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行测试
python tests/mcp_integration/test_notion_connection.py
```

---

## 🎯 预期结果

### 成功输出示例:

```
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
🚀  AILMA - Notion MCP 连接测试
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀

✅ Notion Client 初始化成功
📋 API Key (前10位): secret_abc...

============================================================
🔍 测试 1: 验证 API Token 有效性
============================================================
✅ 连接成功！
👤 用户信息:
   - Type: bot
   - ID: 12345678-1234-1234-1234-123456789abc

============================================================
🔍 测试 2: 搜索工作区内容
============================================================
✅ 搜索成功！
📊 找到 3 个数据库:
   1. AILMA 指令中心（测试） (ID: ...)
   2. 我的笔记 (ID: ...)
   3. 项目管理 (ID: ...)

============================================================
🔍 测试 3: 查询指定数据库
============================================================
✅ 查询成功！
📝 数据库包含 0 条记录

============================================================
🔍 测试 4: 创建测试页面
============================================================
✅ 页面创建成功！
📄 页面 ID: ...
🔗 页面链接: https://notion.so/...

🗑️  清理测试数据...
✅ 测试页面已删除

============================================================
🔍 测试 5: Markdown 内容写入 (模拟 MCP)
============================================================
✅ Markdown 页面创建成功！
🔗 页面链接: https://notion.so/...

📝 注意: MCP 版本可以直接传入 Markdown 字符串，
         无需手动转换为 Blocks（这是 MCP 的优势！）
✅ 测试页面已删除

============================================================
📊 测试结果汇总
============================================================
✅ 通过: 5/5
❌ 失败: 0/5

🎉 所有测试通过！Notion 连接正常！

💡 下一步:
   1. 将直接 API 调用替换为 MCP Client
   2. 利用 MCP 的 Markdown 原生支持
   3. 开始实现核心业务逻辑
```

---

## 🐛 常见问题

### Q1: "未找到 NOTION_API_KEY 环境变量"

**原因**: `.env` 文件不存在或配置错误

**解决**:
```bash
# 检查文件是否存在
ls -la .env

# 检查内容
cat .env | grep NOTION_API_KEY

# 确保格式正确（Token 前后无空格）
NOTION_API_KEY=secret_your_token
```

---

### Q2: "❌ 连接失败: Unauthorized"

**原因**:
- Token 复制错误
- Token 已过期
- Integration 已被删除

**解决**:
1. 重新访问 https://www.notion.so/my-integrations
2. 检查 Integration 状态
3. 复制新的 Token（确保完整）
4. 更新 `.env` 文件

---

### Q3: "❌ 查询失败: object not found"

**原因**: Integration 未被添加到数据库

**解决**:
1. 打开您的测试数据库
2. 点击右上角 "..." → "Connections"
3. 选择 "AILMA Development"
4. 点击 "Confirm"

---

### Q4: "❌ 创建页面失败: validation_error"

**原因**: 数据库字段类型不匹配

**解决**:
确保数据库有名为 "指令" 的 Title 字段，或修改测试脚本中的字段名。

---

## 📊 测试覆盖范围

| 测试 | 功能 | 依赖配置 |
|-----|------|---------|
| ✅ 测试 1 | API Token 验证 | NOTION_API_KEY |
| ✅ 测试 2 | 工作区搜索 | NOTION_API_KEY |
| ⚠️ 测试 3 | 数据库查询 | NOTION_API_KEY + COMMAND_CENTER_DB_ID |
| ⚠️ 测试 4 | 创建/删除页面 | NOTION_API_KEY + COMMAND_CENTER_DB_ID |
| ⚠️ 测试 5 | Markdown 写入 | NOTION_API_KEY + COMMAND_CENTER_DB_ID |

> 注意: 测试 3-5 需要配置 `COMMAND_CENTER_DB_ID`，否则会跳过

---

## 🎓 学习要点

### 1. 理解 Notion Blocks vs Markdown

**当前测试**（直接 API）:
```python
# 需要手动将 Markdown 转换为 Notion Blocks
markdown = "# 标题\n- 列表项"
blocks = convert_markdown_to_blocks(markdown)  # 复杂！
```

**未来 MCP**:
```python
# 直接传入 Markdown
mcp_client.create_page(
    title="报告",
    content="# 标题\n- 列表项"  # 简单！
)
```

### 2. Integration 权限

确保勾选所有权限：
- ✅ Read content - 读取页面和数据库
- ✅ Update content - 修改现有内容
- ✅ Insert content - 创建新页面

### 3. 数据库连接

**关键步骤**: Integration 必须被 **显式添加** 到数据库才能访问！

---

## 🚀 测试成功后的下一步

1. ✅ **验证 MCP 优势**: 对比测试 5 中的代码复杂度
2. ✅ **探索 MCP Client**: 阅读 `docs/ARCHITECTURE-MCP.md`
3. ✅ **规划实现**: 使用 MCP 重写 Notion 集成
4. ✅ **开发核心功能**: Task Parser, Executor, Report Generator

---

**祝测试顺利！** 🎉

如有问题，请参考完整文档: [README.md](./README.md)
