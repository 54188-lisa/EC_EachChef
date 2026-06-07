#!/bin/bash
# EC Each Chef - 安装和部署脚本

set -e  # 遇到错误立即退出

echo "🚀 EC Each Chef 安装脚本"
echo "================================"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. 克隆代码（如果需要）
if [ ! -d "EC_EachChef" ]; then
    echo -e "${YELLOW}📥 克隆代码仓库...${NC}"
    git clone https://github.com/54188-lisa/EC_EachChef.git
    cd EC_EachChef
else
    echo -e "${GREEN}✅ 代码已存在${NC}"
    cd EC_EachChef
fi

# 2. 安装依赖
echo -e "${YELLOW}📦 安装Python依赖...${NC}"
pip install -r requirements.txt

# 3. 运行应用
echo -e "${GREEN}✅ 安装完成！${NC}"
echo -e "${YELLOW}🚀 启动应用...${NC}"
python EC_EachChef_gr.py
