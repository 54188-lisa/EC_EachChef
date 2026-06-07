#!/bin/bash
# 启动脚本

cd "$(dirname "$0")"

echo "🚀 启动 EC Each Chef..."
echo "访问地址: http://localhost:7860"

python3 EC_EachChef_gr.py
