# Step 4: 测试连接

**耗时**: 10 分钟 | **状态**: ✅ 已完成

---

## 🎯 目标

验证 Notion MCP 连接是否正常工作。

---

## 📋 子步骤

### 4.1 准备测试环境 (2 分钟)

```bash
# 激活虚拟环境
source venv/bin/activate

# 确保依赖已安装
pip install -r requirements.txt
```

- [ ] 虚拟环境已激活
- [ ] 依赖已安装

**检查点**: 无报错

---

### 4.2 运行连接测试 (3 分钟)

```bash
python tests/mcp_integration/notion/test_connection.py
```

- [ ] 运行测试脚本

**预期输出**:
```
✅ 连接成功！
✅ 可以访问工作区
✅ 可以查询数据库
```

**检查点**: 所有测试通过

---

### 4.3 手动验证 (3 分钟)

在 Python 交互环境中测试:

```python
from backend.adapters.notion_mcp_client import NotionMCPClient
import os

client = NotionMCPClient(api_key=os.getenv("NOTION_API_KEY"))

# 测试搜索
results = await client.search("测试")
print(f"找到 {len(results)} 个结果")
```

- [ ] 手动测试成功

**检查点**: 能够获取搜索结果

---

### 4.4 记录测试结果 (2 分钟)

- [ ] 更新 PROGRESS.md 状态
- [ ] 记录测试日期

```bash
# 更新进度
python scripts/update_progress.py \
  --task "Notion MCP 集成" \
  --status "✅ 已完成"
```

**检查点**: 进度已更新

---

## ⚠️ 常见问题

### 问题 1: 401 Unauthorized

**原因**: API Key 无效或过期

**解决**:
1. 检查 `.env` 中的 `NOTION_API_KEY`
2. 确认 Token 未过期
3. 重新生成 Token

---

### 问题 2: 403 Forbidden

**原因**: Integration 未分享到工作区

**解决**:
1. 打开 Notion 页面
2. 点击右上角 "..."
3. "Add connections" → 选择你的 Integration

---

## ✅ 完成标准

- [x] 连接测试通过
- [x] 手动验证成功
- [x] 进度已更新

---

## 🔗 链接

- **上一步**: [编写文档](./step-3-write-docs.md)
- **下一步**: 无（集成完成！）
- **返回**: [Notion MCP 任务索引](./INDEX.md)
- **继续**: [Phase 1 下一任务](../../phases/phase-1.md)

---

**最后更新**: 2025-11-27
