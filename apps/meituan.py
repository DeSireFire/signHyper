"""
美团 应用模块
处理有关业务
"""
from pprint import pprint
from urllib.parse import quote

from pydantic import BaseModel, Field
from typing import Optional, Set
from fastapi import FastAPI, Request, Body
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from components.util import convert_cookies_to_dict, check_jd_ck, parse_logs, desensitize_phone_numbers
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
    remarks = raw_data.get('meituan_name')
    value = raw_data.get('meituan_secret')

    # http://meishi.meituan.com/i/?ci=290&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1&userId=71319945&token=AgH0JbBVm3C8JaLNEvUgD_nPqY_0ezYwjXyPbO7ZkGdCU6gSxqicxB9kNtwu9LnZgZOJqZWGcO4G8QAAAAC1HgAAlzApDjpsgxXF1ymIOivmXsXHBhfu1sGN5zTOUvjAfv2Sh8v8a0073jHPtJjI0gbJ
    if value and "http://meishi.meituan.com" in value:
        value = value.split("token=")[1:] or []
        value = "".join(value) or None
        value = value if "http" not in value else ""

    if remarks and value:
        if remarks and not remarks.startswith("美团-"):
            remarks = f"美团-{remarks}"
        data = {
            "name": "meituanCookie",
            "remarks": remarks,
            "status": 0,
            "value": value,
        }
        # print(f"提交内容：{data}")
        callback = ql.envs_check_update(data)
        if callback:
            msg = "OK!"
            return {"code": 1, "msg": msg}
        else:
            msg = "处理提交内容时发生错误，联系管理员。"

    return {"code": 0, "msg": msg if msg else "未知错误!"}


# 获取美团运行情况
@mtApp.get('/mtLogAll')
async def mt_log_all(request: Request):
    msg = ""

    # 美团脚本的job_id
    tasks = ql.crons_search("meituan")
    first_item_id = tasks['data'][0]['id'] if tasks else None
    if not first_item_id:
        msg = "获取指定任务id失败！无法查询..."
        return {"code": 0, "msg": msg if msg else "未知错误!"}

    # 获取指定id的日志,切割
    log_text = ql.job_log_read(first_item_id)
    logs, start_time = parse_logs(log_text)
    print(f"日志开始执行时间：{start_time}")
    for index, account_log in enumerate(logs, start=1):
        print(f"-------- 账号[{index}] --------")
        # print(account_log)

    # 获取所有美团脚本相关的变量
    mt_users = ql.envs_read("meituanCookie")
    print(f"用户列表...")
    for n, m in enumerate(mt_users, start=1):
        print(f"{n}:{m.get('remarks')}")

    # 格式化日志以及对应用户关系
    res_data = {}
    if logs and mt_users:
        for u, l in zip(mt_users, logs):
            if u["remarks"] not in res_data:
                res_data[u["remarks"]] = {}
                for k in ["id", 'remarks', 'name', 'status']:
                    res_data[u["remarks"]][k] = u[k]
                tl = desensitize_phone_numbers(l)
                tls = tl.split("\n") or [""]
                nl = "\n".join(tls[1:]).strip()
                res_data[u["remarks"]]["log_info"] = nl

    if res_data:
        msg = "OK!"
        return {"code": 1, "msg": msg, "datas": res_data}
    else:
        msg = "处理提交内容时发生错误，联系管理员。"

    return {"code": 0, "msg": msg if msg else "未知错误!"}


# 获取美团运行情况
@mtApp.get('/mtLog')
async def mt_log(request: Request, remarks: str):
    msg = ""
    print(f"接口路径:/mtLog. remarks:{remarks}")
    if remarks:
        remarks = remarks.strip()
    if remarks and not remarks.startswith("美团-"):
        remarks = f"美团-{remarks}"
    # 美团脚本的job_id
    tasks = ql.crons_search("meituan")
    first_item_id = tasks['data'][0]['id'] if tasks else None
    if not first_item_id:
        msg = "获取指定任务id失败！无法查询..."
        return {"code": 0, "msg": msg if msg else "未知错误!"}

    # 获取指定id的日志,切割
    log_text = ql.job_log_read(first_item_id)
    logs, start_time = parse_logs(log_text)

    # 获取所有美团脚本相关的变量
    mt_users = ql.envs_read("meituanCookie")

    # 格式化日志以及对应用户关系
    res_data = {}
    if logs and mt_users:
        for u, l in zip(mt_users, logs):
            if u["remarks"] not in res_data:
                res_data[u["remarks"]] = {}
                for k in ["id", 'remarks', 'name', 'status']:
                    res_data[u["remarks"]][k] = u[k]
                tl = desensitize_phone_numbers(l)
                tls = tl.split("\n") or [""]
                nl = "\n".join(tls[1:]).strip()
                res_data[u["remarks"]]["log_info"] = nl

    if res_data:

        for n in res_data.keys():
            print(f"名称：{n}")

        mt_user_log = res_data.get(remarks)
        msg = "OK!"
        return {"code": 1, "msg": msg, "datas": mt_user_log}
    else:
        msg = "处理提交内容时发生错误，联系管理员。"
    return {"code": 0, "msg": msg if msg else "未知错误!"}
