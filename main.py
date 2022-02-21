import os
import platform

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from apps.jd import jdApp

app = FastAPI()
# 创建一个templates（模板）对象，以后可以重用。
templates = Jinja2Templates(directory="./templates")
# 读取静态文件
app.mount("/static", StaticFiles(directory="./static"), name="static")
# 读取子模块
app.mount(f"/api/jdApp", jdApp)
# 读取
auth_json = {}

# Request在路径操作中声明一个参数，该参数将返回模板。
# 使用templates您创建的渲染并返回TemplateResponse，并request在Jinja2“上下文” 中将用作键值对之一。
@app.get("/items/{id}")
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

@app.get("/test")
async def read_root(request: Request):
    return templates.TemplateResponse(f"index.html", {"request": request})

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(f"base_user.html", {"request": request})

# @app.get("/favicon.ico")
# async def favicon(request: Request):
#     return templates.TemplateResponse(f"base_index.html", {"request": request})

@app.get("/{path}")
async def fe_path(request: Request, path: str):
    return templates.TemplateResponse(f"base_{path}.html", {"request": request})


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}

def run_uvicorn(host="127.0.0.1", port=int(5360)):
    uvicorn.run(
        app="main:app",
        host=host, port=port,
        reload=True)

if __name__ == '__main__':
    run_uvicorn()