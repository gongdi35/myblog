#!/bin/bash
# ============================================================================
# 博客一键部署脚本 - 在 PythonAnywhere Bash 终端中运行
#
# 使用方法：
#   在 PythonAnywhere Bash 终端中执行：
#      bash <(curl -s https://raw.githubusercontent.com/gongdi35/myblog/main/deploy_pa.sh)
# ============================================================================

REPO="git@github.com:gongdi35/myblog.git"
PROJECT_DIR="$HOME/blog"
PA_USERNAME="kevin1q88"

echo "============================================"
echo "  🚀 博客一键部署 - PythonAnywhere"
echo "============================================"
echo ""

# ---- 第一步：克隆代码 ----
echo "📦 第一步：克隆代码..."
if [ -d "$PROJECT_DIR" ]; then
    echo "  目录已存在，执行 git pull 更新..."
    cd "$PROJECT_DIR" && git pull
else
    git clone "$REPO" "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi
echo "  ✅ 代码已就绪"
echo ""

# ---- 第二步：安装依赖 ----
echo "📦 第二步：安装 Python 依赖..."
pip install --user -r "$PROJECT_DIR/requirements.txt"
echo "  ✅ 依赖安装完成"
echo ""

# ---- 第三步：输出 WSGI 配置 ----
USERNAME=$(whoami)
echo "============================================"
echo "  ⚠️  还需要手动完成以下步骤："
echo "============================================"
echo ""
echo "📌 第三步：配置 Web 应用"
echo "  1. 点击顶部「Web」标签"
echo "  2. 点击「Add a new web app」"
echo "  3. 域名确认 → Next"
echo "  4. 选择「Manual configuration」"
echo "  5. Python 版本选 3.10+ → Next"
echo ""
echo "📌 第四步：编辑 WSGI 配置文件"
echo "  点击 WGSI configuration file 链接，"
echo "  删除全部内容，替换为："
echo ""
echo "  ┌────────────────────────────────────────┐"
echo "  │ import sys                             │"
echo "  │                                         │"
echo "  │ project_home = '/home/$USERNAME/blog'"
echo "  │ if project_home not in sys.path:        │"
echo "  │     sys.path.insert(0, project_home)    │"
echo "  │                                         │"
echo "  │ from wsgi import application            │"
echo "  └────────────────────────────────────────┘"
echo ""
echo "📌 第五步：配置静态文件"
echo "  在 Static files 部分添加："
echo "  URL: /static/"
echo "  Directory: /home/$USERNAME/blog/static/"
echo ""
echo "📌 第六步：点击绿色「Reload」按钮"
echo ""
echo "============================================"
echo "  🎉 部署完成！访问："
echo "  https://${USERNAME}.pythonanywhere.com"
echo "============================================"
