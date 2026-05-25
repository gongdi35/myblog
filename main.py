"""
博客 FastAPI 主应用
这是整个网站的入口文件，运行它就能启动服务器

学习要点：
1. FastAPI 路由：@app.get("/")、@app.post("/create") 等
2. 模板渲染：用 Jinja2Templates 把数据和 HTML 组合
3. 表单处理：用 Form() 接收用户提交的表单
4. 重定向：用 RedirectResponse 跳转页面
"""

import os
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import database

# ============================================================
# 项目根目录（main.py 所在目录）
# ============================================================
BASE_DIR = Path(__file__).resolve().parent

# ============================================================
# 创建 FastAPI 应用实例
# ============================================================
app = FastAPI(title="我的博客", description="一个简单的个人博客")

# ============================================================
# 配置模板引擎和静态文件
# ============================================================
# 使用绝对路径，确保在任何环境下都能正确找到文件
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# 挂载静态文件目录：让浏览器能访问 CSS 文件
# 使用绝对路径，确保在任何环境下都能正确找到文件
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


# ============================================================
# 启动事件：首次启动时初始化数据库
# ============================================================
@app.on_event("startup")
def startup():
    """应用启动时自动执行，确保数据库表已创建"""
    database.init_db()
    print("✅ 数据库初始化完成！")


# ============================================================
# 路由（页面）
# 每个路由 = 一个网页地址
# ============================================================


@app.get("/")
def index(request: Request):
    """
    首页：显示所有文章列表
    GET /  就是网站的首页
    """
    posts = database.get_all_posts()
    return templates.TemplateResponse(
        "index.html",  # 使用的模板文件
        {"request": request, "posts": posts},  # 传给模板的数据
    )


@app.get("/post/{post_id}")
def view_post(request: Request, post_id: int):
    """
    文章详情页：显示单篇文章的完整内容
    GET /post/1  就显示 id=1 的文章
    """
    post = database.get_post_by_id(post_id)
    if post is None:
        # 文章不存在，重定向到首页
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(
        "post.html",
        {"request": request, "post": post},
    )


@app.get("/create")
def create_page(request: Request):
    """
    写文章页面：显示一个空白表单
    GET /create  就是写新文章的页面
    """
    return templates.TemplateResponse("create.html", {"request": request})


@app.post("/create")
def create_post(
    request: Request,
    title: str = Form(...),  # Form(...) 表示必填，从表单获取数据
    content: str = Form(...),
):
    """
    创建文章：接收表单提交的数据，保存到数据库
    POST /create  处理表单提交
    """
    if title.strip() and content.strip():
        post_id = database.create_post(title.strip(), content.strip())
        return RedirectResponse(url=f"/post/{post_id}", status_code=303)
    # 如果标题或内容为空，返回错误提示
    return templates.TemplateResponse(
        "create.html",
        {"request": request, "error": "标题和内容不能为空！"},
        status_code=400,
    )


@app.get("/edit/{post_id}")
def edit_page(request: Request, post_id: int):
    """
    编辑文章页面：显示已有内容让用户修改
    GET /edit/1  就进入 id=1 文章的编辑页
    """
    post = database.get_post_by_id(post_id)
    if post is None:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(
        "edit.html",
        {"request": request, "post": post},
    )


@app.post("/edit/{post_id}")
def edit_post(
    request: Request,
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
):
    """
    更新文章：接收修改后的表单数据，更新数据库
    POST /edit/1  就更新 id=1 的文章
    """
    if title.strip() and content.strip():
        if database.update_post(post_id, title.strip(), content.strip()):
            return RedirectResponse(url=f"/post/{post_id}", status_code=303)
        return RedirectResponse(url="/", status_code=303)
    post = database.get_post_by_id(post_id)
    return templates.TemplateResponse(
        "edit.html",
        {"request": request, "post": post, "error": "标题和内容不能为空！"},
        status_code=400,
    )


@app.get("/delete/{post_id}")
def delete_post(post_id: int):
    """
    删除文章
    GET /delete/1  就删除 id=1 的文章
    删除后跳转回首页
    """
    database.delete_post(post_id)
    return RedirectResponse(url="/", status_code=303)
