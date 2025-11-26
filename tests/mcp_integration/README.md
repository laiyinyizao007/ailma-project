# Notion MCP 连接测试指南

## 📋 测试目的

验证 AILMA 项目与 Notion 的连接，确保能够：
1. ✅ 通过 API Token 进行身份验证
2. ✅ 访问 Notion 工作区
3. ✅ 读取和查询数据库
4. ✅ 创建和更新页面
5. ✅ 处理 Markdown 内容（为 MCP 做准备）

---

## 🚀 快速开始

### 步骤 1: 创建 Notion Integration

1. 访问 [Notion Integrations](https://www.notion.so/my-integrations)
2. 点击 **"New integration"**
3. 填写信息：
   - **Name**: AILMA Development
   - **Associated workspace**: 选择您的工作区
   - **Capabilities**: 勾选所有权限（Read, Update, Insert）
4. 点击 **"Submit"**
5. 复制 **Internal Integration Token**（以 `secret_` 开头）

### 步骤 2: 创建测试数据库（可选）

在 Notion 中创建一个测试数据库：

1. 创建新页面，选择 **"Table"** 视图
2. 重命名为 **"AILMA 指令中心（测试）"**
3. 添加以下属性：
   - **指令** (Title 类型) - 默认已有
   - **状态** (Select 类型) - 可选项：⏳ Pending, 🔄 Processing, ✅ Done, ❌ Error
   - **结果** (Text 类型)
   - **创建时间** (Created time 类型)

4. **重要**: 将 Integration 添加到此数据库
   - 点击页面右上角的 **"..."**
   - 选择 **"Connections"**
   - 选择 **"AILMA Development"**

5. 复制数据库 ID：
   - 数据库 URL 格式: `https://notion.so/workspace-name/[DATABASE_ID]?v=...`
   - 复制 `DATABASE_ID` 部分

### 步骤 3: 配置环境变量

```bash
# 在项目根目录创建 .env 文件
cd /home/averyubuntu/projects/ailma-project
cp .env.example .env

# 编辑 .env 文件
nano .env
```

填写以下内容：

```bash
# 必需配置
NOTION_API_KEY=secret_your_integration_token_here

# 可选配置（用于完整测试）
COMMAND_CENTER_DB_ID=your_database_id_here
```

### 步骤 4: 安装依赖

```bash
# 创建虚拟环境（如果还没有）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装测试依赖
pip install -r requirements-mcp-test.txt
```

### 步骤 5: 运行测试

```bash
# 运行连接测试
python tests/mcp_integration/test_notion_connection.py
```

---

## 📊 测试说明

### 测试 1: 验证 API Token 有效性
- **测试内容**: 调用 `users.me()` 获取当前用户信息
- **成功标准**: 返回用户 ID 和类型
- **失败原因**:
  - Token 无效或已过期
  - 网络连接问题

### 测试 2: 搜索工作区内容
- **测试内容**: 搜索工作区中的所有数据库
- **成功标准**: 返回数据库列表
- **失败原因**:
  - Integration 没有 "Read content" 权限
  - 工作区为空

### 测试 3: 查询指定数据库
- **测试内容**: 查询 COMMAND_CENTER_DB_ID 指定的数据库
- **成功标准**: 返回数据库内容
- **失败原因**:
  - 数据库 ID 错误
  - Integration 未添加到该数据库
  - 数据库已被删除

### 测试 4: 创建测试页面
- **测试内容**: 在数据库中创建新页面，然后删除
- **成功标准**: 成功创建并删除页面
- **失败原因**:
  - Integration 没有 "Insert content" 权限
  - 数据库字段类型不匹配

### 测试 5: Markdown 内容写入
- **测试内容**: 创建包含 Markdown 格式内容的页面
- **成功标准**: 成功创建带结构化内容的页面
- **说明**:
  - 此测试模拟 MCP 的 Markdown 支持
  - 实际 MCP 客户端会自动处理转换

---

## 🎯 预期输出

成功执行后应该看到：

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
   - ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

============================================================
🔍 测试 2: 搜索工作区内容
============================================================
✅ 搜索成功！
📊 找到 3 个数据库:
   1. AILMA 指令中心（测试） (ID: ...)
   2. 项目管理 (ID: ...)
   3. 周报归档 (ID: ...)

...

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

## 🐛 故障排查

### 问题 1: "未找到 NOTION_API_KEY 环境变量"

**解决方案**:
```bash
# 检查 .env 文件是否存在
ls -la .env

# 检查内容
cat .env | grep NOTION_API_KEY

# 确保格式正确（无空格）
NOTION_API_KEY=secret_your_token
```

---

### 问题 2: "❌ 连接失败: Unauthorized"

**可能原因**:
1. Token 复制错误（有多余空格或换行）
2. Token 已过期或被撤销
3. Integration 已被删除

**解决方案**:
1. 重新复制 Token，确保完整
2. 在 Notion Integrations 页面检查状态
3. 必要时重新创建 Integration

---

### 问题 3: "❌ 查询失败: object not found"

**可能原因**:
1. 数据库 ID 错误
2. Integration 未被添加到数据库

**解决方案**:
```bash
# 1. 检查数据库 ID 格式
# 正确格式: 32位十六进制，可能包含连字符
# 示例: a1b2c3d4e5f6789012345678901234ab

# 2. 添加 Integration 到数据库
# - 打开数据库页面
# - 点击右上角 "..."
# - Connections → 选择 AILMA Development
```

---

### 问题 4: "❌ 创建页面失败: validation_error"

**可能原因**:
数据库字段类型不匹配

**解决方案**:
检查数据库是否有 Title 类型的字段，测试脚本假设字段名为 "指令"。

可以修改测试脚本中的字段名：

```python
# 修改这一行
"指令": {  # 改为您的 Title 字段名
    "title": [...]
}
```

---

## 🔄 后续步骤

测试通过后：

1. ✅ **验证 MCP 优势**: 注意测试 5 中的 Markdown 转换复杂度
2. ✅ **集成 MCP Client**: 替换直接 API 调用
3. ✅ **实现监听器**: 基于测试代码实现生产版监听器
4. ✅ **开发核心功能**: AI 解析器、任务执行器等

---

## 📚 参考资源

- [Notion API 文档](https://developers.notion.com/reference/intro)
- [Notion MCP 文档](https://developers.notion.com/docs/mcp)
- [Python Notion SDK](https://github.com/ramnes/notion-sdk-py)
- [AILMA MCP 架构文档](../../docs/ARCHITECTURE-MCP.md)

---

**测试版本**: v1.0
**最后更新**: 2025-11-27
