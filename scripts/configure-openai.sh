#!/bin/bash

# AILMA OpenAI 配置向导

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}AILMA OpenAI API 配置向导${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""

# 检查 .env 文件
if [ ! -f .env ]; then
    echo -e "${RED}❌ .env 文件不存在${NC}"
    exit 1
fi

echo -e "${BLUE}🔐 安全提醒:${NC}"
echo -e "${RED}⚠️  你之前在对话中暴露的 API Key 已经不安全了！${NC}"
echo ""
echo "请立即采取以下步骤："
echo "1. 前往 https://platform.openai.com/api-keys"
echo "2. 找到并${RED}删除${NC}暴露的密钥"
echo "3. 创建一个${GREEN}新密钥${NC}"
echo ""
echo -e "${YELLOW}按任意键继续...${NC}"
read -n 1 -s

echo ""
echo -e "${BLUE}📋 配置步骤:${NC}"
echo ""

# 提示用户输入 API Key
echo -e "${YELLOW}请输入你的新 OpenAI API Key:${NC}"
echo -e "${BLUE}(输入时不会显示，这是正常的安全措施)${NC}"
read -s OPENAI_KEY

echo ""

# 验证 API Key 格式
if [[ ! $OPENAI_KEY =~ ^sk-proj-.*$ ]] && [[ ! $OPENAI_KEY =~ ^sk-.*$ ]]; then
    echo -e "${RED}❌ API Key 格式不正确${NC}"
    echo -e "${YELLOW}OpenAI API Key 应该以 'sk-' 或 'sk-proj-' 开头${NC}"
    exit 1
fi

# 更新 .env 文件
echo -e "${BLUE}📝 更新 .env 文件...${NC}"

# 备份 .env
cp .env .env.backup
echo -e "${GREEN}✅ 已备份 .env 到 .env.backup${NC}"

# 更新配置
sed -i "s|OPENAI_API_KEY=.*|OPENAI_API_KEY=$OPENAI_KEY|" .env
sed -i "s|LLM_PROVIDER=.*|LLM_PROVIDER=openai|" .env
sed -i "s|LLM_MODEL=.*|LLM_MODEL=gpt-4o-mini|" .env

echo -e "${GREEN}✅ .env 文件已更新${NC}"
echo ""

# 测试 API 连接
echo -e "${BLUE}🔍 测试 OpenAI API 连接...${NC}"

# 创建测试脚本 (使用新版 OpenAI API)
cat > /tmp/test_openai.py << 'EOF'
import os
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

try:
    # 创建客户端 (新版 API)
    client = OpenAI(api_key=api_key)

    # 简单的 API 测试
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say 'OK' if you can hear me"}],
        max_tokens=10
    )

    print("✅ OpenAI API 连接成功！")
    print(f"响应: {response.choices[0].message.content}")
    exit(0)
except AuthenticationError:
    print("❌ API Key 无效")
    exit(1)
except Exception as e:
    print(f"❌ 连接失败: {str(e)}")
    exit(1)
EOF

# 运行测试
source venv/bin/activate
python /tmp/test_openai.py

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✅ 配置成功！${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${BLUE}下一步:${NC}"
    echo "  1. 验证 Notion 数据库: python scripts/verify-raw-api.py"
    echo "  2. 测试完整配置: ./scripts/check-config.sh"
    echo "  3. 启动 AILMA: python -m src.main"
else
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}❌ 配置失败${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
    echo -e "${YELLOW}请检查:${NC}"
    echo "  1. API Key 是否正确"
    echo "  2. OpenAI 账户是否有余额"
    echo "  3. 网络连接是否正常"
    echo ""
    echo "恢复备份: mv .env.backup .env"
fi

# 清理临时文件
rm -f /tmp/test_openai.py
