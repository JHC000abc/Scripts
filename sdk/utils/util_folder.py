#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: util_folder.py
@time: 2023/5/28 13:56
@desc:
"""
import os
import traceback
import shutil
from sdk.base.base_temp import Base


class FolderProcess(Base):
    """

    """

    def __init__(self):
        super(FolderProcess, self).__init__()

    def create_folder(self, path):
        """
        创建文件夹
        :param _path:
        :return:
        """
        os.makedirs(path, exist_ok=True)

    def merge_path(self, path_lis):
        """
        合并路径
        :param path_lis:
        :return:
        """
        if path_lis:
            return os.path.sep.join(path_lis)

    def split_path(self, path: str, spliter: str = None):
        """
        拆分路径
        """
        if not spliter:
            if not path.startswith("http://") or not path.startswith("https://"):
                return os.path.normpath(path).split(os.sep)
            else:
                return os.path.normpath(path).split("/")
        else:
            return path.split(spliter)

    def remove(self, file: str = None, folder: str = None):
        """
        删除文件、文件夹
        :param file:
        :param folder:
        :return:
        """
        try:
            if folder:
                shutil.rmtree(folder)
            if file:
                os.remove(file)
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)

    def get_all_files(self, path: str, ext: list = None):
        """
        获取文件夹下所有文件绝对路径
        :param path:
        :param ext: 后缀列表[".txt",".json",...]
        :return:
        """
        try:
            if os.path.exists(path) and os.path.isabs(path):
                for path, dir_lis, file_lis in os.walk(path):
                    if len(file_lis) > 0:
                        for name in file_lis:
                            if ext:
                                if os.path.splitext(name)[-1] in ext:
                                    yield {
                                        "name": name,
                                        "file": os.path.join(path, name),
                                    }
                            else:
                                yield {
                                    "name": name,
                                    "file": os.path.join(path, name),
                                }
        except BaseException:
            print(traceback.format_exc())
