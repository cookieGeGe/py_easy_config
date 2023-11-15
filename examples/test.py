# -*- coding: utf-8 -*-
# @Time    : 2023/6/12-13:40
# @Author  : 灯下客
# @Email   : 
# @File    : test.py
# @Software: PyCharm

from easy_config_py import EasyConfig, Dict

econfig = EasyConfig(path=__file__)
econfig.load_file()
print(econfig)

a = Dict({"b": []})

print(a)
