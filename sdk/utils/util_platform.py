# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: util_platform.py
@time: 2023/9/10 21:09
@desc:

"""
import sys


class PlatformInfo(object):
    """
    操作系统平台信息
    """

    def __init__(self):
        """

        """

    def get_paltform(self):
        """
        获取操作系统平台信息
        """
        platform = sys.platform
        if platform == "linux":
            return "Linux"
        elif platform == "win32":
            return "Windows"
        elif platform == "darwin":
            return "MacOS"
        else:
            raise ValueError("UnSupport")
