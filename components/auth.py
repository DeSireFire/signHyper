#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2022/2/21
# CreatTIME : 17:30 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import json
import os
import platform


def get_ql_auth():
    """
    获取青龙面板的登录信息
    :return:
    """
    # 获取auth信息
    # /ql/config/auth.json
    ql_auth_path = "ql/config/auth.json" if platform.system() == 'Windows' else '/ql/config/auth.json'
    auth_json = {}
    if os.path.exists(ql_auth_path):
        with open(ql_auth_path, "r", encoding="utf8") as f:
            try:
                auth_json_str = f.read()
                auth_json = json.loads(auth_json_str) if auth_json_str else {}
                print(auth_json)
            except Exception as e:
                print(f"{[auth_json]} --> 错误:{e}")
    return auth_json