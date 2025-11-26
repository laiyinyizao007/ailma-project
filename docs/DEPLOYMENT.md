# AILMA 部署指南

**版本**: v1.0
**最后更新**: 2025-11-27

---

## 📋 目录

1. [部署概述](#部署概述)
2. [环境准备](#环境准备)
3. [本地部署](#本地部署)
4. [生产部署](#生产部署)
5. [Docker 部署](#docker-部署)
6. [Kubernetes 部署](#kubernetes-部署)
7. [监控和维护](#监控和维护)
8. [故障排查](#故障排查)

---

## 🎯 部署概述

### 部署架构

```
┌─────────────────────────────────────────────────┐
│              Load Balancer / CDN                │
│                   (Optional)                    │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│               Reverse Proxy                     │
│            (Nginx / Traefik)                    │
│              SSL Termination                    │
└───────────────────┬─────────────────────────────┘
                    │
       ┌────────────┴────────────┐
       │                         │
       ▼                         ▼
┌──────────────┐       ┌──────────────┐
│  Backend API │       │  Backend API │
│  (FastAPI)   │       │  (FastAPI)   │
│  Instance 1  │       │  Instance 2  │
└──────┬───────┘       └──────┬───────┘
       │                      │
       └──────────┬───────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌─────────┐  ┌─────────┐  ┌─────────┐
│PostgreSQL   │  Redis  │  │ Celery  │
│ Database│  │ Cache   │  │ Workers │
└─────────┘  └─────────┘  └─────────┘
```

---

### 部署环境类型

| 环境 | 用途 | 配置 | 特点 |
|------|------|------|------|
| **Development** | 本地开发 | 单机 Docker | 快速迭代，调试友好 |
| **Staging** | 测试环境 | 类生产配置 | 完整测试，性能验证 |
| **Production** | 生产环境 | 高可用集群 | 稳定性优先，监控完善 |

---

## 🔧 环境准备

### 最低配置要求

| 环境 | CPU | 内存 | 磁盘 | 网络 |
|------|-----|------|------|------|
| **开发** | 2 核 | 4GB | 20GB | 10Mbps |
| **Staging** | 4 核 | 8GB | 50GB | 100Mbps |
| **生产** | 8 核 | 16GB | 100GB | 1Gbps |

### 推荐配置（生产环境）

| 组件 | 配置 | 说明 |
|------|------|------|
| **应用服务器** | 4核8GB x 2台 | 运行 FastAPI 应用 |
| **数据库服务器** | 8核16GB x 1台 | PostgreSQL 主库 |
| **数据库副本** | 8核16GB x 1台 | PostgreSQL 只读副本 |
| **缓存服务器** | 4核8GB x 1台 | Redis |
| **任务队列** | 4核8GB x 2台 | Celery Workers |

---

### 依赖服务清单

| 服务 | 版本 | 用途 | 必需 |
|------|------|------|------|
| **PostgreSQL** | 15+ | 主数据库 | ✅ |
| **Redis** | 7+ | 缓存 + 任务队列 | ✅ |
| **Nginx** | 1.24+ | 反向代理 | 推荐 |
| **Supervisor** | 4.2+ | 进程管理 | 推荐 |
| **Docker** | 24+ | 容器化 | 可选 |
| **Kubernetes** | 1.28+ | 容器编排 | 可选 |

---

## 🖥️ 本地部署

### 方式 1: Docker Compose (推荐)

#### 1. 准备配置

```bash
# 克隆项目
git clone https://github.com/your-org/ailma-project.git
cd ailma-project

# 复制环境变量
cp .env.example .env

# 编辑配置
nano .env
```

**关键配置项**:
```bash
# 应用
DEBUG=False
ENVIRONMENT=production
SECRET_KEY=your-production-secret-key-change-me

# Notion MCP
NOTION_API_KEY=secret_your_token
COMMAND_CENTER_DB_ID=your_db_id
CALENDAR_DB_ID=your_db_id
REPORTS_DB_ID=your_db_id

# LLM
ANTHROPIC_API_KEY=sk-ant-your_key

# 数据库
DATABASE_URL=postgresql://ailma:strong_password@db:5432/ailma

# Redis
REDIS_URL=redis://redis:6379/0

# 安全
ENCRYPTION_KEY=your-32-byte-encryption-key-base64
```

#### 2. 启动服务

```bash
# 构建镜像
docker-compose build

# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 检查服务状态
docker-compose ps
```

#### 3. 初始化数据库

```bash
# 运行迁移
docker-compose exec backend alembic upgrade head

# 创建初始数据（可选）
docker-compose exec backend python scripts/seed_data.py
```

#### 4. 访问服务

- **API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

---

### 方式 2: 手动部署

#### 1. 安装系统依赖

**Ubuntu 22.04**:
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-dev

# 安装 PostgreSQL
sudo apt install postgresql-15 postgresql-contrib

# 安装 Redis
sudo apt install redis-server

# 安装 Nginx
sudo apt install nginx

# 安装 Supervisor
sudo apt install supervisor
```

#### 2. 创建数据库

```bash
# 切换到 postgres 用户
sudo -u postgres psql

-- 创建数据库和用户
CREATE DATABASE ailma;
CREATE USER ailma WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE ailma TO ailma;

-- 退出
\q
```

#### 3. 部署应用

```bash
# 创建应用目录
sudo mkdir -p /opt/ailma
sudo chown $USER:$USER /opt/ailma

# 克隆代码
cd /opt/ailma
git clone https://github.com/your-org/ailma-project.git .

# 创建虚拟环境
python3.11 -m venv venv
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
nano .env

# 运行迁移
alembic upgrade head
```

#### 4. 配置 Supervisor

**`/etc/supervisor/conf.d/ailma.conf`**:
```ini
[program:ailma-api]
command=/opt/ailma/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
directory=/opt/ailma
user=ailma
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/ailma/api.log
environment=PATH="/opt/ailma/venv/bin"

[program:ailma-celery-worker]
command=/opt/ailma/venv/bin/celery -A backend.tasks.celery_app worker --loglevel=info --concurrency=4
directory=/opt/ailma
user=ailma
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/ailma/celery-worker.log

[program:ailma-celery-beat]
command=/opt/ailma/venv/bin/celery -A backend.tasks.celery_app beat --loglevel=info
directory=/opt/ailma
user=ailma
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/ailma/celery-beat.log

[program:ailma-listener]
command=/opt/ailma/venv/bin/python -m backend.listeners.notion_mcp_listener
directory=/opt/ailma
user=ailma
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/ailma/listener.log
```

```bash
# 创建日志目录
sudo mkdir -p /var/log/ailma
sudo chown ailma:ailma /var/log/ailma

# 重新加载配置
sudo supervisorctl reread
sudo supervisorctl update

# 启动服务
sudo supervisorctl start ailma-api
sudo supervisorctl start ailma-celery-worker
sudo supervisorctl start ailma-celery-beat
sudo supervisorctl start ailma-listener

# 查看状态
sudo supervisorctl status
```

#### 5. 配置 Nginx

**`/etc/nginx/sites-available/ailma`**:
```nginx
upstream ailma_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name ailma.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ailma.yourdomain.com;

    # SSL 证书
    ssl_certificate /etc/letsencrypt/live/ailma.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ailma.yourdomain.com/privkey.pem;

    # SSL 配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # 日志
    access_log /var/log/nginx/ailma-access.log;
    error_log /var/log/nginx/ailma-error.log;

    # 客户端最大请求大小
    client_max_body_size 10M;

    # 代理设置
    location / {
        proxy_pass http://ailma_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket 支持（如果需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 静态文件（如果有）
    location /static {
        alias /opt/ailma/static;
        expires 30d;
    }

    # 健康检查
    location /health {
        proxy_pass http://ailma_backend/health;
        access_log off;
    }
}
```

```bash
# 启用站点
sudo ln -s /etc/nginx/sites-available/ailma /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重新加载 Nginx
sudo systemctl reload nginx
```

#### 6. 配置 SSL（Let's Encrypt）

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d ailma.yourdomain.com

# 自动续期
sudo certbot renew --dry-run
```

---

## 🐳 Docker 部署

### 完整的 docker-compose.yml

```yaml
version: '3.8'

services:
  # ============================================
  # 数据库
  # ============================================
  db:
    image: postgres:15-alpine
    container_name: ailma-postgres
    environment:
      POSTGRES_USER: ailma
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ailma
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ailma"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # ============================================
  # Redis
  # ============================================
  redis:
    image: redis:7-alpine
    container_name: ailma-redis
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # ============================================
  # Backend API
  # ============================================
  backend:
    build:
      context: .
      dockerfile: docker/Dockerfile
    container_name: ailma-backend
    command: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
    environment:
      - DATABASE_URL=postgresql://ailma:${DB_PASSWORD}@db:5432/ailma
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      - NOTION_API_KEY=${NOTION_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
      - ENCRYPTION_KEY=${ENCRYPTION_KEY}
      - DEBUG=False
      - ENVIRONMENT=production
    volumes:
      - ./backend:/app/backend
      - ./logs:/app/logs
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  # ============================================
  # Celery Worker
  # ============================================
  celery_worker:
    build:
      context: .
      dockerfile: docker/Dockerfile
    container_name: ailma-celery-worker
    command: celery -A backend.tasks.celery_app worker --loglevel=info --concurrency=4
    environment:
      - DATABASE_URL=postgresql://ailma:${DB_PASSWORD}@db:5432/ailma
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      - NOTION_API_KEY=${NOTION_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./backend:/app/backend
      - ./logs:/app/logs
    depends_on:
      - db
      - redis
    restart: unless-stopped

  # ============================================
  # Celery Beat
  # ============================================
  celery_beat:
    build:
      context: .
      dockerfile: docker/Dockerfile
    container_name: ailma-celery-beat
    command: celery -A backend.tasks.celery_app beat --loglevel=info
    environment:
      - DATABASE_URL=postgresql://ailma:${DB_PASSWORD}@db:5432/ailma
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
    volumes:
      - ./backend:/app/backend
      - ./logs:/app/logs
    depends_on:
      - db
      - redis
    restart: unless-stopped

  # ============================================
  # Nginx (Reverse Proxy)
  # ============================================
  nginx:
    image: nginx:1.24-alpine
    container_name: ailma-nginx
    volumes:
      - ./docker/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./docker/ssl:/etc/nginx/ssl:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### Dockerfile

**`docker/Dockerfile`**:
```dockerfile
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY backend/ ./backend/
COPY alembic/ ./alembic/
COPY alembic.ini .

# 创建非 root 用户
RUN useradd -m -u 1000 ailma && \
    chown -R ailma:ailma /app

USER ailma

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 默认命令
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## ☸️ Kubernetes 部署

### 1. Kubernetes 清单文件

**`k8s/deployment.yaml`**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ailma-backend
  namespace: ailma
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ailma-backend
  template:
    metadata:
      labels:
        app: ailma-backend
    spec:
      containers:
      - name: backend
        image: ailma/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: ailma-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: ailma-secrets
              key: redis-url
        - name: NOTION_API_KEY
          valueFrom:
            secretKeyRef:
              name: ailma-secrets
              key: notion-api-key
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: ailma-secrets
              key: anthropic-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

**`k8s/service.yaml`**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: ailma-backend
  namespace: ailma
spec:
  selector:
    app: ailma-backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
```

**`k8s/ingress.yaml`**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ailma-ingress
  namespace: ailma
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - ailma.yourdomain.com
    secretName: ailma-tls
  rules:
  - host: ailma.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ailma-backend
            port:
              number: 80
```

### 2. 部署到 Kubernetes

```bash
# 创建命名空间
kubectl create namespace ailma

# 创建 Secrets
kubectl create secret generic ailma-secrets \
  --from-literal=database-url="postgresql://..." \
  --from-literal=redis-url="redis://..." \
  --from-literal=notion-api-key="secret_..." \
  --from-literal=anthropic-api-key="sk-ant-..." \
  -n ailma

# 应用配置
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# 查看状态
kubectl get pods -n ailma
kubectl get svc -n ailma
kubectl get ingress -n ailma

# 查看日志
kubectl logs -f deployment/ailma-backend -n ailma
```

---

## 📊 监控和维护

### 1. 健康检查

```bash
# HTTP 健康检查
curl -f http://localhost:8000/health

# 详细健康检查
curl http://localhost:8000/health/detailed
```

### 2. 日志管理

```bash
# Supervisor 日志
sudo tail -f /var/log/ailma/api.log
sudo tail -f /var/log/ailma/celery-worker.log

# Docker 日志
docker-compose logs -f backend
docker-compose logs -f celery_worker --tail=100

# Kubernetes 日志
kubectl logs -f deployment/ailma-backend -n ailma
```

### 3. 数据库备份

```bash
# 手动备份
docker-compose exec db pg_dump -U ailma ailma > backup_$(date +%Y%m%d).sql

# 自动备份脚本
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec -T db pg_dump -U ailma ailma | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# 保留最近7天的备份
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
```

### 4. 监控指标

推荐使用 **Prometheus + Grafana**:

```bash
# 添加 Prometheus 客户端
pip install prometheus-fastapi-instrumentator

# 在 backend/main.py 添加
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)
```

---

## 🐛 故障排查

### 问题 1: 服务无法启动

```bash
# 检查日志
docker-compose logs backend

# 检查配置
docker-compose config

# 检查端口占用
sudo netstat -tulpn | grep 8000
```

### 问题 2: 数据库连接失败

```bash
# 测试连接
docker-compose exec backend python -c "from backend.database import engine; print(engine.url)"

# 检查数据库状态
docker-compose ps db
docker-compose exec db psql -U ailma -d ailma -c "SELECT 1;"
```

### 问题 3: Celery 任务不执行

```bash
# 检查 Celery 状态
docker-compose exec celery_worker celery -A backend.tasks.celery_app inspect active

# 查看队列
docker-compose exec redis redis-cli -a ${REDIS_PASSWORD} LLEN celery

# 重启 Worker
docker-compose restart celery_worker
```

---

## 📚 相关资源

- [Docker 文档](https://docs.docker.com/)
- [Kubernetes 文档](https://kubernetes.io/docs/)
- [Nginx 文档](https://nginx.org/en/docs/)
- [PostgreSQL 文档](https://www.postgresql.org/docs/)

---

**部署版本**: v1.0
**最后更新**: 2025-11-27
