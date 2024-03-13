import os
import platform
from typing import Optional, Set
from fastapi import Form
import uvicorn
from fastapi import FastAPI, Request, Response
from config import host, port
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
from apps.jd import jdApp
from apps.meituan import mtApp
# app.mount(f"/api/jdApp", jdApp)
app.mount(f"/api/meituan", mtApp) # /api/meituan/setToken
# 读取
auth_json = {}


def run_uvicorn(HOST=host, PORT=int(port)):
    uvicorn.run(
        app="server:app",
        host=HOST, port=PORT,
        reload=True)


if __name__ == '__main__':
    run_uvicorn()
