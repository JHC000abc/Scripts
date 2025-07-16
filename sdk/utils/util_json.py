#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: util_json.py
@time: 2023/5/27 22:41
@desc:
"""
import json
import traceback
from typing import Dict, List, Generator


class JsonProcess:
    """
    json 序列化 反序列化
    """

    def loads(self, data: str) -> dict:
        """
        str - dict
        :param data:
        :return:
        """
        return json.loads(data, strict=False)

    def dumps(self, data: dict, indent: None = 4,
              ensure_ascii: bool = False) -> str:
        """
        dict-str
        :param data:
        :param indent:
        :param ensure_ascii:
        :return:
        """
        return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)

    def encode_path(self, rules: str) -> List[str]:
        """

        :param rules:
        :return:
        """
        rules = ",".join(rules.split(']['))
        rules = self.loads(rules)
        return rules

    def parse_json_by_path(self, data, path: List[str]) -> Generator:
        """

        :param data:
        :param rules:
        :return:
        """
        if len(path) == 0:
            yield data
            return

        _path, *path = path

        if _path == "*":
            if isinstance(data, Dict):
                yield from self.parse_json_by_path(data[_path], path)
            elif isinstance(data, List):
                for _data in data:
                    yield from self.parse_json_by_path(_data, path)
            return
        try:
            yield from self.parse_json_by_path(data[_path], path)
        except Exception as e:
            yield traceback.format_exc()
