#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: util_single.py
@time: 2023/6/13 23:26
@desc: 单例实现
"""
from functools import wraps


def single(cls):
    """
    装饰类
    :param cls:
    :return:
    """
    instance = {}

    @wraps(cls)
    def decorate(*args, **kwargs):
        if instance.get(cls) is None:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return decorate


def single_params(**params):
    """
    带参装饰器
    :param params:
    :return:
    """
    instance = {}

    def decorate(cls):
        @wraps(cls)
        def dec(*args, **kwargs):
            if instance.get(cls) is None:
                instance[cls] = cls(*args, **kwargs)
            print("params", params)
            return instance[cls]
        return dec
    return decorate


"""
实现单例模式的六种方式
1. 模块导入
2. 类装饰器
3. 类绑定方法 @classmethod
3. __new__() 方法
4. 元类中的__call__() 方法
5. 并发

"""


def singlemethod(func):
    """
    类装饰器
    :param func:
    :return:
    """
    obj = None

    def wrapper(*args, **kwargs):
        nonlocal obj
        if not obj:
            obj = func(*args, **kwargs)
        return obj
    return wrapper


class SingleMethodBind(object):
    """
    类绑定方法
    """
    obj = None

    @classmethod
    def singlemethod(cls, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        if not cls.obj:
            cls.obj = cls(*args, **kwargs)
        return cls.obj


class SingleMethodNew(object):
    """
    new 方法
    """
    obj = None

    def __new__(cls, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        if not cls.obj:
            cls.obj = super().__new__(cls, *args, **kwargs)
        return cls.obj


class MyType(type):
    """
    元类
    """
    obj = None

    def __call__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        if not self.obj:
            self.obj = super().__call__(*args, **kwargs)
        return self.obj
