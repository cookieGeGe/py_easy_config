# -*- coding: utf-8 -*-
# @Time    : 2023/6/12-11:39
# @Author  : 灯下客
# @Email   : 
# @File    : file_loader.py
# @Software: PyCharm
import os
import asyncio

# 模块级文件缓存，键为文件路径，值为文件内容或解析后的配置
_files_cached = {}


class FileLoader(object):
    default_file = None
    path = None

    def __init__(self, path, default_filename):
        self.path = path
        self.default_file = default_filename

    def get_file(self, path=None, parse_func=None):
        if path is None:
            path = self.path
        if os.path.isdir(path):
            path = os.path.join(path, self.default_file)
        return self._get_conf_from_file(path, parse_func)

    def put_file(self, path, content, mode="w"):
        """同步写入文件"""
        with open(path, mode) as file_to_write:
            file_to_write.write(content)

    def _get_conf_from_file(self, path, parse_func=None):
        if path and os.path.isdir(path):
            path = os.path.join(path, self.default_file)

        if not path or not os.path.isfile(path):
            return {}
        if path not in _files_cached:
            self.path = path
            if parse_func:
                _files_cached[path] = parse_func(path)
            else:
                with open(path, "rb") as file_to_read:
                    content = file_to_read.read()
                _files_cached[path] = content
        return _files_cached[path]

    async def async_get_file(self, path=None, parse_func=None):
        """异步获取文件内容"""
        if path is None:
            path = self.path
        if os.path.isdir(path):
            path = os.path.join(path, self.default_file)
        return await self._async_get_conf_from_file(path, parse_func)

    async def async_put_file(self, path, content, mode="w"):
        """异步写入文件"""
        try:
            import aiofiles
            async with aiofiles.open(path, mode) as file_to_write:
                await file_to_write.write(content)
        except ImportError:
            # 如果没有安装 aiofiles，回退到同步方式（在线程池中运行）
            try:
                # Python 3.9+ 使用 to_thread
                await asyncio.to_thread(self.put_file, path, content, mode)
            except AttributeError:
                # Python 3.7-3.8 使用 run_in_executor
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self.put_file, path, content, mode)

    async def _async_get_conf_from_file(self, path, parse_func=None):
        """异步从文件获取配置"""
        if path and os.path.isdir(path):
            path = os.path.join(path, self.default_file)

        if not path or not os.path.isfile(path):
            return {}
        
        if path not in _files_cached:
            self.path = path
            if parse_func:
                # 如果提供了解析函数，在线程池中运行（因为 anyconfig 是同步的）
                try:
                    # Python 3.9+ 使用 to_thread
                    _files_cached[path] = await asyncio.to_thread(parse_func, path)
                except AttributeError:
                    # Python 3.7-3.8 使用 run_in_executor
                    loop = asyncio.get_event_loop()
                    _files_cached[path] = await loop.run_in_executor(None, parse_func, path)
            else:
                # 异步读取文件内容
                try:
                    import aiofiles
                    async with aiofiles.open(path, "rb") as file_to_read:
                        content = await file_to_read.read()
                    _files_cached[path] = content
                except ImportError:
                    # 如果没有安装 aiofiles，回退到同步方式
                    try:
                        # Python 3.9+ 使用 to_thread
                        _files_cached[path] = await asyncio.to_thread(self._sync_read_file, path)
                    except AttributeError:
                        # Python 3.7-3.8 使用 run_in_executor
                        loop = asyncio.get_event_loop()
                        _files_cached[path] = await loop.run_in_executor(
                            None, self._sync_read_file, path
                        )
        return _files_cached[path]

    def _sync_read_file(self, path):
        """同步读取文件的辅助方法（用于回退）"""
        with open(path, "rb") as file_to_read:
            return file_to_read.read()
