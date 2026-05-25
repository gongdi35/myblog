"""
build.py - 静态博客生成器

扫描 posts/ 目录下的 Markdown 文件，生成纯静态 HTML 站点。

用法：
    python build.py           # 构建到 docs/ 目录
    python -m http.server -d docs 8000   # 本地预览

依赖：
    pip install markdown pyyaml jinja2
"""

import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from markdown import markdown
import yaml


BASE_DIR = Path(__file__).resolve().parent
POSTS_DIR = BASE_DIR / "posts"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
OUTPUT_DIR = BASE_DIR / "docs"


def parse_front_matter(text: str) -> tuple[dict, str]:
    """解析 YAML Front Matter：文章头部 `---` 包裹的元数据。"""
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text
    metadata = yaml.safe_load(parts[1]) or {}
    content = parts[2]
    return metadata, content


def build() -> None:
    """构建整个静态站点。"""
    # 1. 清空并重建输出目录
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()
    (OUTPUT_DIR / "post").mkdir()

    # 2. 复制静态文件（CSS）
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, OUTPUT_DIR / "static")

    # 3. 配置 Jinja2 模板引擎
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

    # 4. 遍历所有 Markdown 文章
    post_files = sorted(POSTS_DIR.glob("*.md"), key=lambda f: f.name, reverse=True)
    posts: list[dict] = []

    for md_file in post_files:
        slug = md_file.stem
        text = md_file.read_text(encoding="utf-8")
        meta, md_content = parse_front_matter(text)

        html_content = markdown(
            md_content,
            extensions=["extra"],
        )

        excerpt = meta.get("excerpt", "")
        if not excerpt:
            excerpt = md_content.strip()[:200]
            if len(md_content.strip()) > 200:
                excerpt += "..."

        post = {
            "slug": slug,
            "title": meta.get("title", slug),
            "date": meta.get("date", ""),
            "content": html_content,
            "excerpt": excerpt,
        }
        posts.append(post)

        # 生成文章详情页（base_path=".." 因为详情页在 post/ 子目录下）
        post_template = env.get_template("post.html")
        post_html = post_template.render(post=post, base_path="..")
        out_path = OUTPUT_DIR / "post" / f"{slug}.html"
        out_path.write_text(post_html, encoding="utf-8")

    # 5. 生成首页（base_path="." 因为首页在根目录）
    index_template = env.get_template("index.html")
    index_html = index_template.render(posts=posts, base_path=".")
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    print(f"✅ 构建完成！共 {len(posts)} 篇文章")
    print(f"   输出目录: {OUTPUT_DIR}")
    print(f"   本地预览: python -m http.server -d docs 8000")


if __name__ == "__main__":
    build()
