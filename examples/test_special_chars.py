# -*- coding: utf-8 -*-
# 测试特殊字符键名访问

from easy_config_py import EasyConfig, Dict

print("=" * 50)
print("测试 Dict 类的特殊字符键名访问")
print("=" * 50)

# 测试1: 包含连字符的键名
d = Dict({
    'key-with-dash': 1,
    'key_with_underscore': 2,
    'nested': {
        'sub-key': 3,
        'sub_key': 4
    }
})

print("\n1. 使用 getattr 访问包含特殊字符的键:")
print(f"   d.getattr('key-with-dash') = {d.getattr('key-with-dash')}")
print(f"   d.getattr('key_with_underscore') = {d.getattr('key_with_underscore')}")
print(f"   d.getattr('nested.sub-key') = {d.getattr('nested.sub-key')}")
print(f"   d.getattr('nested.sub_key') = {d.getattr('nested.sub_key')}")

# 测试2: 使用 setattr 设置包含特殊字符的键
print("\n2. 使用 setattr 设置包含特殊字符的键:")
d.setattr('new-key-with-dash', 100)
d.setattr('new-nested.sub-key', 200)
print(f"   d.getattr('new-key-with-dash') = {d.getattr('new-key-with-dash')}")
print(f"   d.getattr('new-nested.sub-key') = {d.getattr('new-nested.sub-key')}")

# 测试3: 使用方括号访问（原有方式仍然可用）
print("\n3. 使用方括号访问（原有方式）:")
print(f"   d['key-with-dash'] = {d['key-with-dash']}")
print(f"   d['nested']['sub-key'] = {d['nested']['sub-key']}")

print("\n" + "=" * 50)
print("测试 EasyConfig 的特殊字符键名访问")
print("=" * 50)

# 测试4: 从配置文件加载包含特殊字符的键
config = EasyConfig()
yaml_content = """
database:
  host-name: localhost
  port-number: 5432
  user-name: admin
app:
  api-key: secret123
  timeout-seconds: 30
"""

config.load_by_content(yaml_content)

print("\n4. 使用 getattr 访问配置中的特殊字符键:")
print(f"   config.getattr('database.host-name') = {config.getattr('database.host-name')}")
print(f"   config.getattr('database.port-number') = {config.getattr('database.port-number')}")
print(f"   config.getattr('app.api-key') = {config.getattr('app.api-key')}")
print(f"   config.getattr('app.timeout-seconds') = {config.getattr('app.timeout-seconds')}")

# 测试5: 使用 setattr 设置包含特殊字符的配置
print("\n5. 使用 setattr 设置包含特殊字符的配置:")
config.setattr('new-service.endpoint-url', 'https://api.example.com')
config.setattr('new-service.retry-count', 3)
print(f"   config.getattr('new-service.endpoint-url') = {config.getattr('new-service.endpoint-url')}")
print(f"   config.getattr('new-service.retry-count') = {config.getattr('new-service.retry-count')}")

# 测试6: 使用方括号访问（原有方式）
print("\n6. 使用方括号访问（原有方式）:")
print(f"   config.data['database']['host-name'] = {config.data['database']['host-name']}")
print(f"   config.data['app']['api-key'] = {config.data['app']['api-key']}")

print("\n" + "=" * 50)
print("测试完成！")
print("=" * 50)

