# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author  : v_jiaohaicheng@baidu.com
@des     :

"""


class ToolsOthers(object):
    """
    常用工具
    """

    def split_list(self, lis: list, size: int = 1000):
        """
        根据size,拆分列表
        :param lis:
        :param size:
        :return:
        """
        len_lis = len(lis) + 1
        split_nums = len_lis // size if len_lis % size == 0 else len_lis // size + 1
        print(split_nums)
        for i in range(split_nums):
            yield lis[i * size:(i + 1) * size]
