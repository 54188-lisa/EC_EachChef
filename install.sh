#!/bin/bash
# 安装脚本 - 首次运行使用

set -e

echo "🍳 EC Each Chef - 安装脚本"
echo "================================"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

# 克隆仓库
echo "📥 克隆仓库..."
git clone https://github.com/54188-lisa/EC_EachChef.git
cd EC_EachChef

# 安装依赖
echo "📦 安装依赖..."
pip3 install -r requirements.txt

echo "✅ 安装完成！"
echo "运行 ./run.sh 启动应用"
