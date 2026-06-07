git clone https://gitee.com/sisu-aidc/pangxuanning.git
cd EC_EachChef_gr.py
pip install -r requirements.txt
python EC_EachChef_gr.py

#!/bin/bash
# 设置脚本 - 用于Hugging Face Spaces部署

pip install -r requirements.txt

# 进入项目目录
cd /path/to/EC_EachChef_gr.py

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: EC Each Chef 智能菜谱助手"

# 添加远程仓库
git remote add origin https://github.com/54188-lisa/EC_EachChef.git

# 推送到GitHub
git branch -M main
git push -u origin main

# 1. 创建项目文件夹
mkdir EC_EachChef
cd EC_EachChef

# 2. 复制你的EC_EachChef.py到当前目录

# 3. 创建requirements.txt
echo "gradio>=4.0.0
pandas>=2.0.0" > requirements.txt

# 4. 创建README.md（使用上面的内容）

# 5. 创建.gitignore（使用上面的内容）

# 6. 初始化Git
git init
git add .
git commit -m "First commit"

# 7. 连接GitHub仓库
git remote add origin https://github.com/54188-lisa/EC_EachChef.git
git push -u origin main

# 修改代码后，提交更新
git add EC_EachChef_gr.py
git commit -m "Update: 修复bug或添加新功能"
git push
