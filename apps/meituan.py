"""
美团 应用模块
处理有关业务
"""
from urllib.parse import quote

from pydantic import BaseModel, Field
from typing import Optional, Set
from fastapi import FastAPI, Request, Body
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from components.util import convert_cookies_to_dict, check_jd_ck
from fastapi import Cookie, Response
from components.ql import *
from urllib.parse import quote
from urllib.parse import parse_qs
from fastapi.encoders import jsonable_encoder

mtApp = FastAPI()
ql = qinglong()


class post_data_item(BaseModel):
    remark: Optional[str] = ""
    token: Optional[str] = ""


@mtApp.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"参数不对{request.method} {request.url}")
    return JSONResponse({"code": 0, "msg": exc.errors()})


# 视图函数接收post请求体中的Form表单元素
@mtApp.post('/setToken')
async def set_jd_cookies(request: Request):
    msg = ""
    raw_data = await request.form()
    raw_data = dict(raw_data)
    remark = raw_data.get('meituan_name')
    value = raw_data.get('meituan_secret')
    if remark and value:
        if remark and not remark.startswith("美团-"):
            remark = f"美团-{remark}"
        data = {
            "name": "meituanCookie",
            "remark": remark,
            "status": 0,
            "value": value,
        }
        callback = ql.envs_check_update(data)
        if callback:
            msg = "OK!"
            return {"code": 1, "msg": msg}
        else:
            msg = "处理提交内容时发生错误，联系管理员。"

    return {"code": 0, "msg": msg if msg else "未知错误!"}
