import os
import platform
from typing import Optional, Set
import uvicorn
from fastapi import FastAPI, Request, Response
from config import host, port
from urllib.parse import quote

app = FastAPI()
# 读取子模块
# app.mount(f"/api/jdApp", jdApp)
# 读取
auth_json = {}

# # Request在路径操作中声明一个参数，该参数将返回模板。
# # 使用templates您创建的渲染并返回TemplateResponse，并request在Jinja2“上下文” 中将用作键值对之一。
# @app.get("/items/{id}")
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})
#
# @app.get("/test")
# async def read_root(request: Request):
#     return templates.TemplateResponse(f"index.html", {"request": request})
#
# @app.get("/")
# async def read_root(request: Request, response: Response):
#     return templates.TemplateResponse(f"base_user.html", {"request": request})
#
# @app.get("/{path}")
# async def fe_path(request: Request, response: Response, path: str):
#     filePath = 'templates'
#     templates_files = os.listdir(filePath)
#
#     TR_html = f"base_{path}.html" if f"base_{path}.html" in templates_files else f"base_user.html"
#     return templates.TemplateResponse(TR_html, {"request": request})

@app.get("/cookies/{ck}")
async def cookie_test(response: Response, ck: Optional[str] = None):
    text = quote(f'{ck}', 'utf-8')
    response.set_cookie(key="jd-user", value=text)
    return {"ck": ck}

def run_uvicorn(HOST=host, PORT=int(port)):
    uvicorn.run(
        app="main:app",
        host=HOST, port=PORT,
        reload=True)

if __name__ == '__main__':
    run_uvicorn()