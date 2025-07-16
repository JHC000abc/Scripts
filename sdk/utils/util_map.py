#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: util_map.py
@time: 2023/5/28 14:02
@desc:
"""
from typing import Any, Tuple


class MapProcess(object):
    """

    """

    def __init__(self):
        pass

    def reduce(self, map: dict, key: [
               str, int, bool, Tuple], value: Any, mode="a"):
        """
        聚合
        :param map:
        :param key:
        :param value:
        :param mode: a/w
        :return:
        """
        if not self.check_key(map, key):
            if mode == "a" and isinstance(map[key], list):
                map[key] = map[key].append(value)
            elif mode == "w":
                map[key] = value
            else:
                raise ValueError("unsupport mode : {}".format(mode))
        else:
            map[key] = value

        return map

    def check_key(self, map, key):
        """
        检查key是否存在
        :param map:
        :param key:
        :return:
        """
        if map.get(key) is not None:
            return True
        else:
            return False
