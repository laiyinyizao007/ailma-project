# AILMA API 文档

**版本**: v1.0
**Base URL**: `https://api.ailma.yourdomain.com/api/v1`
**最后更新**: 2025-11-27

---

## 📋 目录

1. [API 概述](#api-概述)
2. [认证](#认证)
3. [通用规范](#通用规范)
4. [健康检查](#健康检查)
5. [命令管理](#命令管理)
6. [日历管理](#日历管理)
7. [报告管理](#报告管理)
8. [用户管理](#用户管理)
9. [错误处理](#错误处理)

---

## 🎯 API 概述

AILMA 提供 RESTful API 用于管理用户指令、日历事件和自动化报告。

### API 特性

- ✅ RESTful 设计
- ✅ JWT 认证
- ✅ JSON 格式
- ✅ 速率限制
- ✅ 版本控制
- ✅ OpenAPI 3.0 规范

### 交互式文档

访问以下 URL 查看和测试 API:

- **Swagger UI**: `https://api.ailma.yourdomain.com/docs`
- **ReDoc**: `https://api.ailma.yourdomain.com/redoc`

---

## 🔐 认证

### JWT Token 认证

所有需要认证的端点都使用 JWT Bearer Token。

#### 获取 Token

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your_password"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

#### 使用 Token

```http
GET /api/v1/commands
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📖 通用规范

### HTTP 方法

| 方法 | 用途 | 幂等性 |
|------|------|--------|
| `GET` | 获取资源 | ✅ |
| `POST` | 创建资源 | ❌ |
| `PUT` | 完整更新资源 | ✅ |
| `PATCH` | 部分更新资源 | ❌ |
| `DELETE` | 删除资源 | ✅ |

### 状态码

| 状态码 | 含义 | 说明 |
|--------|------|------|
| `200` | OK | 请求成功 |
| `201` | Created | 资源创建成功 |
| `204` | No Content | 成功但无返回内容 |
| `400` | Bad Request | 请求参数错误 |
| `401` | Unauthorized | 未认证 |
| `403` | Forbidden | 无权限 |
| `404` | Not Found | 资源不存在 |
| `422` | Unprocessable Entity | 验证失败 |
| `429` | Too Many Requests | 请求过于频繁 |
| `500` | Internal Server Error | 服务器错误 |

### 分页

使用 `limit` 和 `offset` 参数进行分页：

```http
GET /api/v1/commands?limit=20&offset=40
```

**Response**:
```json
{
  "data": [...],
  "total": 156,
  "limit": 20,
  "offset": 40,
  "has_more": true
}
```

### 排序

使用 `sort` 参数进行排序：

```http
GET /api/v1/commands?sort=-created_at,title
```

- `-` 前缀表示降序
- 默认升序

### 过滤

使用字段名作为查询参数：

```http
GET /api/v1/commands?status=completed&user_id=123
```

---

## ❤️ 健康检查

### 简单健康检查

```http
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "service": "ailma-backend",
  "version": "1.0.0",
  "timestamp": "2025-11-27T10:30:00Z"
}
```

### 详细健康检查

```http
GET /health/detailed
```

**Response**:
```json
{
  "status": "healthy",
  "service": "ailma-backend",
  "version": "1.0.0",
  "timestamp": "2025-11-27T10:30:00Z",
  "checks": {
    "database": {
      "status": "healthy",
      "response_time_ms": 5
    },
    "redis": {
      "status": "healthy",
      "response_time_ms": 2
    },
    "notion_mcp": {
      "status": "healthy",
      "response_time_ms": 150
    }
  }
}
```

---

## 📝 命令管理

### 创建命令

```http
POST /api/v1/commands
Authorization: Bearer {token}
Content-Type: application/json

{
  "instruction": "帮我把明天下午3点的团队会议加到日历",
  "priority": "normal"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "instruction": "帮我把明天下午3点的团队会议加到日历",
  "status": "pending",
  "priority": "normal",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2025-11-27T10:30:00Z",
  "updated_at": "2025-11-27T10:30:00Z"
}
```

### 获取命令列表

```http
GET /api/v1/commands?status=pending&limit=20
Authorization: Bearer {token}
```

**Response**:
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "instruction": "帮我把明天下午3点的团队会议加到日历",
      "status": "pending",
      "priority": "normal",
      "created_at": "2025-11-27T10:30:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "instruction": "生成本周工作总结报告",
      "status": "processing",
      "priority": "high",
      "created_at": "2025-11-27T10:25:00Z"
    }
  ],
  "total": 45,
  "limit": 20,
  "offset": 0,
  "has_more": true
}
```

### 获取单个命令

```http
GET /api/v1/commands/{command_id}
Authorization: Bearer {token}
```

**Response**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "instruction": "帮我把明天下午3点的团队会议加到日历",
  "status": "completed",
  "priority": "normal",
  "result": {
    "message": "✅ 已成功创建事件：团队会议",
    "event_url": "https://calendar.google.com/event?eid=...",
    "notion_page_url": "https://notion.so/..."
  },
  "intent": "calendar_create",
  "entities": {
    "event_title": "团队会议",
    "start_time": "2025-11-28T15:00:00",
    "duration_minutes": 60
  },
  "processing_time_ms": 2350,
  "error_message": null,
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2025-11-27T10:30:00Z",
  "updated_at": "2025-11-27T10:30:02Z",
  "completed_at": "2025-11-27T10:30:02Z"
}
```

### 取消命令

```http
DELETE /api/v1/commands/{command_id}
Authorization: Bearer {token}
```

**Response** (204 No Content)

---

## 📅 日历管理

### 创建日历事件

```http
POST /api/v1/calendar/events
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "团队会议",
  "start_time": "2025-11-28T15:00:00Z",
  "end_time": "2025-11-28T16:00:00Z",
  "description": "讨论 Q4 产品规划",
  "location": "会议室 A",
  "attendees": ["colleague@example.com"]
}
```

**Response** (201 Created):
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440002",
  "external_id": "google_cal_event_123",
  "title": "团队会议",
  "start_time": "2025-11-28T15:00:00Z",
  "end_time": "2025-11-28T16:00:00Z",
  "description": "讨论 Q4 产品规划",
  "location": "会议室 A",
  "attendees": ["colleague@example.com"],
  "source": "google",
  "event_url": "https://calendar.google.com/event?eid=...",
  "created_at": "2025-11-27T10:35:00Z"
}
```

### 获取日历事件列表

```http
GET /api/v1/calendar/events?start_date=2025-11-01&end_date=2025-11-30
Authorization: Bearer {token}
```

**Response**:
```json
{
  "data": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "title": "团队会议",
      "start_time": "2025-11-28T15:00:00Z",
      "end_time": "2025-11-28T16:00:00Z",
      "source": "google",
      "event_url": "https://calendar.google.com/event?eid=..."
    },
    {
      "id": "880e8400-e29b-41d4-a716-446655440003",
      "title": "客户演示",
      "start_time": "2025-11-29T10:00:00Z",
      "end_time": "2025-11-29T11:30:00Z",
      "source": "outlook",
      "event_url": "https://outlook.office.com/..."
    }
  ],
  "total": 15,
  "start_date": "2025-11-01",
  "end_date": "2025-11-30"
}
```

### 更新日历事件

```http
PATCH /api/v1/calendar/events/{event_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "start_time": "2025-11-28T16:00:00Z",
  "end_time": "2025-11-28T17:00:00Z"
}
```

**Response**:
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440002",
  "title": "团队会议",
  "start_time": "2025-11-28T16:00:00Z",
  "end_time": "2025-11-28T17:00:00Z",
  "updated_at": "2025-11-27T10:40:00Z"
}
```

### 删除日历事件

```http
DELETE /api/v1/calendar/events/{event_id}
Authorization: Bearer {token}
```

**Response** (204 No Content)

---

## 📊 报告管理

### 生成报告

```http
POST /api/v1/reports
Authorization: Bearer {token}
Content-Type: application/json

{
  "report_type": "weekly",
  "start_date": "2025-11-24",
  "end_date": "2025-11-30",
  "include_calendar": true,
  "include_notion_tasks": true
}
```

**Response** (202 Accepted):
```json
{
  "id": "990e8400-e29b-41d4-a716-446655440004",
  "report_type": "weekly",
  "status": "generating",
  "start_date": "2025-11-24",
  "end_date": "2025-11-30",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2025-11-27T10:45:00Z",
  "estimated_completion_time": "2025-11-27T10:45:30Z"
}
```

### 获取报告状态

```http
GET /api/v1/reports/{report_id}
Authorization: Bearer {token}
```

**Response**:
```json
{
  "id": "990e8400-e29b-41d4-a716-446655440004",
  "report_type": "weekly",
  "status": "completed",
  "start_date": "2025-11-24",
  "end_date": "2025-11-30",
  "notion_page_url": "https://notion.so/2025-W48-report",
  "summary": {
    "total_meetings": 12,
    "total_hours": 18,
    "tasks_completed": 23,
    "key_achievements": [
      "完成用户研究报告",
      "发布 v2.0 版本"
    ]
  },
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2025-11-27T10:45:00Z",
  "completed_at": "2025-11-27T10:45:25Z"
}
```

### 获取报告列表

```http
GET /api/v1/reports?report_type=weekly&limit=10
Authorization: Bearer {token}
```

**Response**:
```json
{
  "data": [
    {
      "id": "990e8400-e29b-41d4-a716-446655440004",
      "report_type": "weekly",
      "status": "completed",
      "start_date": "2025-11-24",
      "end_date": "2025-11-30",
      "notion_page_url": "https://notion.so/2025-W48-report",
      "created_at": "2025-11-27T10:45:00Z"
    }
  ],
  "total": 8,
  "limit": 10,
  "offset": 0
}
```

---

## 👤 用户管理

### 注册用户

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "newuser@example.com",
  "password": "SecurePassword123!",
  "username": "newuser"
}
```

**Response** (201 Created):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "newuser@example.com",
  "username": "newuser",
  "created_at": "2025-11-27T10:50:00Z"
}
```

### 获取当前用户信息

```http
GET /api/v1/users/me
Authorization: Bearer {token}
```

**Response**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "username": "user",
  "settings": {
    "timezone": "Asia/Shanghai",
    "language": "zh-CN",
    "notion_workspace_id": "workspace_123",
    "default_calendar": "google"
  },
  "created_at": "2025-11-20T08:00:00Z",
  "updated_at": "2025-11-27T10:00:00Z"
}
```

### 更新用户设置

```http
PATCH /api/v1/users/me/settings
Authorization: Bearer {token}
Content-Type: application/json

{
  "timezone": "America/New_York",
  "language": "en-US"
}
```

**Response**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "settings": {
    "timezone": "America/New_York",
    "language": "en-US",
    "notion_workspace_id": "workspace_123",
    "default_calendar": "google"
  },
  "updated_at": "2025-11-27T11:00:00Z"
}
```

---

## ⚠️ 错误处理

### 错误响应格式

所有错误都遵循统一格式：

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数验证失败",
    "details": [
      {
        "field": "start_time",
        "message": "start_time 不能早于当前时间"
      }
    ],
    "request_id": "req_123abc",
    "timestamp": "2025-11-27T11:05:00Z"
  }
}
```

### 错误代码

| 错误代码 | HTTP 状态码 | 说明 |
|---------|------------|------|
| `VALIDATION_ERROR` | 422 | 请求参数验证失败 |
| `AUTHENTICATION_REQUIRED` | 401 | 需要认证 |
| `INSUFFICIENT_PERMISSIONS` | 403 | 权限不足 |
| `RESOURCE_NOT_FOUND` | 404 | 资源不存在 |
| `RATE_LIMIT_EXCEEDED` | 429 | 超过速率限制 |
| `EXTERNAL_SERVICE_ERROR` | 502 | 外部服务错误 |
| `INTERNAL_SERVER_ERROR` | 500 | 服务器内部错误 |

### 速率限制

API 实施速率限制以确保服务质量：

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 998
X-RateLimit-Reset: 1638000000
```

当超过限制时：

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "您已超过速率限制，请稍后重试",
    "retry_after": 60
  }
}
```

---

## 📚 代码示例

### Python

```python
import httpx
import asyncio

BASE_URL = "https://api.ailma.yourdomain.com/api/v1"
TOKEN = "your_jwt_token"

async def create_command(instruction: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/commands",
            json={"instruction": instruction},
            headers={"Authorization": f"Bearer {TOKEN}"}
        )
        response.raise_for_status()
        return response.json()

# 使用
result = asyncio.run(create_command("生成本周工作总结"))
print(result)
```

### JavaScript

```javascript
const BASE_URL = "https://api.ailma.yourdomain.com/api/v1";
const TOKEN = "your_jwt_token";

async function createCommand(instruction) {
  const response = await fetch(`${BASE_URL}/commands`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${TOKEN}`
    },
    body: JSON.stringify({ instruction })
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
}

// 使用
createCommand("生成本周工作总结")
  .then(result => console.log(result))
  .catch(error => console.error(error));
```

### cURL

```bash
# 创建命令
curl -X POST https://api.ailma.yourdomain.com/api/v1/commands \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_jwt_token" \
  -d '{"instruction": "生成本周工作总结"}'

# 获取命令列表
curl -X GET "https://api.ailma.yourdomain.com/api/v1/commands?status=completed&limit=10" \
  -H "Authorization: Bearer your_jwt_token"
```

---

## 🔗 相关链接

- [交互式 API 文档 (Swagger)](https://api.ailma.yourdomain.com/docs)
- [API 文档 (ReDoc)](https://api.ailma.yourdomain.com/redoc)
- [OpenAPI 规范文件](https://api.ailma.yourdomain.com/openapi.json)
- [开发指南](./DEVELOPMENT.md)
- [部署指南](./DEPLOYMENT.md)

---

**API 版本**: v1.0
**最后更新**: 2025-11-27
