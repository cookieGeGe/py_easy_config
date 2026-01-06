# -*- coding: utf-8 -*-
# @Time    : 2023/6/13-10:57
# @Author  : 灯下客
# @Email   : 
# @File    : Dict.py
# @Software: PyCharm


import copy


class Dict(dict):

    def __init__(self, *args, **kwargs):
        object.__setattr__(self, '__parent', kwargs.pop('__parent', None))
        object.__setattr__(self, '__key', kwargs.pop('__key', None))
        object.__setattr__(self, '__frozen', False)
        for arg in args:
            if not arg:
                continue
            elif isinstance(arg, dict):
                for key, val in arg.items():
                    self[key] = self._hook(val)
            elif isinstance(arg, tuple) and (not isinstance(arg[0], tuple)):
                self[arg[0]] = self._hook(arg[1])
            else:
                for key, val in iter(arg):
                    self[key] = self._hook(val)

        for key, val in kwargs.items():
            self[key] = self._hook(val)

    def __setattr__(self, name, value):
        if hasattr(self.__class__, name):
            raise AttributeError(f"'Dict' object attribute '{name}' is read-only")
        else:
            self[name] = value

    def __setitem__(self, name, value):
        is_frozen = (hasattr(self, '__frozen') and
                    object.__getattribute__(self, '__frozen'))
        if is_frozen and name not in super(Dict, self).keys():
                raise KeyError(name)
        super(Dict, self).__setitem__(name, value)
        try:
            p = object.__getattribute__(self, '__parent')
            key = object.__getattribute__(self, '__key')
        except AttributeError:
            p = None
            key = None
        if p is not None:
            p[key] = self
            object.__delattr__(self, '__parent')
            object.__delattr__(self, '__key')

    def __add__(self, other):
        if not self.keys():
            return other
        else:
            self_type = type(self).__name__
            other_type = type(other).__name__
            msg = "unsupported operand type(s) for +: '{}' and '{}'"
            raise TypeError(msg.format(self_type, other_type))

    @classmethod
    def _hook(cls, item):
        if isinstance(item, dict):
            return cls(item)
        elif isinstance(item, (list, tuple)):
            return type(item)(cls._hook(elem) for elem in item)
        return item

    def __getattr__(self, item):
        return self.__getitem__(item)
    
    def getattr(self, key, default=None):
        """
        通过字符串键名获取值，支持包含特殊字符的键名。
        
        这个方法可以访问包含特殊字符（如 '-'）或 Python 关键字的键名。
        
        Args:
            key: 键名（字符串），支持点号分隔的嵌套路径
            default: 如果键不存在时返回的默认值
        
        Returns:
            对应的值，如果键不存在返回 default
        
        示例:
            >>> d = Dict({'key-with-dash': 1, 'nested': {'sub-key': 2}})
            >>> d.getattr('key-with-dash')  # 1
            >>> d.getattr('nested.sub-key')  # 2
            >>> d.getattr('not-exist', 'default')  # 'default'
        """
        if '.' in key:
            # 支持嵌套路径访问
            keys = key.split('.')
            current = self
            for k in keys:
                if isinstance(current, Dict):
                    if k not in current:
                        return default
                    current = current[k]
                elif isinstance(current, dict):
                    if k not in current:
                        return default
                    current = current[k]
                else:
                    return default
            return current
        else:
            # 直接访问
            return self.get(key, default)

    def __missing__(self, name):
        if object.__getattribute__(self, '__frozen'):
            raise KeyError(name)
        return self.__class__(__parent=self, __key=name)

    def __delattr__(self, name):
        del self[name]

    def to_dict(self):
        base = {}
        for key, value in self.items():
            if isinstance(value, type(self)):
                base[key] = value.to_dict()
            elif isinstance(value, (list, tuple)):
                base[key] = type(value)(
                    item.to_dict() if isinstance(item, type(self)) else
                    item for item in value)
            else:
                base[key] = value
        return base

    def copy(self):
        return copy.copy(self)

    def deepcopy(self):
        return copy.deepcopy(self)

    def __deepcopy__(self, memo):
        other = self.__class__()
        memo[id(self)] = other
        for key, value in self.items():
            other[copy.deepcopy(key, memo)] = copy.deepcopy(value, memo)
        return other

    def update(self, *args, **kwargs):
        other = {}
        if args:
            if len(args) > 1:
                raise TypeError("update() takes at most 1 positional argument")
            other.update(Dict(args[0]))
        other.update(Dict(kwargs))
        for k, v in other.items():
            if ((k not in self) or
                (not isinstance(self[k], dict)) or
                (not isinstance(v, dict))):
                value = v
                if isinstance(v, list):
                    value = [Dict(item) if isinstance(item, dict) else item for item in v]
                self[k] = value
            else:
                self[k].update(Dict(v))

    def __getnewargs__(self):
        return tuple(self.items())

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)

    def __or__(self, other):
        if not isinstance(other, (Dict, dict)):
            return NotImplemented
        new = Dict(self)
        new.update(other)
        return new

    def __ror__(self, other):
        if not isinstance(other, (Dict, dict)):
            return NotImplemented
        new = Dict(other)
        new.update(self)
        return new

    def __ior__(self, other):
        self.update(other)
        return self

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
        return self[key]

    def setattr(self, key, value):
        """
        通过字符串键名设置值，支持包含特殊字符的键名和嵌套路径。
        
        Args:
            key: 键名（字符串），支持点号分隔的嵌套路径
            value: 要设置的值
        
        Raises:
            TypeError: 如果中间路径的值不是字典类型且无法转换
        
        示例:
            >>> d = Dict()
            >>> d.setattr('key-with-dash', 1)
            >>> d.setattr('nested.sub-key', 2)
            >>> d.getattr('key-with-dash')  # 1
            >>> d.getattr('nested.sub-key')  # 2
        """
        if '.' in key:
            # 支持嵌套路径设置
            keys = key.split('.')
            current = self
            for k in keys[:-1]:
                if k not in current:
                    current[k] = Dict()
                elif isinstance(current[k], Dict):
                    # 已经是 Dict，直接使用
                    pass
                elif isinstance(current[k], dict):
                    # 是普通字典，转换为 Dict
                    current[k] = Dict(current[k])
                else:
                    # 不是字典类型，无法创建嵌套路径
                    raise TypeError(
                        f"Cannot set nested path '{key}': "
                        f"'{k}' is not a dict (got {type(current[k]).__name__})"
                    )
                current = current[k]
            # 设置最后一个键的值
            current[keys[-1]] = self._hook(value)
        else:
            # 直接设置
            self[key] = self._hook(value)

    def freeze(self, should_freeze=True):
        object.__setattr__(self, '__frozen', should_freeze)
        for key, val in self.items():
            if isinstance(val, Dict):
                val.freeze(should_freeze)

    def unfreeze(self):
        self.freeze(False)
