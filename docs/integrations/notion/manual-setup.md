# AILMA Notion 数据库手动配置指南

由于 Notion API 的限制，某些情况下需要手动为数据库添加属性。本指南提供详细的步骤说明。

---

## 📋 问题说明

当前使用 Notion API 创建的数据库缺少必要的属性字段。这可能是由于:

1. Notion API 版本限制
2. Integration 权限配置
3. 数据库创建时的 API 行为变化

**解决方案**: 手动在 Notion UI 中添加属性

---

## 🎯 三个数据库需要配置

### 1. 📋 指令中心 (Command Center)
**数据库 ID**: `636ef17996874d73a89216e02f8a1e44`
**访问链接**: https://www.notion.so/636ef17996874d73a89216e02f8a1e44

### 2. 📅 日历事件 (Calendar Events)
**数据库 ID**: `25233dd42bf84edaa9413de792331c66`
**访问链接**: https://www.notion.so/25233dd42bf84edaa9413de792331c66

### 3. 📊 工作报告 (Reports)
**数据库 ID**: `b39030a5821045a4997ebc7cb8bd9b8f`
**访问链接**: https://www.notion.so/b39030a5821045a4997ebc7cb8bd9b8f

---

## 🛠️ 手动配置步骤

### 准备工作

1. 在浏览器中打开 Notion
2. 确保已登录你的 Notion 账户
3. 准备好下面的属性配置表

### 数据库 1: 📋 指令中心 (Command Center)

#### 步骤 1: 打开数据库
打开链接: https://www.notion.so/636ef17996874d73a89216e02f8a1e44

#### 步骤 2: 添加属性

点击数据库表格右上角的 **"+ New"** 按钮旁边的 **"..."**，然后选择 **"Properties"**

**需要添加的 8 个属性**:

| # | 属性名 | 类型 | 配置说明 |
|---|--------|------|----------|
| 1 | 指令 | Title | 默认已存在，如不存在需添加 |
| 2 | 状态 | Select | 添加选项: pending(黄), processing(蓝), completed(绿), failed(红) |
| 3 | 意图类型 | Select | 添加选项: calendar_create(蓝), calendar_query(紫), calendar_update(橙), calendar_delete(红), notion_create_page(绿), notion_create_todo(黄), generate_report(粉), unknown(灰) |
| 4 | 置信度 | Number | 格式选择: Percent |
| 5 | 执行结果 | Text | 类型: Text |
| 6 | 错误信息 | Text | 类型: Text |
| 7 | 创建时间 | Created time | 自动属性 |
| 8 | 处理时间 | Date | 包含时间 |

#### 详细添加步骤:

**添加 "状态" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `状态`
3. 类型选择: **Select**
4. 点击 "Edit property" 添加选项:
   - `pending` - 颜色选黄色
   - `processing` - 颜色选蓝色
   - `completed` - 颜色选绿色
   - `failed` - 颜色选红色
5. 点击 **Done**

**添加 "意图类型" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `意图类型`
3. 类型选择: **Select**
4. 添加以下选项:
   - `calendar_create` - 蓝色
   - `calendar_query` - 紫色
   - `calendar_update` - 橙色
   - `calendar_delete` - 红色
   - `notion_create_page` - 绿色
   - `notion_create_todo` - 黄色
   - `generate_report` - 粉色
   - `unknown` - 灰色

**添加 "置信度" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `置信度`
3. 类型选择: **Number**
4. 点击属性，选择 "Edit property"
5. Number format 选择: **Percent**

**添加 "执行结果" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `执行结果`
3. 类型选择: **Text**

**添加 "错误信息" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `错误信息`
3. 类型选择: **Text**

**添加 "创建时间" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `创建时间`
3. 类型选择: **Created time**

**添加 "处理时间" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `处理时间`
3. 类型选择: **Date**
4. 确保选择 "Include time"

---

### 数据库 2: 📅 日历事件 (Calendar Events)

#### 步骤 1: 打开数据库
打开链接: https://www.notion.so/25233dd42bf84edaa9413de792331c66

#### 步骤 2: 添加属性

**需要添加的 10 个属性**:

| # | 属性名 | 类型 | 配置说明 |
|---|--------|------|----------|
| 1 | 事件标题 | Title | 默认已存在 |
| 2 | 开始时间 | Date | 包含时间 |
| 3 | 地点 | Text | 文本类型 |
| 4 | 参与者 | Multi-select | 初始为空，使用时添加 |
| 5 | 事件类型 | Select | 会议(蓝), 个人(绿), 团队活动(紫), 培训(橙), 其他(灰) |
| 6 | 状态 | Select | 已计划(黄), 进行中(蓝), 已完成(绿), 已取消(红) |
| 7 | Google Calendar ID | Text | 文本类型 |
| 8 | Meet 链接 | URL | URL类型 |
| 9 | 描述 | Text | 文本类型 |
| 10 | 创建时间 | Created time | 自动属性 |

#### 详细添加步骤:

**添加 "开始时间" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `开始时间`
3. 类型选择: **Date**
4. 确保勾选 "Include time"

**添加 "地点" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `地点`
3. 类型选择: **Text**

