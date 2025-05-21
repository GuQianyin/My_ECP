# ecp_test_case.py
import pickle
import pytest
import hashlib
import sys
import enum
import datetime
import os
import platform
import json
from pathlib import Path
from collections import deque

# 配置常量
PICKLE_PROTOCOL = 1


# 辅助函数 ----------------------------------------------------------
def obj_to_str(obj):
    """安全转换对象为可读字符串，避免递归崩溃"""
    visited = set()
    return _obj_to_str_helper(obj, visited)


def _obj_to_str_helper(obj, visited):
    """递归辅助函数"""
    obj_id = id(obj)
    if obj_id in visited:
        return '...'
    visited.add(obj_id)

    # 处理基础类型
    if isinstance(obj, (int, str, float, bool, type(None))):
        return repr(obj)

    # 处理容器类型
    elif isinstance(obj, (list, tuple, set, frozenset, deque)):
        items = [_obj_to_str_helper(item, visited) for item in obj]
        if isinstance(obj, list):
            return f"[{', '.join(items)}]"
        elif isinstance(obj, tuple):
            return f"({', '.join(items)})"
        elif isinstance(obj, set):
            return f"{{{', '.join(items)}}}"
        elif isinstance(obj, frozenset):
            return f"frozenset({{{', '.join(items)}}})"
        elif isinstance(obj, deque):
            return f"deque([{', '.join(items)}])"

    # 处理字典类型
    elif isinstance(obj, dict):
        pairs = []
        for k, v in obj.items():
            k_str = _obj_to_str_helper(k, visited)
            v_str = _obj_to_str_helper(v, visited)
            pairs.append(f"{k_str}: {v_str}")
        return f"{{{', '.join(pairs)}}}"

    # 处理路径对象
    elif isinstance(obj, Path):
        return f"Path({str(obj)!r})"

    # 处理时间对象
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()

    # 处理枚举类型
    elif isinstance(obj, enum.Enum):
        return f"{type(obj).__name__}.{obj.name}"

    # 处理有 __slots__ 的类
    elif hasattr(obj, '__slots__'):
        attrs = {attr: _obj_to_str_helper(getattr(obj, attr), visited) for attr in obj.__slots__ if hasattr(obj, attr)}
        return f"{type(obj).__name__}({attrs})"

    # 处理普通对象
    elif hasattr(obj, '__dict__'):
        attrs = {k: _obj_to_str_helper(v, visited) for k, v in obj.__dict__.items()}
        return f"{type(obj).__name__}({attrs})"

    # 其他类型
    else:
        return repr(obj)


# 保存函数 ----------------------------------------------------------
def save_test_result(obj, protocol, hash_value):
    """保存测试结果到系统/Python版本对应的文件"""
    system = platform.system().lower()
    py_version = f"py{sys.version_info.major}{sys.version_info.minor}"
    filename = f"{system}_{py_version}_results.txt"

    # 首次写入时记录环境信息
    if not os.path.exists(filename):
        env_info = {
            "python_version": sys.version,
            "pickle_protocol": protocol,
            "platform": sys.platform
        }
        with open(filename, "w") as f:
            f.write(f"ENV_INFO: {json.dumps(env_info, indent=2)}\n\n")

    # 追加测试结果
    with open(filename, "a") as f:
        f.write(f"Object: {obj}, Protocol: {protocol}, Hash: {hash_value}\n")


# 自定义类型定义 ----------------------------------------------------
class CustomClass:
    """用于测试的自定义类"""

    def __init__(self, value):
        self.value = value


class NestedClass:
    def __init__(self, value):
        self.value = value


class CyclicClass:
    def __init__(self):
        self.other = None


class SlotsClass:
    __slots__ = ['a', 'b']

    def __init__(self):
        self.a = 1
        self.b = 2


class Color(enum.Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


# 确保模块路径一致性 ------------------------------------------------
import __main__

__main__.CustomClass = CustomClass
__main__.NestedClass = NestedClass
__main__.CyclicClass = CyclicClass


# 核心功能 ----------------------------------------------------------
def get_hash(obj, protocol=PICKLE_PROTOCOL):
    """获取对象pickle哈希（强制使用协议1）"""
    try:
        data = pickle.dumps(obj, protocol=protocol)
        return hashlib.sha256(data).hexdigest()
    except Exception as e:
        return f"ERROR::{str(e)}"


def create_recursive_dict():
    """创建递归字典"""
    d = {}
    d['self'] = d
    return d


# 测试类 ------------------------------------------------------------
class TestValidEquivalence:
    """合法输入测试套件"""
    def test_primitive_types(self):
        """基本数据类型"""
        cases = [
            ("int", 42),
            ("string", "hello"),
            ("float", 3.14),
            ("bool_true", True),
            ("bool_false", False),
            ("none", None)
        ]
        for name, obj in cases:
            hash_value = get_hash(obj)
            obj_str = obj_to_str(obj)
            save_test_result(obj_str, PICKLE_PROTOCOL, hash_value)

    def test_containers(self):
        """容器类型测试"""
        containers = [
            ("list", [1, 2, 3]),
            ("tuple", (4, 5)),
            ("dict", {'b': 2, 'a': 1}),
            ("set", {1, 2, 3}),
            ("frozenset", frozenset([4, 5, 6])),
            ("deque", deque([1, 2, 3])),
            ("bytearray", bytearray(b'abc')),
            ("nested", [{'x': (1, 2)}, {5, 6}, bytearray(b'data')])
        ]
        for name, obj in containers:
            hash_value = get_hash(obj)
            obj_str = obj_to_str(obj)
            save_test_result(obj_str, PICKLE_PROTOCOL, hash_value)

    def test_custom_objects(self):
        """自定义对象测试"""
        cases = [
            ("simple", CustomClass(5)),
            ("nested", [NestedClass(10), NestedClass(20)]),
            ("cyclic", self._create_cyclic_ref()),
            ("slots", SlotsClass())
        ]
        for name, obj in cases:
            hash_value = get_hash(obj)
            obj_str = obj_to_str(obj)
            save_test_result(obj_str, PICKLE_PROTOCOL, hash_value)

    def _create_cyclic_ref(self):
        obj1 = CyclicClass()
        obj2 = CyclicClass()
        obj1.other = obj2
        obj2.other = obj1
        return obj1

    def test_special_types(self):
        """特殊数据类型测试"""
        cases = [
            ("pathlib", Path("/test/path")),
            ("datetime", datetime.datetime(2023, 1, 1)),
            ("enum", Color.RED),
            ("recursive_dict", create_recursive_dict()),
            ("nan_float", float('nan'))
        ]
        for name, obj in cases:
            hash_value = get_hash(obj)
            obj_str = obj_to_str(obj)
            save_test_result(obj_str, PICKLE_PROTOCOL, hash_value)


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__), "-v"])