"""
JD 应用模块
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

jdApp = FastAPI()
ql = qinglong()


class post_data_item(BaseModel):
    remark: Optional[str] = ""
    jdCookies: Optional[str] = ""


@jdApp.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"参数不对{request.method} {request.url}")
    return JSONResponse({"code": 0, "msg": exc.errors()})

# 视图函数接收post请求体中的Form表单元素
@jdApp.post('/setpt')
async def set_jd_cookies(request: Request):
    msg = ""
    raw_data = await request.form()
    raw_data = dict(raw_data)
    remarks = raw_data.get('jd_name')
    # pt_pin = raw_data.get('pt_pin')
    # pt_key = raw_data.get('pt_key')
    jd_cookie = raw_data.get('jd_cookie')
    if remarks and jd_cookie and "pt_pin" in jd_cookie and "pt_key" in jd_cookie:
        before_name = "京东-"
        if remarks and not remarks.startswith(before_name):
            remarks = f"{before_name}{remarks}"
        # if pt_pin and pt_key:
        #     value = f"pt_pin={pt_pin};pt_key={pt_key};"
        data = {
            "name": "JD_COOKIE",
            "remarks": remarks,
            "status": 0,
            "value": jd_cookie,
        }
        print(f"提交内容：{data}")
        callback = ql.envs_check_update(data)
        if callback:
            msg = "OK!"
            return {"code": 1, "msg": msg}
        else:
            msg = "处理提交内容时发生错误，联系管理员。"
    else:
        # if not pt_pin:
        #     msg += "pt_pin 值不能为空！"
        # if not pt_key:
        #     msg += "pt_key 值不能为空！"
        if not remarks:
            msg += "名称 值不能为空！"
        if not jd_cookie:
            msg += "京东cookie 值不能为空！"
        if "pt_pin" not in jd_cookie:
            msg += "提交的cookie值中没有 pt_pin！无法使用,请自行检查。"
        if "pt_key" not in jd_cookie:
            msg += "提交的cookie值中没有 pt_key！无法使用,请自行检查。"
    return {"code": 0, "msg": msg if msg else "未知错误!"}

# # 视图函数接收post请求体中的Form表单元素
# @jdApp.post('/setck')
# # async def login(request: Request, form_data=Form(...), act=Form(...)):
# async def set_jd_cookies(request: Request):
#     msg = ""
#     raw_data = await request.form()
#     raw_data = jsonable_encoder(raw_data)
#     form_data = parse_qs(raw_data.get("form_data"))
#     remarks = "".join(form_data.get("remarks")[:1]) if form_data.get("remark") else None
#     user_id = "".join(form_data.get("user_id")[:1]) if form_data.get("user_id") else None
#
#     # 检查是否成功接收到数据
#     if not user_id:
#         msg = "发生了剧烈的错误!"
#         return {"code": 0, "msg": msg}
#
#     cookies_dict = parse_qs(user_id.replace(';', '&').replace(' ', ''))
#     cookies_dict = {k: "".join(v[:1]) for k, v in cookies_dict.items() if v}
#
#     # 检查是否为有效的JD ck
#     if check_jd_ck(cookies_dict):
#         unick = cookies_dict.get("unick", remark)
#         # check_jd_ck已经检查了这两个值是否存在
#         pt_key = cookies_dict.get("pt_key", None)
#         pt_pin = cookies_dict.get("pt_pin", None)
#         simple_ck = f"pt_key={pt_key};pt_pin={pt_pin};"
#         ql.envs_create("JD_COOKIE", simple_ck, f"{unick}")
#         msg = "OK!"
#         return {"code": 1, "msg": msg}
#     else:
#         msg = "非合法的京东ck!"
#
#     return {"code": 0, "msg": msg if msg else "未知错误!"}
