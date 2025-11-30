#!/bin/bash
# AILMA 配置检查脚本

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}AILMA 配置检查${NC}"
echo "================================"
echo ""

# 加载 .env 文件
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env 文件不存在${NC}"
    echo "请运行: cp .env.example .env"
    exit 1
fi

echo -e "${GREEN}✓${NC} 找到 .env 文件"
echo ""

# 加载环境变量
set -a
source .env
set +a

# 检查必需的 API Keys
echo "检查必需配置..."
echo "---"

MISSING_REQUIRED=0

# Notion API Key
if [ -z "$NOTION_API_KEY" ] || [ "$NOTION_API_KEY" = "secret_your_notion_integration_token_here" ]; then
    echo -e "${RED}❌ NOTION_API_KEY${NC} 未配置"
    echo "   获取方法: https://www.notion.so/my-integrations"
    MISSING_REQUIRED=1
else
    echo -e "${GREEN}✅ NOTION_API_KEY${NC} 已配置"
fi

# Anthropic API Key
if [ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" = "sk-ant-your_api_key_here" ]; then
    echo -e "${RED}❌ ANTHROPIC_API_KEY${NC} 未配置"
    echo "   获取方法: https://console.anthropic.com/settings/keys"
    MISSING_REQUIRED=1
else
    echo -e "${GREEN}✅ ANTHROPIC_API_KEY${NC} 已配置"
fi

echo ""
echo "检查可选配置..."
echo "---"

# Google Calendar
if [ -z "$GOOGLE_CALENDAR_MCP_SERVER_URL" ] || [ "$GOOGLE_CALENDAR_MCP_SERVER_URL" = "http://localhost:3000/mcp" ]; then
    echo -e "${YELLOW}⚠️  GOOGLE_CALENDAR_MCP_SERVER_URL${NC} 使用默认值（可选）"
else
    echo -e "${GREEN}✅ GOOGLE_CALENDAR_MCP_SERVER_URL${NC} 已配置"
fi

# Database
if [ -z "$DATABASE_URL" ]; then
    echo -e "${YELLOW}⚠️  DATABASE_URL${NC} 未配置（可选）"
else
    echo -e "${GREEN}✅ DATABASE_URL${NC} 已配置"
fi

# Redis
if [ -z "$REDIS_URL" ]; then
    echo -e "${YELLOW}⚠️  REDIS_URL${NC} 未配置（可选）"
else
    echo -e "${GREEN}✅ REDIS_URL${NC} 已配置"
fi

echo ""
echo "检查应用配置..."
echo "---"

# Secret Key
if [ -z "$SECRET_KEY" ] || [ "$SECRET_KEY" = "your-super-secret-key-change-in-production" ]; then
    echo -e "${YELLOW}⚠️  SECRET_KEY${NC} 使用默认值（生产环境请更改）"
else
    echo -e "${GREEN}✅ SECRET_KEY${NC} 已配置"
fi

# Environment
if [ -z "$ENVIRONMENT" ]; then
    echo -e "${YELLOW}⚠️  ENVIRONMENT${NC} 未配置，使用默认值 'development'"
else
    echo -e "${GREEN}✅ ENVIRONMENT${NC} = $ENVIRONMENT"
fi

# Debug
if [ -z "$DEBUG" ]; then
    echo -e "${YELLOW}⚠️  DEBUG${NC} 未配置，使用默认值 'True'"
else
    echo -e "${GREEN}✅ DEBUG${NC} = $DEBUG"
fi

echo ""
echo "================================"

if [ $MISSING_REQUIRED -eq 1 ]; then
    echo -e "${RED}❌ 配置检查失败${NC}"
    echo ""
    echo "缺少必需的 API Keys，请参考文档:"
    echo "  docs/guides/api-keys-setup.md"
    echo ""
    exit 1
else
    echo -e "${GREEN}✅ 配置检查通过${NC}"
    echo ""
    echo "下一步:"
    echo "  1. 运行测试: ./scripts/run-tests.sh"
    echo "  2. 启动应用: python -m uvicorn src.main:app --reload"
    echo ""
    exit 0
fi
