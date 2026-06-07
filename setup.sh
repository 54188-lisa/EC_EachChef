#!/bin/bash
# 完整设置脚本 - 一键完成所有操作

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🍳 EC Each Chef - 一键安装脚本${NC}"
echo "================================"

# 1. 创建项目目录
echo -e "${YELLOW}📁 创建项目目录...${NC}"
mkdir -p EC_EachChef
cd EC_EachChef

# 2. 创建requirements.txt
echo -e "${YELLOW}📝 创建 requirements.txt...${NC}"
cat > requirements.txt << 'EOF'
gradio>=4.0.0
pandas>=2.0.0
EOF

# 3. 克隆你的代码（如果代码在别处）
echo -e "${YELLOW}📥 获取代码...${NC}"
# 方式1：如果代码已在GitHub
if [ ! -f "EC_EachChef_gr.py" ]; then
    git clone https://github.com/54188-lisa/EC_EachChef.git .
fi

# 方式2：如果代码在本地，请手动复制
# cp /path/to/your/EC_EachChef_gr.py .

# 4. 安装依赖
echo -e "${YELLOW}📦 安装依赖...${NC}"
pip3 install -r requirements.txt

# 5. 创建数据目录
mkdir -p recipe_data

# 6. 创建启动脚本
echo -e "${YELLOW}📝 创建启动脚本...${NC}"
cat > start.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 EC_EachChef_gr.py
EOF

chmod +x start.sh

echo -e "${GREEN}✅ 安装完成！${NC}"
echo ""
echo -e "${YELLOW}运行以下命令启动应用：${NC}"
echo "  cd EC_EachChef"
echo "  ./start.sh"
echo ""
echo -e "${YELLOW}或直接运行：${NC}"
echo "  python3 EC_EachChef_gr.py"
