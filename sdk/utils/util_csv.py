# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: util_csv.py
@time: 2024/7/31 14:51 
@desc: 

"""
import csv
import pandas as pd


class CSV(object):
    """
    CSV
    """

    def read_yield_csv(self, file, headers=None, encoding="utf-8"):
        """

        :param file:
        :param heaers:
        :param encoding:
        :return:
        """
        if not headers:
            flag = False
        else:
            flag = True

        with open(file, newline='', encoding=encoding, errors="ignore") as csvfile:
            for ind, line in enumerate(csv.reader(csvfile)):
                if ind == 0:
                    if not headers:
                        headers = [i.replace("\ufeff", "") for i in line]
                    else:
                        if flag:
                            ind = ind + 1
                        yield {
                            "headers": headers,
                            "num": ind,
                            "line": line,
                        }
                        continue

                if ind > 0:
                    if flag:
                        ind = ind + 1
                    yield {
                        "headers": headers,
                        "num": ind,
                        "line": line,
                    }

    def write_to_csv(self, file, data, headers, encoding="gbk"):
        """

        :param file:
        :param data:[[,,,],[,,,],[,,,],[,,,]]
        :param headers:[,,,]
        :param encoding:
        :return:
        """
        map = {}
        for ind, val in enumerate(headers):
            _temp = []
            for i in data:
                _i = i[ind].replace("\u2708", "").replace("\ufffd", "").replace('\ufe0f', "").replace("\u2753",
                                                                                                      "") if isinstance(
                    i[ind], str) else i[ind]
                _temp.append(_i)
            map[val] = _temp

        df = pd.DataFrame(map)
        df.to_csv(file, index=False, encoding=encoding)
