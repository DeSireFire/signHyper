"""
JD 应用模块
处理有关业务
"""
from pydantic import BaseModel, Field
from typing import Optional, Set
from fastapi import FastAPI, Request, Body
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from components.auth import get_ql_auth
jdApp = FastAPI()


class post_data_item(BaseModel):
    remark: Optional[str] = "备注"
    jdCookies: Optional[str] = ""


@jdApp.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"参数不对{request.method} {request.url}")
    return JSONResponse({"code": "400", "message": exc.errors()})


@jdApp.post("/setck")
async def set_jd_cookies(item: post_data_item):
    # 查询所有变量->更新 or 添加
    # 测试更新可不可以直接添加
    print(dict(item))
    return {"status": 0}
