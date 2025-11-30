# 部署准备任务拆解

**模块**: 生产部署
**预计时间**: 1h 50min
**步骤数**: 6
**阶段**: Phase 4

---

## 📋 步骤列表

| # | 任务 | 时间 | 状态 |
|---|------|------|------|
| 1 | [生产 Dockerfile](./step-1-dockerfile.md) | 20min | 📋 |
| 2 | [Docker Compose 生产版](./step-2-compose.md) | 20min | 📋 |
| 3 | [环境变量管理](./step-3-env.md) | 15min | 📋 |
| 4 | [数据库迁移脚本](./step-4-migration.md) | 20min | 📋 |
| 5 | [Nginx 配置](./step-5-nginx.md) | 20min | 📋 |
| 6 | [SSL 证书](./step-6-ssl.md) | 15min | 📋 |

---

## 🎯 部署架构

```
Internet
    │
    ▼
[Nginx] (SSL, Reverse Proxy)
    │
    ├─► [FastAPI App] x N
    │
    ├─► [Celery Worker] x N
    │
    ├─► [PostgreSQL]
    │
    └─► [Redis]
```

---

## 🔗 链接

- **所属阶段**: [Phase 4](../../phases/phase-4.md)
- **下一步**: [上线发布](../release/INDEX.md)
