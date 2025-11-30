# AILMA API 文档

AILMA RESTful API 完整参考

---

## 基础信息

- **Base URL**: `http://localhost:8000`
- **Protocol**: HTTP/1.1
- **Content-Type**: `application/json`

---

## 认证

当前版本（v0.1.0）暂不需要认证。生产环境将使用 JWT 认证。

---

## 端点列表

### 1. 健康检查

#### GET `/`

基础健康检查

**响应示例**:
```json
{
  "service": "AILMA",
  "version": "0.1.0",
  "status": "running",
  "listener_active": true
}
```

---

#### GET `/health`

详细健康状态

**响应示例**:
```json
{
  "status": "healthy",
  "components": {
    "listener": true,
    "last_check": "2025-11-27T10:30:00+08:00"
  }
}
```

**状态码**:
- `200 OK` - 服务正常
- `503 Service Unavailable` - 服务异常

---

### 2. 指令解析

#### POST `/api/parse`

手动解析自然语言指令

**请求体**:
```json
{
  "text": "明天下午3点开会"
}
```

**响应示例**:
```json
{
  "intent": {
    "type": "calendar_create",
    "confidence": 0.95,
    "explanation": "用户想创建日历事件"
  },
  "entities": {
    "title": "开会",
    "description": null,
    "time": {
      "start": "2025-11-28T15:00:00+08:00",
      "end": null,
      "is_all_day": false
    },
    "location": null
  }
}
```

**状态码**:
- `200 OK` - 解析成功
- `400 Bad Request` - 请求格式错误
- `500 Internal Server Error` - 解析失败

---

### 3. 日历操作 (计划中)

#### POST `/api/calendar/events`

创建日历事件

**请求体**:
```json
{
  "title": "团队会议",
  "start_time": "2025-11-28T15:00:00+08:00",
  "end_time": "2025-11-28T16:00:00+08:00",
  "description": "讨论Q4计划",
  "location": "会议室A",
  "attendees": ["user1@example.com", "user2@example.com"]
}
```

**响应示例**:
```json
{
  "id": "event_abc123",
  "title": "团队会议",
  "htmlLink": "https://calendar.google.com/event?eid=abc123",
  "status": "confirmed"
}
```

---

#### GET `/api/calendar/events`

查询日历事件

**查询参数**:
- `time_min` (required): 开始时间 (ISO 8601)
- `time_max` (required): 结束时间 (ISO 8601)
- `max_results` (optional): 最大结果数，默认 100

**示例**:
```
GET /api/calendar/events?time_min=2025-11-27T00:00:00Z&time_max=2025-11-28T00:00:00Z
```

**响应示例**:
```json
{
  "events": [
    {
      "id": "event1",
      "summary": "站会",
      "start": {
        "dateTime": "2025-11-27T09:00:00+08:00"
      }
    },
    {
      "id": "event2",
      "summary": "产品评审",
      "start": {
        "dateTime": "2025-11-27T14:00:00+08:00"
      }
    }
  ],
  "count": 2
}
```

---

### 4. Notion 操作 (计划中)

#### POST `/api/notion/pages`

创建 Notion 页面

**请求体**:
```json
{
  "parent_id": "database_id",
  "title": "项目笔记",
  "content": "# 标题\n\n内容...",
  "tags": ["项目", "笔记"]
}
```

---

### 5. 报告生成 (计划中)

#### POST `/api/reports/generate`

生成报告

**请求体**:
```json
{
  "type": "weekly",  // weekly | monthly | custom
  "time_range": {
    "start": "2025-11-25T00:00:00+08:00",
    "end": "2025-12-01T00:00:00+08:00"
  }
}
```

---

## 错误响应

所有错误响应遵循统一格式：

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "人类可读的错误信息",
    "details": {
      "field": "具体错误细节"
    }
  }
}
```

### 错误码列表

| 错误码 | HTTP 状态 | 说明 |
|--------|-----------|------|
| `INVALID_REQUEST` | 400 | 请求格式错误 |
| `PARSING_FAILED` | 400 | 指令解析失败 |
| `UNAUTHORIZED` | 401 | 未授权 |
| `NOT_FOUND` | 404 | 资源不存在 |
| `RATE_LIMIT_EXCEEDED` | 429 | 请求频率超限 |
| `INTERNAL_ERROR` | 500 | 内部错误 |
| `SERVICE_UNAVAILABLE` | 503 | 服务不可用 |

---

## 速率限制

- **开发环境**: 无限制
- **生产环境**: 100 请求/分钟/用户

响应头包含速率限制信息：
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1635724800
```

---

## Webhook (计划中)

AILMA 支持 Webhook 通知事件状态变化。

### 事件类型

- `command.processing` - 指令开始处理
- `command.completed` - 指令执行成功
- `command.failed` - 指令执行失败

### Webhook 负载

```json
{
  "event": "command.completed",
  "timestamp": "2025-11-27T10:30:00+08:00",
  "data": {
    "command_id": "cmd_abc123",
    "user_input": "明天下午3点开会",
    "intent": "calendar_create",
    "result": {
      "status": "success",
      "message": "成功创建事件: 开会",
      "event_id": "event_xyz789"
    }
  }
}
```

---

## 示例代码

### Python

```python
import httpx

# 解析指令
async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/api/parse",
        json={"text": "明天下午3点开会"}
    )
    result = response.json()
    print(result["intent"]["type"])  # calendar_create
```

### cURL

```bash
# 健康检查
curl http://localhost:8000/health

# 解析指令
curl -X POST http://localhost:8000/api/parse \
  -H "Content-Type: application/json" \
  -d '{"text": "明天下午3点开会"}'
```

### JavaScript

```javascript
// 解析指令
const response = await fetch('http://localhost:8000/api/parse', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: '明天下午3点开会'
  }),
});

const result = await response.json();
console.log(result.intent.type); // calendar_create
```

---

## 变更日志

### v0.1.0 (2025-11-27)

- 初始版本
- 支持指令解析 API
- 健康检查端点

---

**最后更新**: 2025-11-27
