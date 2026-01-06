# EasyConfig

一个简单易用的 Python 配置管理库，支持多种配置文件格式，提供便捷的点号访问和异步操作支持。

## 特性

- 🚀 **多种格式支持**: 支持 YAML、JSON、TOML、INI 等多种配置文件格式（通过 anyconfig）
- 📝 **点号访问**: 支持类似 JavaScript 的点号访问方式，代码更简洁
- 🔄 **异步支持**: 同时支持同步和异步操作，适合现代 Python 应用
- 🔑 **特殊字符键名**: 支持访问包含特殊字符（如 `-`）或 Python 关键字的键名
- 🎯 **自动转换**: 自动将嵌套字典转换为 Dict 对象，支持链式访问
- 💾 **文件缓存**: 自动缓存已加载的配置文件，提高性能
- 🔒 **冻结功能**: 支持冻结配置，防止意外修改

## 安装

### 基础安装（仅同步功能）

```bash
pip install easy-config-py
```

### 完整安装（包含异步功能，推荐）

```bash
pip install easy-config-py[aio]
```

或者手动安装异步依赖：

```bash
pip install easy-config-py aiofiles
```

## 快速开始

### 基本使用

```python
from easy_config_py import EasyConfig

# 创建配置对象
config = EasyConfig(path="./config")

# 加载配置文件（默认查找 config.yml）
config.load_file()

# 使用点号访问配置
print(config.database.host)      # localhost
print(config.database.port)      # 5432
print(config.app.name)           # MyApp
```

### 从内容加载

```python
from easy_config_py import EasyConfig

config = EasyConfig()

# 从字符串内容加载配置
yaml_content = """
database:
  host: localhost
  port: 5432
app:
  name: MyApp
  debug: true
"""

config.load_by_content(yaml_content, parser_type='yml')
print(config.database.host)  # localhost
```

## 详细用法

### 1. 点号访问

```python
from easy_config_py import EasyConfig

config = EasyConfig()
config.load_file("config.yml")

# 访问嵌套配置
host = config.database.host
port = config.database.port

# 动态创建嵌套键
config.new_key.sub_key = "value"
print(config.new_key.sub_key)  # value
```

### 2. 访问特殊字符键名

如果配置文件中包含特殊字符（如 `-`）或 Python 关键字，可以使用 `getattr()` 和 `setattr()` 方法：

```python
from easy_config_py import EasyConfig

config = EasyConfig()
config.load_by_content("""
database:
  host-name: localhost
  port-number: 5432
app:
  api-key: secret123
""")

# 使用 getattr 访问包含特殊字符的键
host = config.getattr('database.host-name')      # localhost
port = config.getattr('database.port-number')   # 5432
api_key = config.getattr('app.api-key')         # secret123

# 使用 setattr 设置包含特殊字符的键
config.setattr('new-service.endpoint-url', 'https://api.example.com')
print(config.getattr('new-service.endpoint-url'))
```

### 3. 异步操作

```python
import asyncio
from easy_config_py import EasyConfig

async def main():
    config = EasyConfig(path="./config")
    
    # 异步加载配置文件
    await config.async_load_file()
    
    # 异步从内容加载
    await config.async_load_by_content("key: value", parser_type='yml')
    
    # 访问配置（与同步方式相同）
    print(config.database.host)

# 运行异步函数
asyncio.run(main())
```

### 4. 在异步框架中使用

```python
# FastAPI 示例
from fastapi import FastAPI
from easy_config_py import EasyConfig

app = FastAPI()
config = EasyConfig()

@app.on_event("startup")
async def startup():
    await config.async_load_file("config.yml")

@app.get("/")
async def read_root():
    return {
        "database_host": config.database.host,
        "app_name": config.app.name
    }
```

### 5. 使用 Dict 类

