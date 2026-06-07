#!/bin/bash
# 部署到GitHub的脚本

set -e

echo "📤 部署到 GitHub..."

# 添加所有更改
git add .

# 提交
git commit -m "Update: $(date '+%Y-%m-%d %H:%M:%S')" || echo "没有需要提交的更改"

# 推送到GitHub
git push origin main

echo "✅ 部署完成！"
echo "访问: https://github.com/54188-lisa/EC_EachChef"
