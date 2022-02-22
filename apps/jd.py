"""
JD 应用模块
处理有关业务
"""
from pydantic import BaseModel, Field
from typing import Optional, Set
from fastapi import FastAPI, Request, Body
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from components.util import convert_cookies_to_dict

from components.ql import *
jdApp = FastAPI()
ql = qinglong()

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
    remark = dict(item).get("remark") or {}
    jdCookies = dict(item).get("jdCookies") or {}
    temp_cookies = convert_cookies_to_dict(jdCookies)
    pt_key = temp_cookies.get("pt_key")
    pt_pin = temp_cookies.get("pt_pin")
    datas = []
    print(temp_cookies)
    res = None
    if pt_key and pt_pin:
        # 搜索变量
        datas = ql.envs_read(pt_pin) or []
        # 有结果只取第一个
        if datas:
            d_id = datas[0].get("id")
            res = await ql.envs_update("JD_COOKIE", f"pt_key={pt_key};pt_pin={pt_pin};", f"{remark}", id_str=d_id)
            print(f"JD_COOKIE--->{res}")
        else:   # 没到说明是新变量
            res = await ql.envs_create("JD_COOKIE", f"pt_key={pt_key};pt_pin={pt_pin};", f"{remark}")
            print(f"JD_COOKIE3--->{res}")
        return {"status": 1}
    return {"status": 0}