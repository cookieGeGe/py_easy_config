# -*- coding: utf-8 -*-
# 异步使用示例

import asyncio
from easy_config_py import EasyConfig, Dict


async def async_example():
    """异步加载配置示例"""
    print("=" * 50)
    print("异步示例: 加载配置文件")
    print("=" * 50)
    
    # 创建配置对象
    econfig = EasyConfig(path=__file__)
    
    # 异步加载配置文件
    await econfig.async_load_file()
    print(f"配置对象: {econfig}")
    print(f"访问配置项: econfig.hello.world = {econfig.hello.world}")
    print(f"访问列表: econfig.hello.list = {econfig.hello.list}")
    
    # 异步从内容加载配置
    yaml_content = """
    test:
      async_model: true
      value: 100
    """
    await econfig.async_load_by_content(yaml_content)
    print(f"\n从内容加载后: econfig.test.async_model = {econfig.test.async_model}")
    print(f"econfig.test.value = {econfig.test.value}")


def sync_example():
    """同步加载配置示例（原有功能保持不变）"""
    print("\n" + "=" * 50)
    print("同步示例: 加载配置文件")
    print("=" * 50)
    
    # 创建配置对象
    econfig = EasyConfig(path=__file__)
    
    # 同步加载配置文件
    econfig.load_file()
    print(f"配置对象: {econfig}")
    print(f"访问配置项: econfig.hello.world = {econfig.hello.world}")
    
    # 同步从内容加载配置
    yaml_content = """
    test:
      sync: true
      value: 200
    """
    econfig.load_by_content(yaml_content)
    print(f"\n从内容加载后: econfig.test.sync = {econfig.test.sync}")
    print(f"econfig.test.value = {econfig.test.value}")


async def main():
    """主函数"""
    # 运行异步示例
    await async_example()
    
    # 运行同步示例
    sync_example()


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())

