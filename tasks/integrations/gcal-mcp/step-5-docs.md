# Step 5: 编写文档

**耗时**: 30 分钟 | **状态**: 📋 待开始

---

## 🎯 目标

为 Google Calendar MCP 集成编写完整文档。

---

## 📋 子步骤

### 5.1 创建目录结构 (1 分钟)

```bash
mkdir -p docs/integrations/google-calendar
```

- [ ] 目录已创建

---

### 5.2 编写 README.md (10 分钟)

**文件**: `docs/integrations/google-calendar/README.md`

**内容大纲**:
- [ ] 概述 (~30 行)
- [ ] 核心特性 (~20 行)
  - 自然语言时间解析
  - 自动 Meet 链接
  - 多日历支持
- [ ] 快速开始链接 (~20 行)
- [ ] 相关文档链接 (~10 行)

**检查点**: README.md < 100 行

---

### 5.3 编写 mcp-setup.md (10 分钟)

**文件**: `docs/integrations/google-calendar/mcp-setup.md`

**内容大纲**:
- [ ] 前置要求 (~20 行)
- [ ] GCP 配置（链接到详细步骤）(~20 行)
- [ ] MCP Server 安装 (~40 行)
- [ ] 环境变量配置 (~30 行)
- [ ] 验证方法 (~20 行)

**检查点**: mcp-setup.md < 150 行

---

### 5.4 编写 tools-reference.md (10 分钟)

**文件**: `docs/integrations/google-calendar/tools-reference.md`

**7 个工具**:
- [ ] `list_events()` (~20 行)
- [ ] `create_event()` (~25 行)
- [ ] `update_event()` (~15 行)
- [ ] `delete_event()` (~10 行)
- [ ] `search_events()` (~15 行)
- [ ] `get_free_busy()` (~20 行)
- [ ] `list_calendars()` (~10 行)

**检查点**: tools-reference.md < 180 行

---

### 5.5 更新索引 (2 分钟)

- [ ] 更新 `docs/INDEX.md`
- [ ] 添加 Google Calendar 链接

---

## ✅ 完成标准

- [ ] README.md < 100 行
- [ ] mcp-setup.md < 150 行
- [ ] tools-reference.md < 180 行
- [ ] INDEX.md 已更新

---

## 🔗 链接

- **上一步**: [安装 MCP Server](./step-4-mcp-server.md)
- **下一步**: [测试连接](./step-6-test.md)
- **返回**: [Google Calendar MCP 任务索引](./INDEX.md)

---

**最后更新**: 2025-11-27
