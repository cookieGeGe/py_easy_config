# -*- coding: utf-8 -*-
# @Time    : 2023/6/12-11:40
# @Author  : 灯下客
# @Email   : 
# @File    : config.py
# @Software: PyCharm
import os.path
import asyncio
from functools import partial

import anyconfig

from easy_config_py import Dict
from easy_config_py import FileLoader


class EasyConfig(object):

    def __init__(self, data=None, path=None, default_filename='config.yml'):
        self._data = Dict(data)
        if path is not None and os.path.isfile(path):
            path = os.path.dirname(path)
        if path is None:
            path = os.path.dirname(__file__)
        self.path = path
        self._loader = FileLoader(path, default_filename)

    def __getattr__(self, item):
        return self._data.get(item)
    
    def getattr(self, key, default=None):
        """
        通过字符串键名获取配置值，支持包含特殊字符的键名。
        
        这个方法可以访问包含特殊字符（如 '-'）或 Python 关键字的键名。
        支持点号分隔的嵌套路径访问。
        
        Args:
            key: 键名（字符串），支持点号分隔的嵌套路径，如 'database.host-name'
            default: 如果键不存在时返回的默认值
        
        Returns:
            对应的配置值，如果键不存在返回 default
        
        示例:
            >>> config = EasyConfig()
            >>> config.load_by_content("key-with-dash: value")
            >>> config.getattr('key-with-dash')  # 'value'
            >>> config.getattr('nested.sub-key', 'default')  # 访问嵌套键
        """
        return self._data.getattr(key, default)
    
    def setattr(self, key, value):
        """
        通过字符串键名设置配置值，支持包含特殊字符的键名和嵌套路径。
        
        Args:
            key: 键名（字符串），支持点号分隔的嵌套路径
            value: 要设置的值
        
        示例:
            >>> config = EasyConfig()
            >>> config.setattr('key-with-dash', 'value')
            >>> config.setattr('nested.sub-key', 123)
            >>> config.getattr('key-with-dash')  # 'value'
        """
        self._data.setattr(key, value)

    @property
    def data(self):
        return self._data

    def to_dict(self):
        return self._data.to_dict()

    def update(self, *args, **kwargs):
        self._data.update(*args, **kwargs)

    def load_file(self, path=None):
        config = self._loader.get_file(path, anyconfig.load)
        self._data.update(config)

    def load_by_content(self, content, parser_type='yml'):
        parser_type_lower = parser_type.lower()
        extension = "yaml" if parser_type_lower == "yml" else parser_type_lower
        support_ext = anyconfig.list_types()
        if extension not in support_ext:
            raise ValueError(
                f"Unsupported file format '{extension}'. "
                f"Currently supported formats: {', '.join(support_ext)}"
            )
        config_dict = anyconfig.loads(content, ac_parser=extension)
        self._data.update(config_dict)

    async def async_load_file(self, path=None):
        """异步加载配置文件"""
        config = await self._loader.async_get_file(path, anyconfig.load)
        self._data.update(config)

    async def async_load_by_content(self, content, parser_type='yml'):
        """异步从内容加载配置"""
        parser_type_lower = parser_type.lower()
        extension = "yaml" if parser_type_lower == "yml" else parser_type_lower
        support_ext = anyconfig.list_types()
        if extension not in support_ext:
            raise ValueError(
                f"Unsupported file format '{extension}'. "
                f"Currently supported formats: {', '.join(support_ext)}"
            )
        # anyconfig.loads 是同步的，在线程池中运行
        # 使用 partial 来传递关键字参数
        load_func = partial(anyconfig.loads, content, ac_parser=extension)
        try:
            # Python 3.9+ 使用 to_thread
            config_dict = await asyncio.to_thread(load_func)
        except AttributeError:
            # Python 3.7-3.8 使用 run_in_executor
            loop = asyncio.get_event_loop()
            config_dict = await loop.run_in_executor(None, load_func)
        self._data.update(config_dict)
