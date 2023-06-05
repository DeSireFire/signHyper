import os
import platform
from typing import Optional, Set
from fastapi import Form
import uvicorn
from fastapi import FastAPI, Request, Response
from config import host, port
from urllib.parse import quote
from urllib.parse import parse_qs
import http.cookies
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 读取子模块
# app.mount(f"/api/jdApp", jdApp)
# 读取
auth_json = {}

def parse_cookies(cookies_str):
    cookies = http.cookies.SimpleCookie()
    cookies.load(cookies_str)
    return {key: morsel.value for key, morsel in cookies.items()}

def check_jd_ck(cookies_dict:dict):
    temp = {}
    for k, v in cookies_dict.items():
        if k.starwith("pt_"):
            temp[k] = v

    if temp.get("pt_key") and temp.get("pt_pin"):
        return True
    else:
        return False

# 视图函数接收post请求体中的Form表单元素
@app.post('/sign')
# async def login(request: Request, form_data=Form(...), act=Form(...)):
async def login(request: Request):
    raw_data = await request.form()
    raw_data = jsonable_encoder(raw_data)
    form_data = parse_qs(raw_data.get("form_data"))
    remark = "".join(form_data.get("remark")[:1]) if form_data.get("remark") else None
    user_id = "".join(form_data.get("user_id")[:1]) if form_data.get("user_id") else None

    # 检查是否成功接收到数据
    if not user_id:
        return {"code": 0, "msg": "发生了剧烈的错误!"}

    cookies_dict = parse_qs(user_id.replace(';', '&').replace(' ', ''))

    # 检查是否为有效的ck
    if check_jd_ck(cookies_dict):
        print(cookies_dict)
        return {"code": 1, "msg": "OK"}

    return {"code": 0, "msg": "未知错误!"}



def run_uvicorn(HOST=host, PORT=int(port)):
    uvicorn.run(
        app="server:app",
        host=HOST, port=PORT,
        reload=True)


if __name__ == '__main__':
    run_uvicorn()
