#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: util_file.py
@time: 2023/5/27 21:25
@desc:
"""
import os
import shutil
import traceback
import chardet
from sdk.base.base_temp import Base
from sdk.utils.util_json import JsonProcess


class FileProcess(Base):
    """
    文件处理类
    """

    def __init__(self):
        super(FileProcess, self).__init__()
        self.json = JsonProcess()

    def check_exists(self, file: str):
        """

        :param file:
        :return:
        """
        if os.path.exists(file):
            return True
        return False

    def get_file_lines(self, file: str, status: int = 1):
        """
        获取文件总行数
        :param file:
        :param status:0:大文件、1小文件
        :return:
        """
        if status == 1:
            return sum(1 for _ in open(file, 'rb'))
        else:
            with open(file, 'rb') as f:
                for count, _ in enumerate(f, 1):
                    pass
            return count

    def rename_file(self, old: str, new: str):
        """
        重命名文件
        :param old:
        :param new:
        :return:
        """
        try:
            if os.path.isfile(old) and not os.path.exists(new):
                os.renames(old, new)
        except BaseException:
            print(traceback.format_exc())

    def get_file_encode(self, file: str, size=1024 * 1024) -> str:
        """
        获取文件编码
        :param file:
        :param size:
        :return:
        """
        with open(file, "rb") as fp:
            fp_bit = fp.read(size)
        return chardet.detect(fp_bit)["encoding"]

    def get_file_size(self, file: str, unit: str = "MB") -> str:
        """
        获取文件大小
        :param file:
        :param unit:
        :return:
        """
        file_size = os.path.getsize(file)
        if unit == "KB":
            return str(round(file_size / float(1024), 2)) + " " + unit
        elif unit == "MB":
            return str(round(file_size / float(1024 * 1024), 2)) + " " + unit

    def get_file_tail(self, file: str):
        """
        获取文件后缀
        :param file:
        :return:
        """
        return os.path.splitext(file)[-1]

    def read_yield(self, file: str, headers: list = None,
                   encoding: str = "utf-8", spliter: str = "\t", sheets: list = None, mode="r") -> dict:
        """
        按行读文件
        :param file:
        :param headers:
        :param encoding:
        :param spliter:
        :param sheets:
        :return:
        """
        with open(file, mode=mode, encoding=encoding) as fp:
            # 传headers 从第一行开始处理，不传headers默认第一行为headers
            if not headers:
                headers = fp.readline().strip().split(spliter)
            for num, data in enumerate(fp):
                line = data.strip("\n").split(spliter)
                yield {
                    "headers": headers,
                    "num": num + 1,
                    "line": line
                }

    def read_json_file(self, file: str, encoding: str = "utf-8") -> dict:
        """
        读取json文件
        :param file:
        :param encoding:
        :return:
        """
        with open(file, "r", encoding=encoding) as fp:
            return self.json.loads(fp.read())

    def save(self, file: str, data: dict, mode: str = "w", encoding: str = "utf-8",
             spliter: str = "\t", indent: int = None, ensure_ascii: bool = False):
        """
        保存文件
        :param file:
        :param data:
        :param mode:
        :param encoding:
        :param spliter:
        :param indent:
        :param ensure_ascii:
        :return:
        """
        with open(file, mode=mode, encoding=encoding) as fp:
            tail = self.get_file_tail(file)
            if data.get("headers") is not None:
                if tail == ".txt":
                    fp.write("{}\n".format(spliter.join(data["headers"])))
                    for line in data.get("line"):
                        fp.write("{}\n".format(spliter.join(line)))
            else:
                if tail == ".json":
                    if isinstance(data["line"], dict):
                        fp.write(self.json.dumps(data["line"]))
                    else:
                        fp.write(self.json.dumps(data["line"]))

    def split_file(self, file: str, spliter_nums: int = 1000,
                   headers: str = None, encoding: str = "utf-8", spliter="\t") -> dict:
        """
        按行 拆分文件
        :param file:
        :param spliter_nums:
        :param headers:
        :param encoding:
        :return:
        """
        lis = []
        with open(file, "r", encoding=encoding) as fp:
            if not headers:
                headers = fp.readline().strip().split(spliter)
            for i in fp:
                line = i.strip().split(spliter)
                lis.append(line)
                if len(lis) == spliter_nums:
                    yield {
                        "headers": headers,
                        "line": lis,
                    }
                    lis.clear()
            if len(lis) > 0:
                yield {
                    "headers": headers,
                    "line": lis,
                }

    def merge_file(self, file1, file2, headers=None,
                   encoding="utf-8", mode="r"):
        """
        合并文件
        :param file1:待合并文件
        :param file2:合并后新文件
        :param headers:
        :param encoding:
        :param mode:
        :return:
        """
        with open(file2, "a", encoding=encoding) as fp:
            for args in self.read_yield(
                    file1, headers=headers, encoding=encoding, mode=mode):
                line = args["line"]
                fp.write("{}\n".format("\t".join(line)))

    def move_file(self, old_file, new_file, mode=True):
        """

        :param old_file:
        :param new_file:
        :param mode: 默认不删除原文件
        :return:
        """
        shutil.copy(old_file, new_file)
        if not mode:
            os.remove(old_file)
