#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: base_temp.py
@time: 2023/5/27 21:07
@desc:
"""
import os
import shutil


class Base(object):
    """

    """

    def read_yield(self, file: str, headers: list = None,
                   encoding: str = "utf-8", spliter: str = "\t", sheets: list = None) -> dict:
        """
        按行返回
        :param file:
        :param headers:
        :param encoding:
        :return:
        """

    def save(self, file: str, data: dict, mode: str = "w", encoding: str = "utf-8",
             spliter: str = "\t", indent: int = None, ensure_ascii: bool = False) -> str:
        """
        保存结果
        :param file:
        :param data:{'headers': ['', '', ''], 'data': [{"line":1,"data":[]},{"line":2,"data":[]}]} /
                    {'headers': ['', '', ''], 'data': [{"line":1,"data":[{},{}]},{"line":2,"data":["{}","{}"]}]}
        :param mode:
        :param encoding:
        :return:
        """

    def remove(self, file: str = None, folder: str = None):
        """
        删除文件、文件夹
        :param file:
        :param folder:
        :return:
        """
        try:
            if file:
                os.remove(file)
            if folder:
                shutil.rmtree(folder)
            return True
        except:
            return False
