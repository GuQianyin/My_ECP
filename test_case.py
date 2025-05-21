# test_case.py
import pickle
import pytest
import hashlib
import sys
import json
import enum
import datetime
import inspect
import socket
import threading
import sqlite3
import asyncio
import os
from pathlib import Path
from collections import deque

# 配置区（协议版本设为1）
PICKLE_PROTOCOL = 1
TEST_RESULTS = {
    "valid_cases": {},
    "invalid_cases": {},
    "env_info": {
        "python_version": sys.version,
        "pickle_protocol": PICKLE_PROTOCOL,
        "platform": sys.platform
    }
}


# 自定义类型定义
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


# 确保模块路径一致性
import __main__

__main__.CustomClass = CustomClass
__main__.NestedClass = NestedClass
__main__.CyclicClass = CyclicClass


# 核心功能（协议版本强制设为1）
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


# 合法输入测试类
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
            TEST_RESULTS["valid_cases"][f"primitive_{name}"] = get_hash(obj)

    def test_containers(self):
        """容器类型测试"""
        containers = [
            ("list", [1, 2, 3]),
            ("tuple", (4, 5)),
            ("dict", {'a': 2, 'b': 1}),
            ("set", {1, 2, 3}),
            ("frozenset", frozenset([4, 5, 6])),
            ("deque", deque([1, 2, 3])),
            ("bytearray", bytearray(b'abc')),
            ("memoryview", memoryview(b"test")),
            ("nested", [{'x': (1, 2)}, {5, 6}, bytearray(b'data')])
        ]
        for name, obj in containers:
            TEST_RESULTS["valid_cases"][f"container_{name}"] = get_hash(obj)

    def test_custom_objects(self):
        """自定义对象测试"""
        cases = [
            ("simple", CustomClass(5)),
            ("nested", [NestedClass(10), NestedClass(20)]),
            ("cyclic", self._create_cyclic_ref()),
            ("slots", SlotsClass())
        ]
        for name, obj in cases:
            TEST_RESULTS["valid_cases"][f"custom_{name}"] = get_hash(obj)

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
            TEST_RESULTS["valid_cases"][f"special_{name}"] = get_hash(obj)





if __name__ == "__main__":
    # 显式调用 pytest 并传递当前文件的绝对路径
    pytest.main([os.path.abspath(__file__), "-v"])