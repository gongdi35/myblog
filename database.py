"""
博客数据库模块 - 使用 Python 内置的 sqlite3
SQLite 是一个文件型数据库，不需要安装任何数据库软件
sqlite3 是 Python 自带的标准库，也不需要 pip 安装

学习要点：
1. 数据库连接和游标
2. SQL 语句的编写（CREATE TABLE, INSERT, SELECT, UPDATE, DELETE）
3. 参数化查询（用 ? 占位符防止 SQL 注入）
4. 上下文管理器（with 语句自动管理资源）
"""

import os
import sqlite3
from datetime import datetime

# 数据库文件路径：放在当前文件（database.py）所在的目录
# 这样不管从哪里运行程序，数据库都会建在正确位置
DB_PATH = os.path.join(os.path.dirname(__file__), "blog.db")


def get_db():
    """
    获取数据库连接
    为什么用函数而不是全局变量？
    因为每个请求应该有自己的连接，避免多用户冲突
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 让查询结果可以用字典方式访问 row['title']
    return conn


def init_db():
    """
    初始化数据库：创建表
    程序启动时调用一次即可
    IF NOT EXISTS 确保不会重复创建
    """
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT    NOT NULL,
                content     TEXT    NOT NULL,
                created_at  TEXT    NOT NULL,
                updated_at  TEXT    NOT NULL
            )
            """
        )
        conn.commit()


# ============================================================
# 以下是 CRUD 操作（增删改查）
# 每个函数做一件事，命名清晰，注释充分
# ============================================================


def create_post(title: str, content: str) -> int:
    """
    创建一篇新文章
    返回新文章的 id
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO posts (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (title, content, now, now),
        )
        conn.commit()
        return cursor.lastrowid


def get_all_posts() -> list[dict]:
    """
    获取所有文章（按创建时间倒序）
    用于首页文章列表
    """
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, title, content, created_at, updated_at FROM posts ORDER BY created_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def get_post_by_id(post_id: int) -> dict | None:
    """
    根据 id 获取单篇文章
    用于文章详情页、编辑页
    找不到时返回 None
    """
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, title, content, created_at, updated_at FROM posts WHERE id = ?",
            (post_id,),
        ).fetchone()
        return dict(row) if row else None


def update_post(post_id: int, title: str, content: str) -> bool:
    """
    更新文章
    返回 True 表示更新成功，False 表示文章不存在
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_db() as conn:
        cursor = conn.execute(
            "UPDATE posts SET title = ?, content = ?, updated_at = ? WHERE id = ?",
            (title, content, now, post_id),
        )
        conn.commit()
        return cursor.rowcount > 0


def delete_post(post_id: int) -> bool:
    """
    删除文章
    返回 True 表示删除成功，False 表示文章不存在
    """
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()
        return cursor.rowcount > 0
