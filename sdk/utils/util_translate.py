#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: util_translate.py
@time: 2023/6/12 20:20
@desc:
"""
import zhconv
import pypinyin


class TranProcess():
    """
    繁简体翻译
    """

    @staticmethod
    def tran_chinese(string: str, mode: int = 0):
        """
        繁简体转化
        :param string:
        :param mode:0：繁转简 ；1：简转繁
        :return:
        """
        if mode == 0:
            locale = 'zh-hans'
        elif mode == 1:
            locale = 'zh-hant'
        else:
            raise ValueError("mode not in (0,1)")
        return zhconv.convert(string, locale)

    @staticmethod
    def tran_Pinyin(string: str):
        """
        简体/繁体 中文转拼音
        :param string:
        :return:
        """
        return " ".join(
            [i[0] for i in pypinyin.pinyin(string, style=pypinyin.NORMAL)])