**添加 "参与者" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `参与者`
3. 类型选择: **Multi-select**
4. 暂不添加选项（使用时动态添加）

**添加 "事件类型" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `事件类型`
3. 类型选择: **Select**
4. 添加选项:
   - `会议` - 蓝色
   - `个人` - 绿色
   - `团队活动` - 紫色
   - `培训` - 橙色
   - `其他` - 灰色

**添加 "状态" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `状态`
3. 类型选择: **Select**
4. 添加选项:
   - `已计划` - 黄色
   - `进行中` - 蓝色
   - `已完成` - 绿色
   - `已取消` - 红色

**添加 "Google Calendar ID" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `Google Calendar ID`
3. 类型选择: **Text**

**添加 "Meet 链接" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `Meet 链接`
3. 类型选择: **URL**

**添加 "描述" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `描述`
3. 类型选择: **Text**

**添加 "创建时间" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `创建时间`
3. 类型选择: **Created time**

---

### 数据库 3: 📊 工作报告 (Reports)

#### 步骤 1: 打开数据库
打开链接: https://www.notion.so/b39030a5821045a4997ebc7cb8bd9b8f

#### 步骤 2: 添加属性

**需要添加的 8 个属性**:

| # | 属性名 | 类型 | 配置说明 |
|---|--------|------|----------|
| 1 | 报告标题 | Title | 默认已存在 |
| 2 | 报告类型 | Select | 日报(蓝), 周报(绿), 月报(紫), 季度报告(橙), 年度总结(红) |
| 3 | 时间范围 | Date | 日期范围 |
| 4 | 事件统计 | Number | 数字 |
| 5 | 会议时长 | Number | 格式: Number with commas |
| 6 | 生成时间 | Created time | 自动属性 |
| 7 | 状态 | Select | 草稿(黄), 已完成(绿), 已归档(灰) |
| 8 | 标签 | Multi-select | 重要(红), 团队(蓝), 个人(绿) |

#### 详细添加步骤:

**添加 "报告类型" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `报告类型`
3. 类型选择: **Select**
4. 添加选项:
   - `日报` - 蓝色
   - `周报` - 绿色
   - `月报` - 紫色
   - `季度报告` - 橙色
   - `年度总结` - 红色

**添加 "时间范围" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `时间范围`
3. 类型选择: **Date**
4. 确保选择 "End date" 以支持日期范围

**添加 "事件统计" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `事件统计`
3. 类型选择: **Number**

**添加 "会议时长" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `会议时长`
3. 类型选择: **Number**
4. 点击 "Edit property"
5. Number format 选择: **Number with commas**

**添加 "生成时间" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `生成时间`
3. 类型选择: **Created time**

**添加 "状态" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `状态`
3. 类型选择: **Select**
4. 添加选项:
   - `草稿` - 黄色
   - `已完成` - 绿色
   - `已归档` - 灰色

**添加 "标签" 属性**:
1. 点击 **"+ Add a property"**
2. 属性名输入: `标签`
3. 类型选择: **Multi-select**
4. 添加选项:
   - `重要` - 红色
   - `团队` - 蓝色
   - `个人` - 绿色

---

## ✅ 验证配置

完成所有配置后，运行验证脚本:

```bash
source venv/bin/activate
python scripts/verify-notion-databases.py
```

应该看到所有属性都显示为 ✅ 成功。

---

## 📸 配置截图参考

### 如何添加属性

1. **打开数据库**
   - 点击数据库视图

2. **查看属性面板**
   - 点击右上角 "..." 菜单
   - 选择 "Properties"

3. **添加新属性**
   - 点击 "+ Add a property"
   - 输入属性名
   - 选择类型

4. **配置 Select 选项**
   - 点击属性
   - 选择 "Edit property"
   - 点击 "+ Add an option"
   - 输入选项名并选择颜色

---

## 🔧 常见问题

### Q1: 找不到数据库
**A**: 确保你已经用正确的 Notion 账户登录，并且 Integration 已经分享给父页面。

### Q2: 无法添加属性
**A**: 检查你的 Notion 权限。如果是工作区数据库，需要管理员权限。

### Q3: 属性类型选错了
**A**: 可以删除属性重新添加，或者在属性设置中更改类型（部分类型支持转换）。

### Q4: Select 选项颜色不对
**A**: 颜色是建议配置，不影响功能，可以按个人喜好调整。

---

## 📝 配置检查清单

配置完成后，请确认:

- [ ] 📋 指令中心: 8 个属性全部配置
- [ ] 📅 日历事件: 10 个属性全部配置
- [ ] 📊 工作报告: 8 个属性全部配置
- [ ] 运行验证脚本通过
- [ ] 每个数据库都已分享给 Integration

---

## 🚀 下一步

配置完成后:

1. ✅ 配置 Claude API Key（如果还没有）
2. ✅ 运行配置检查: `./scripts/check-config.sh`
3. ✅ 测试 API 连接: `python scripts/test-api-connections.py`
4. ✅ 启动 AILMA 服务: `python -m src.main`

---

**最后更新**: 2025-11-30
**维护者**: AILMA Project Team