```python
from easy_config_py import Dict

# 创建 Dict 对象
d = Dict({
    'database': {
        'host': 'localhost',
        'port': 5432
    }
})

# 点号访问
print(d.database.host)  # localhost
print(d.database.port)  # 5432

# 动态创建嵌套键
d.new_key.sub_key = "value"

# 转换为普通字典
normal_dict = d.to_dict()

# 冻结配置（防止修改）
d.freeze()
# d.new_key = "value"  # 会抛出 KeyError
```

### 6. 配置更新和合并

```python
from easy_config_py import EasyConfig

config = EasyConfig()
config.load_file("config.yml")

# 更新配置
config.update({
    'database': {
        'host': 'newhost'
    }
})

# 深度合并
config.update({
    'database': {
        'port': 3306  # 只更新 port，host 保持不变
    }
})
```

## API 文档

### EasyConfig 类

#### 初始化

```python
EasyConfig(data=None, path=None, default_filename='config.yml')
```

- `data`: 初始配置数据（字典）
- `path`: 配置文件路径或目录路径
- `default_filename`: 默认配置文件名

#### 主要方法

| 方法 | 说明 | 示例 |
|------|------|------|
| `load_file(path=None)` | 同步加载配置文件 | `config.load_file()` |
| `async_load_file(path=None)` | 异步加载配置文件 | `await config.async_load_file()` |
| `load_by_content(content, parser_type='yml')` | 同步从内容加载 | `config.load_by_content(yaml_str)` |
| `async_load_by_content(content, parser_type='yml')` | 异步从内容加载 | `await config.async_load_by_content(yaml_str)` |
| `getattr(key, default=None)` | 获取配置值（支持特殊字符） | `config.getattr('key-with-dash')` |
| `setattr(key, value)` | 设置配置值（支持特殊字符） | `config.setattr('new-key', 'value')` |
| `update(*args, **kwargs)` | 更新配置（深度合并） | `config.update({'key': 'value'})` |
| `to_dict()` | 转换为普通字典 | `config.to_dict()` |
| `data` | 获取内部的 Dict 对象 | `config.data` |

### Dict 类

#### 主要方法

| 方法 | 说明 | 示例 |
|------|------|------|
| `getattr(key, default=None)` | 获取值（支持特殊字符和嵌套路径） | `d.getattr('nested.sub-key')` |
| `setattr(key, value)` | 设置值（支持特殊字符和嵌套路径） | `d.setattr('new-key', 'value')` |
| `to_dict()` | 转换为普通字典 | `d.to_dict()` |
| `freeze(should_freeze=True)` | 冻结字典（防止添加新键） | `d.freeze()` |
| `unfreeze()` | 解冻字典 | `d.unfreeze()` |
| `copy()` | 浅拷贝 | `d.copy()` |
| `deepcopy()` | 深拷贝 | `d.deepcopy()` |

## 支持的配置文件格式

通过 anyconfig 支持以下格式：

- YAML (`.yml`, `.yaml`)
- JSON (`.json`)
- TOML (`.toml`)
- INI (`.ini`)
- 更多格式请参考 [anyconfig 文档](https://python-anyconfig.readthedocs.io/)

## 性能说明

- **同步模式**: 使用标准文件 I/O，适合传统同步代码
- **异步模式**: 
  - 如果安装了 `aiofiles`，使用真正的异步文件 I/O
  - 如果未安装 `aiofiles`，会自动回退到在线程池中运行同步操作
  - 配置解析（anyconfig）始终在线程池中运行，避免阻塞事件循环

## 示例

查看 `examples/` 目录获取更多示例：

- `test.py` - 基本使用示例
- `async_example.py` - 异步使用示例
- `test_special_chars.py` - 特殊字符键名访问示例
- `config.yml` - 示例配置文件

## 许可证

MIT License

Copyright (c) 2023 cookieGeGe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 贡献

欢迎提交 Issue 和 Pull Request！

## 相关链接

- GitHub: [https://github.com/cookieGeGe/py_easy_config](https://github.com/cookieGeGe/py_easy_config)
- PyPI: [https://pypi.org/project/easy-config-py/](https://pypi.org/project/easy-config-py/)
