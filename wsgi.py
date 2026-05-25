"""
wsgi.py - PythonAnywhere 部署入口文件

PythonAnywhere 使用 WSGI 协议（一种古老但广泛的 Python Web 服务器接口），
但 FastAPI 是 ASGI 协议（新一代异步接口）。

Mangum 的作用就是充当「适配器/翻译器」：
把 ASGI 应用包装成 WSGI 应用，让 PythonAnywhere 能运行 FastAPI。

PythonAnywhere 会自动找到 application 变量，所以变量名必须叫 application。
"""

from mangum import Mangum
from main import app

# lifespan="off" 禁用 FastAPI 的生命周期管理，
# 改用下面的 database.init_db() 手动初始化
application = Mangum(app, lifespan="off")

# 手动初始化数据库
# PythonAnywhere 在首次导入这个模块时就会执行这段代码
from database import init_db

init_db()
print("✅ 数据库初始化完成！（通过 wsgi.py）")
