# 🚀 博客部署到 PythonAnywhere 教程

## 为什么不能用 GitHub Pages？

GitHub Pages 只能托管**静态文件**（HTML / CSS / JS），没有后端、没有数据库。
你的博客是**动态网站**——有 FastAPI 做后端、有 SQLite 存数据——所以必须用能跑 Python 的主机。

PythonAnywhere 是免费、最友好的 Python 托管平台，完美适合你的博客。

---

## 📋 部署步骤（约 10 分钟）

### 第一步：注册 PythonAnywhere

1. 打开 https://www.pythonanywhere.com/
2. 点击右上角 **「Pricing & signup」**
3. 选择 **「Beginner」（免费版）**
4. 填写用户名、邮箱、密码，注册
5. 免费版域名是 `你的用户名.pythonanywhere.com`

---

### 第二步：上传代码到 PythonAnywhere

注册登录后，你会看到顶部的控制台面板 **「Consoles」**。

#### 方法一：用 Bash 终端 + Git（推荐）

1. 点击顶部 **「Consoles」** 标签
2. 点击 **「Bash」** 打开一个在线终端
3. 在终端中执行：

```bash
# 先把代码推送到 GitHub，然后克隆到 PythonAnywhere
git clone https://github.com/你的用户名/你的仓库名.git
```

> 如果还没有 GitHub 仓库，先看下面的"方法二"上传。

#### 方法二：通过网页直接上传文件

1. 点击顶部 **「Files」** 标签
2. 在左侧目录树中，进入 `/home/你的用户名/`
3. 点击 **「New directory」**，输入 `blog`，创建项目目录
4. 点击进入 `blog/` 目录
5. 再创建 `templates/` 和 `static/` 两个文件夹
6. 逐个点击 **「Upload a file」**，把本地的所有文件上传到对应位置

**最终目录结构应该是：**
```
/home/你的用户名/blog/
├── wsgi.py            ← PythonAnywhere 会自动找到这个
├── main.py
├── database.py
├── requirements.txt
├── blog.db            ← 上传本地已有的也行，不上传也会自动创建
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── index.html
    ├── post.html
    ├── create.html
    └── edit.html
```

---

### 第三步：安装依赖

回到 **「Bash」** 终端，执行：

```bash
pip install --user mangum fastapi uvicorn jinja2 python-multipart
```

> `--user` 表示安装到用户目录，免费版必须加这个参数。

或者进入项目目录后从 requirements.txt 安装：

```bash
cd ~/blog
pip install --user -r requirements.txt
```

验证安装：
```bash
python -c "import mangum; print('OK')"
# 输出 OK 就成功了
```

---

### 第四步：配置 Web 应用

1. 点击顶部 **「Web」** 标签
2. 点击蓝色按钮 **「Add a new web app」**
3. 域名确认 → 点 **「Next」**
4. 选择框架：**「Manual configuration」**（不要选 Python Web 框架！）
5. Python 版本：选 **Python 3.10** 或更新版本
6. 点 **「Next」** 完成创建

---

### 第五步：编辑 WSGI 配置文件

在 Web 页面找到 **「Code」** 部分：

1. 点击 `WGSI configuration file` 后面的蓝色链接
   （类似 `/var/www/你的用户名_pythonanywhere_com_wsgi.py`）
2. **删除文件里的全部内容**，替换成：

```python
import sys

# 告诉 Python 去哪里找你的代码
project_home = '/home/你的用户名/blog'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# 导入 wsgi.py 模块，从中获取 application 变量
from wsgi import application
```

> ⚠️ 把 `你的用户名` 替换成你注册时填的用户名！

3. 点击 **「Save」**（绿色按钮）

---

### 第六步：设置静态文件

在 Web 页面找到 **「Static files」** 部分，添加一条规则：

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/你的用户名/blog/static/` |

> 这相当于告诉 PythonAnywhere：「凡是以 /static/ 开头的 URL，直接从 static/ 目录取文件」，和本地的 `app.mount("/static", ...)` 作用一样。

---

### 第七步：启动！

1. 回到 **「Web」** 页面顶部
2. 点击绿色按钮 **「Reload 你的用户名.pythonanywhere.com」**
3. 点击域名链接 `你的用户名.pythonanywhere.com` 打开你的博客！

---

## 🔄 更新代码

以后修改了代码，只需：

1. 上传新文件（覆盖旧文件），或用 `git pull` 拉取
2. 在 **「Web」** 页面点击 **「Reload」**

---

## ❓ 常见问题

### 网站打不开 / 显示错误页面

在 Web 页面查看 **「Error log」**，找到最近的错误信息。常见原因：
- 文件名/路径写错了
- 忘记 `pip install --user` 安装依赖
- wsgi 配置文件里的用户名没改
- /static/ 目录路径写错了

### 免费版有什么限制？

- CPU/带宽有限（个人博客完全够）
- **每 3 个月需要手动续期一次**（会发邮件提醒，点击一下就行）
- 不能运行长时间后台任务
- 必须用 `pip install --user`

### 本地还能继续用 `uvicorn main:app` 吗？

可以！`wsgi.py` 是专门给 PythonAnywhere 用的，本地开发完全不受影响：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 🎯 总结

```
你的电脑（开发）               PythonAnywhere（生产/公网）
┌──────────────┐              ┌─────────────────────────┐
│ uvicorn      │              │ WSGI Server             │
│ main:app     │              │ wsgi.py → Mangum        │
│ (ASGI) ──────│──── 上传 ────│→ main:app (ASGI)        │
│ SQLite       │              │   → SQLite              │
│ blog.db      │              │   → blog.db             │
│ localhost:8000│             │ yourname.pythonanywhere.com│
└──────────────┘              └─────────────────────────┘
```

核心思想：`Mangum` 就像一个电源转接头，让 PythonAnywhere 的 WSGI 接口能驱动你的 FastAPI（ASGI）应用。
