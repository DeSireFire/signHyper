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
from config import ql_url


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
        auth_json = {}
        raw = requests.get("http://10.0.0.3:2180/config/auth.json")
        # raw = requests.get(url="https://ani.lovewx.club:25100/config/auth.json", verify=False)
        assert raw.status_code == 200, '获取青龙面板密钥文件时失败！'
        if raw.json():
            auth_json = raw.json()
        assert auth_json, '获取青龙面板密钥为空！不能正常使用！'
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

    def envs_update_old(self, name, value, remarks, id_str):
        """
        更新变量
        :param name: str, 环境变量名称
        :param value: str, 环境变量值
        :param remarks: str, 环境变量的备注
        :param id_str: str, 环境变量索引，用于数据更新
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

    def envs_update(self, id_str, **kwargs):
        """
        更新变量
        :param id_str: str, 环境变量索引，用于数据更新
        kwargs ↓
        :param name: str, 环境变量名称
        :param value: str, 环境变量值
        :param remarks: str, 环境变量的备注
        :return:
        """
        params = {
            't': str(int(round(time.time() * 1000))),
        }
        # 样例 data = {"name":"test888","value":"ohohoh","remarks":"test","id":35}
        # data = {"name": f"{name}", "value": f"{value}", "id": int(id_str)}
        data = {}
        data.update(kwargs)
        data["id"] = int(id_str)
        item = {k: v for k, v in data.items() if v}
        response = requests.put(f'{self.url}/api/envs', headers=self.ql_headers, params=params, data=json.dumps(item))
        print(f"envs_update-->{response.text}")
        if '"code":200' in response.text:
            datas = json.loads(response.text).get("data")
            return datas
        else:
            # todo 日志 请求失败
            return None

    def envs_create_old(self, name, value, remarks):
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

    def envs_create(self, **kwargs):
        """
        添加变量 kwargs ↓
        :param name: str, 环境变量名称
        :param value: str, 环境变量值
        :param remarks: str, 环境变量的备注
        :return:
        """
        params = {
            't': str(int(round(time.time() * 1000))),
        }
        items = []
        # data = '[{"name":"test777","value":"test888","remarks":"90909"}]'
        # data = json.dumps([{"name":f"{name}","value":"test888","remarks":"90909"}])
        data = {}
        data.update(kwargs)
        item = {k: v for k, v in data.items() if v}
        items.append(item)
        response = requests.post(f'{self.url}/api/envs', headers=self.ql_headers, params=params, data=json.dumps(items))
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
        data = f'[{",".join(ids)}]'

        response = requests.delete(f'{self.url}/api/envs', headers=self.ql_headers, params=params, data=data)
        print(response.text)
        if '"code":200' in response.text:
            datas = json.loads(response.text).get("data")
            return datas
        else:
            # todo 日志 请求失败
            return None

    def envs_enable(self, ids):
        """
        启用变量
        :param ids: list, 需要启用的环境变量id列表
        :return:
        """
        params = {
            't': str(int(round(time.time() * 1000))),
        }
        data = f'[{",".join(ids)}]'

        response = requests.put(f'{self.url}/api/envs', headers=self.ql_headers, params=params, data=data)
        print(response.text)
        if '"code":200' in response.text:
            datas = json.loads(response.text).get("data")
            return datas
        else:
            # todo 日志 请求失败
            return None

    def envs_check_update(self, update_value):
        """
        获取青龙面板的所有环境变量
        :param update_value: dict,需要查找并更新的数据
        :return:
        """
        item = {}
        #  如果存在id直接使用id更新
        if "id" in update_value:
            item = update_value
            callback = self.envs_update(update_value.get('id'), **item)
            return callback

        # 如果没有id,则通过name字段和remarks的完全匹配
        if "id" not in update_value:
            envs_list = self.envs_read('') or []
            name = update_value.get("name") or None
            remarks = update_value.get("remarks") or None
            temp = {}
            for i in envs_list:
                if i.get("name") == name and i.get("remarks") == remarks:
                    temp.update(i)
                    break
            if temp:
                temp.update(update_value)
                key_list = ["id", "name", "remarks", "value", "status"]
                item = {k: v.strip() if isinstance(v, str) else v for k, v in temp.items() if k in key_list}
                callback = self.envs_update(item.get('id'), **item)
                return callback

        # todo 完全没找到匹配项的则新建
        if not item and "name" in update_value and "value" in update_value:
            item = update_value
            callback = self.envs_create(**item)
            return callback

        if not item:
            print(f"{update_value} 该数据不规范，提交失败")
            return None

        print(f"{update_value} 该数据提交失败，原因未知。")
        return None


if __name__ == '__main__':
    print(__name__)
    # cls = qinglong()
    # print(cls.auth)
    # print(cls.ql_headers)
    # 增删改查
    # c = cls.envs_create("demo", "demo", "demo")
    # d = cls.envs_del("28")
    # u = cls.envs_update("demo", "demo", "demo666", "28")
    # r = cls.envs_read("JD")
