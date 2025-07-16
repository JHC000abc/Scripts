# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: util_jsonl.py
@time: 2024/7/31 14:53 
@desc: 

"""
import os.path

from sdk.utils.util_json import JsonProcess


class JSONL(object):
    """

    """

    def __init__(self):
        self.json = JsonProcess()

    def read_yield_jsonl(self, file, encoding="utf-8", format=True):
        """

        :param file:
        :param encoding:
        :return:
        """
        with open(file, "r", encoding=encoding) as fp:
            for i in fp:
                if format:
                    yield self.json.loads(i.strip())
                else:
                    yield i.strip()

    def write_to_jsonl(self, file, data, rm=True):
        """

        :param file:
        :param data:  [{}]
        :param rm:  是否删除已存在文件 不删除 采用a 模式写入
        :return:
        """
        mode = "w"
        if os.path.exists(file):
            if rm:
                os.remove(file)
            else:
                mode = "a"
        with open(file, mode, encoding="utf-8") as fp:
            for i in data:
                fp.write(f"{self.json.dumps(i, indent=None)}\n")

    def read_json(self, file, encoding="utf-8"):
        """

        :param file:
        :param encoding:
        :return:
        """
        with open(file, "r", encoding=encoding) as fp:
            return self.json.loads(fp.read())
