# Step 6: 测试连接

**耗时**: 10 分钟 | **状态**: 📋 待开始

---

## 🎯 目标

验证 Google Calendar MCP 连接正常工作。

---

## 📋 子步骤

### 6.1 启动 MCP Server (2 分钟)

```bash
cd ~/mcp-servers/google-calendar-mcp
npm start
```

- [ ] Server 启动成功
- [ ] 看到 "MCP Server running on port 3000"

**检查点**: Server 运行中

---

### 6.2 运行连接测试 (3 分钟)

```bash
cd ~/projects/ailma-project
python tests/mcp_integration/google_calendar/test_connection.py
```

- [ ] 测试脚本运行成功

**预期输出**:
```
✅ MCP Server 连接成功
✅ 可以列出日历
✅ 可以查询事件
```

---

### 6.3 手动测试创建事件 (3 分钟)

```python
from backend.adapters.gcal_mcp_client import GoogleCalendarMCPClient

client = GoogleCalendarMCPClient()

# 创建测试事件
event = await client.create_event(
    summary="AILMA 测试事件",
    start="tomorrow 3pm",
    end="tomorrow 4pm"
)

print(f"✅ 事件创建成功: {event['htmlLink']}")
```

- [ ] 事件创建成功
- [ ] 在 Google Calendar 中可见

**检查点**: 能在日历中看到测试事件

---

### 6.4 清理测试数据 (1 分钟)

```python
# 删除测试事件
await client.delete_event(event_id=event['id'])
print("✅ 测试事件已删除")
```

- [ ] 测试事件已清理

---

### 6.5 更新进度 (1 分钟)

```bash
# 更新 PROGRESS.md
python scripts/update_progress.py \
  --task "Google Calendar MCP 集成" \
  --status "✅ 已完成"
```

- [ ] 进度已更新

---

## ⚠️ 常见问题

### 问题 1: Connection refused

**原因**: MCP Server 未启动

**解决**:
```bash
cd ~/mcp-servers/google-calendar-mcp
npm start
```

---

### 问题 2: Token expired

**原因**: OAuth Token 过期（测试环境 7 天）

**解决**:
1. 删除 `token.json`
2. 重新运行 MCP Server
3. 重新授权

---

### 问题 3: Rate limit exceeded

**原因**: API 调用超出限制

**解决**:
- 等待几分钟后重试
- 检查是否有循环调用

---

## ✅ 完成标准

- [ ] MCP Server 可以启动
- [ ] 连接测试通过
- [ ] 可以创建事件
- [ ] 可以删除事件
- [ ] 进度已更新

---

## 🎉 集成完成！

恭喜！Google Calendar MCP 集成已完成。

**下一步**:
- 继续 [Phase 1](../../phases/phase-1.md) 中的其他任务
- 或开始 [Phase 2](../../phases/phase-2.md)

---

## 🔗 链接

- **上一步**: [编写文档](./step-5-docs.md)
- **下一步**: 无（集成完成！）
- **返回**: [Google Calendar MCP 任务索引](./INDEX.md)

---

**最后更新**: 2025-11-27
