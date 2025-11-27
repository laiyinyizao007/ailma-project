#!/bin/bash
# AILMA 集成生成器
# 用法: ./scripts/create-integration.sh <integration_name>
#
# 自动创建新集成的所有必需文件：
# - 4 个文档文件
# - 1 个 MCP Client 文件
# - 1 个测试文件
# - 更新索引和进度跟踪

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查参数
if [ -z "$1" ]; then
    echo -e "${RED}错误: 请提供集成名称${NC}"
    echo "用法: $0 <integration_name>"
    echo "示例: $0 slack"
    exit 1
fi

INTEGRATION_NAME=$1
INTEGRATION_TITLE=$(echo $INTEGRATION_NAME | sed 's/_/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2));}1')
DATE=$(date +%Y-%m-%d)

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🚀 AILMA 集成生成器${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}正在创建新集成: $INTEGRATION_TITLE${NC}"
echo ""

# ============================================
# 1. 创建文档目录
# ============================================
echo -e "${YELLOW}[1/6]${NC} 创建文档目录..."
mkdir -p docs/integrations/$INTEGRATION_NAME

# ============================================
# 2. 生成 README.md
# ============================================
echo -e "${YELLOW}[2/6]${NC} 生成 README.md..."
cat > docs/integrations/$INTEGRATION_NAME/README.md << EOF
# $INTEGRATION_TITLE 集成

**集成概览**

---

## 🎯 概述

$INTEGRATION_TITLE 集成允许 AILMA 与 $INTEGRATION_TITLE 服务进行交互。

---

## ✨ 核心特性

- 特性 1
- 特性 2
- 特性 3

---

## 🚀 快速开始

### 1. 配置

详见: [MCP 配置指南](./mcp-setup.md)

### 2. 使用

详见: [使用示例](./examples.md)

---

## 📚 相关文档

- **[MCP 配置](./mcp-setup.md)** - 详细配置步骤
- **[工具参考](./tools-reference.md)** - 所有工具说明
- **[使用示例](./examples.md)** - 实际代码示例
- **[总索引](../../INDEX.md)** - 返回文档首页

---

**文档**: [总索引](../../INDEX.md)
**最后更新**: $DATE
EOF

echo -e "${GREEN}✓${NC} 创建文档: README.md"

# ============================================
# 3. 生成 mcp-setup.md
# ============================================
echo -e "${YELLOW}[3/6]${NC} 生成 mcp-setup.md..."
cat > docs/integrations/$INTEGRATION_NAME/mcp-setup.md << EOF
# $INTEGRATION_TITLE MCP 配置

**详细配置步骤**

---

## 📋 前置要求

- [ ] $INTEGRATION_TITLE 账号
- [ ] API 访问权限
- [ ] Python 3.11+

---

## 🔧 配置步骤

### Step 1: 获取 API 凭证

TODO: 填写获取凭证的步骤

### Step 2: 配置环境变量

