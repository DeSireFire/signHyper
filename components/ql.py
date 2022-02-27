#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2022/2/22
# CreatTIME : 10:04 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
import json
import os
import platform
import time
import requests
from config import base_file_path, ql_url
class qinglong(object):
    def __init__(self):
        self.url = ql_url

    @property
    def auth(self):
        """
        获取和刷新青龙面板的登录信息
        :return:
        """
        # 获取auth信息
        # /ql/config/auth.json
        ql_auth_path = os.path.join(base_file_path, "ql", "config", "auth.json")\
            if platform.system() == 'Windows' else '/ql/config/auth.json'
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

    @property
    def ql_headers(self):
        # todo 可用性检查 {"code":401,"message":"jwt malformed"}
        # todo 获取不到tokens会报错！
        token = ""
        if self.auth and isinstance(self.auth.get("tokens"), dict):
            token = self.auth.get("tokens").get("desktop")
        else:
            # todo 日志->为获取到密钥
            pass
        return {
            'accept': 'application/json',
            'content-type': 'application/json;charset=UTF-8',
            'authorization': f'Bearer {token}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7,und;q=0.6,ja;q=0.5',
        }

    def envs_read(self, searchValue=''):
        """
        获取青龙面板的所有环境变量
        :param searchValue: str, 搜索字符串。为空串时，默认返回所有数据
        :return:
        """
        params = {
            'searchValue': searchValue,
            't': str(int(round(time.time() * 1000))),
        }
        response = requests.get(f'{self.url}/api/envs', headers=self.ql_headers, params=params)
        if '"code":200' in response.text:
            datas = json.loads(response.text).get("data")
            return datas
        else:
            # todo 日志 请求失败
            return None

    def envs_update(self, name, value, remarks, id_str):
        """
        更新变量
        :param name: str, 环境变量名称
        :param value: str, 环境变量值
        :param remarks: str, 环境变量的备注
        :param id_str: int, 环境变量索引，用于数据更新
        :return:
        """
        params = {
            't': str(int(round(time.time() * 1000))),
        }
        # 样例 data = {"name":"test888","value":"ohohoh","remarks":"test","id":35}
        data = {"name": f"{name}", "value": f"{value}", "id": int(id_str)}
        if remarks:
            data["remarks"] = f"{remarks}"
        response = requests.put(f'{self.url}/api/envs', headers=self.ql_headers, params=params, data=json.dumps(data))
        print(f"envs_update-->{response.text}")
        if '"code":200' in response.text:
            datas = json.loads(response.text).get("data")
            return datas
        else:
            # todo 日志 请求失败
            return None

    def envs_create(self, name, value, remarks):
        """
        添加变量
        :param name: str, 环境变量名称
        :param value: str, 环境变量值
        :param remarks: str, 环境变量的备注
        :return:
        """
        params = {
            't': str(int(round(time.time() * 1000))),
        }
        datas = []
        # data = '[{"name":"test777","value":"test888","remarks":"90909"}]'
        # data = json.dumps([{"name":f"{name}","value":"test888","remarks":"90909"}])
        data = {"name": f"{name}", "value": f"{value}"}
        if remarks:
            data["remarks"] = f"{remarks}"
        datas.append(data)
        response = requests.post(f'{self.url}/api/envs', headers=self.ql_headers, params=params, data=json.dumps(datas))
        print(response.text)
        if '"code":200' in response.text:
            datas = json.loads(response.text).get("data")
            return datas
        else:
            # todo 日志 请求失败
            return None

    def envs_del(self, ids):
        """
        删除变量
        :param ids: list, 需要删除的环境变量id列表
        :return:
        """
        params = {
            't': str(int(round(time.time() * 1000))),
        }
        # data = '[36]'
        data = json.dumps(ids)

        response = requests.delete(f'{self.url}/api/envs', headers=self.ql_headers, params=params, data=data)
        print(response.text)
        if '"code":200' in response.text:
            datas = json.loads(response.text).get("data")
            return datas
        else:
            # todo 日志 请求失败
            return None

if __name__ == '__main__':
    cls = qinglong()
    # print(cls.get_ql_auth())
    # 增删改查
    c = cls.envs_create("demo", "demo", "demo")
    # d = cls.envs_del("36")
    # u = cls.envs_update("demo", "demo", "demo", "35")
    # r = cls.envs_read("DeSireFire")
