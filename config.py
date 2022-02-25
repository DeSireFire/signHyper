#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2022/2/21
# CreatTIME : 17:27
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
import os
import platform

# 项目路径
base_file_path = os.path.dirname(__file__)

# signHyper 服务地址/端口
host = "127.0.0.1" if platform.system() == 'Windows' else "0.0.0.0"
port = 5701

# 青龙地址
ql_url = "http://127.0.0.1:5700" if platform.system() == 'Windows' else "http://localhost:5700"