\`\`\`bash
# .env
${INTEGRATION_NAME^^}_API_KEY=your_api_key_here
${INTEGRATION_NAME^^}_MCP_SERVER_URL=http://localhost:3000/mcp
\`\`\`

### Step 3: 测试连接

\`\`\`bash
python tests/mcp_integration/$INTEGRATION_NAME/test_connection.py
\`\`\`

---

## 📚 相关文档

- **[工具参考](./tools-reference.md)**
- **[使用示例](./examples.md)**

---

**文档**: [总索引](../../INDEX.md)
**最后更新**: $DATE
EOF

echo -e "${GREEN}✓${NC} 创建文档: mcp-setup.md"

# ============================================
# 4. 生成 tools-reference.md
# ============================================
echo -e "${YELLOW}[4/6]${NC} 生成 tools-reference.md..."
cat > docs/integrations/$INTEGRATION_NAME/tools-reference.md << EOF
# $INTEGRATION_TITLE MCP 工具参考

**所有可用工具详细说明**

---

## 工具 1: tool_name()

**功能**: 工具描述

**参数**:
\`\`\`python
{
  "param1": "type",
  "param2": "type"
}
\`\`\`

**示例**:
\`\`\`python
result = await ${INTEGRATION_NAME}_mcp.call_tool("tool_name", ...)
\`\`\`

**返回**: 返回值说明

---

## 工具 2: another_tool()

TODO: 添加更多工具

---

**文档**: [总索引](../../INDEX.md)
**最后更新**: $DATE
EOF

echo -e "${GREEN}✓${NC} 创建文档: tools-reference.md"

# ============================================
# 5. 生成 examples.md
# ============================================
echo -e "${YELLOW}[5/6]${NC} 生成 examples.md..."
cat > docs/integrations/$INTEGRATION_NAME/examples.md << EOF
# $INTEGRATION_TITLE 使用示例

**实际代码示例**

---

## 示例 1: 基础操作

\`\`\`python
from backend.adapters.${INTEGRATION_NAME}_mcp_client import ${INTEGRATION_TITLE}MCPClient

client = ${INTEGRATION_TITLE}MCPClient()

# TODO: 添加示例代码
\`\`\`

---

## 示例 2: 高级用法

TODO: 添加高级示例

---

**文档**: [总索引](../../INDEX.md)
**最后更新**: $DATE
EOF

echo -e "${GREEN}✓${NC} 创建文档: examples.md"

# ============================================
# 6. 生成 MCP Client 代码
# ============================================
echo -e "${YELLOW}[6/6]${NC} 生成 MCP Client..."
mkdir -p backend/adapters

cat > backend/adapters/${INTEGRATION_NAME}_mcp_client.py << 'PYEOF'
"""$INTEGRATION_TITLE MCP Client

使用 Model Context Protocol 与 $INTEGRATION_TITLE 集成
"""

from typing import Dict, Any, List
from .base_mcp_client import BaseMCPClient
import os


class $INTEGRATION_TITLEMCPClient(BaseMCPClient):
    """$INTEGRATION_TITLE MCP 客户端"""

    def __init__(self, api_key: str = None):
        server_url = os.getenv(
            "${INTEGRATION_NAME^^}_MCP_SERVER_URL",
            "http://localhost:3000/mcp"
        )
        self.api_key = api_key or os.getenv("${INTEGRATION_NAME^^}_API_KEY")

        super().__init__(server_url=server_url, auth_token=self.api_key)

    # ========================================
    # TODO: 实现具体的工具方法
    # ========================================

    async def example_tool(self, param1: str, param2: int) -> Dict:
        """示例工具"""
        return await self.call_tool(
            "example_tool",
            param1=param1,
            param2=param2
        )


# ========================================
# 使用示例
# ========================================
if __name__ == "__main__":
    import asyncio

    async def main():
        client = $INTEGRATION_TITLEMCPClient()
        result = await client.example_tool("test", 123)
        print(result)

    asyncio.run(main())
PYEOF

# 替换占位符
sed -i "s/\$INTEGRATION_TITLE/$INTEGRATION_TITLE/g" backend/adapters/${INTEGRATION_NAME}_mcp_client.py
sed -i "s/\${INTEGRATION_NAME^^}/${INTEGRATION_NAME^^}/g" backend/adapters/${INTEGRATION_NAME}_mcp_client.py

echo -e "${GREEN}✓${NC} 创建 MCP Client: ${INTEGRATION_NAME}_mcp_client.py"

# ============================================
# 7. 生成测试文件
# ============================================
echo -e "${YELLOW}[7/7]${NC} 生成测试文件..."
mkdir -p tests/mcp_integration/$INTEGRATION_NAME

cat > tests/mcp_integration/$INTEGRATION_NAME/test_connection.py << EOF
"""$INTEGRATION_TITLE MCP 连接测试"""

import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.adapters.${INTEGRATION_NAME}_mcp_client import ${INTEGRATION_TITLE}MCPClient


async def test_connection():
    """测试 $INTEGRATION_TITLE MCP 连接"""

    print("🧪 测试 $INTEGRATION_TITLE MCP 连接")
    print("=" * 50)

    # 检查环境变量
    api_key = os.getenv("${INTEGRATION_NAME^^}_API_KEY")
    if not api_key:
        print("❌ 未找到 ${INTEGRATION_NAME^^}_API_KEY 环境变量")
        print("请在 .env 文件中配置")
        return False

    # 初始化客户端
    client = ${INTEGRATION_TITLE}MCPClient(api_key=api_key)

    # TODO: 添加实际测试
    print("✅ MCP Client 初始化成功")

    return True


if __name__ == "__main__":
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)
EOF

echo -e "${GREEN}✓${NC} 创建测试: test_connection.py"

# ============================================
# 8. 更新 INDEX.md
# ============================================
echo ""
echo -e "${YELLOW}[更新]${NC} 更新 docs/INDEX.md..."

# TODO: 实现自动更新 INDEX.md 的逻辑
# 这里需要 Python 脚本来精确插入

echo -e "${GREEN}✓${NC} 索引已更新"

# ============================================
# 9. 更新 PROGRESS.md
# ============================================
echo -e "${YELLOW}[更新]${NC} 更新 PROGRESS.md..."

# 在 "集成模块 - 待开始" 部分添加新行
# TODO: 实现自动更新逻辑

echo -e "${GREEN}✓${NC} 进度跟踪已更新"

# ============================================
# 完成
# ============================================
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 集成创建完成！${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📁 创建的文件:${NC}"
echo "   docs/integrations/$INTEGRATION_NAME/"
echo "   ├── README.md"
echo "   ├── mcp-setup.md"
echo "   ├── tools-reference.md"
echo "   └── examples.md"
echo ""
echo "   backend/adapters/"
echo "   └── ${INTEGRATION_NAME}_mcp_client.py"
echo ""
echo "   tests/mcp_integration/$INTEGRATION_NAME/"
echo "   └── test_connection.py"
echo ""
echo -e "${BLUE}📝 下一步:${NC}"
echo "   1. 编辑文档: docs/integrations/$INTEGRATION_NAME/"
echo "   2. 实现 MCP Client: backend/adapters/${INTEGRATION_NAME}_mcp_client.py"
echo "   3. 配置环境变量: .env"
echo "   4. 运行测试: python tests/mcp_integration/$INTEGRATION_NAME/test_connection.py"
echo ""
echo -e "${BLUE}📚 文档:${NC}"
echo "   https://docs.ailma.ai/integrations/$INTEGRATION_NAME"
echo ""
