#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: util_compress.py
@time: 2023/5/28 14:58
@desc: rarfile 使用需要安装 rarfile 和 unrar 并且将 unrar.exe 复制到venv/Scrpits目录下
"""
import os
import gzip
from zipfile import ZipFile
import shutil
import rarfile
from sdk.utils.util_folder import FolderProcess
from sdk.utils.util_file import FileProcess


class ZipProcess(object):
    """
    压缩，解压文件
    """

    def __init__(self):
        """

        """
        self.folder = FolderProcess()
        self.file = FileProcess()
        self.format = [".zip", ".rar", ".gz"]

    def zip(self, zip_name: str, filefolder: str = None, kind: str = "zip"):
        """
        压缩
        :param zip_name:
        :param filefolder: 支持file/folder
        :param kind: zip,tar,gztar等
        :return:
        """
        shutil.make_archive(zip_name, kind, filefolder)

    def _check_zip_files(self, save_folder):
        """

        :param save_folder:
        :return:
        """
        for args in self.folder.get_all_files(save_folder):
            tail = self.file.get_file_tail(args["file"])
            if tail in self.format:
                self.unzip(args["file"], os.sep.join(self.folder.split_path(args["file"])[:-1]))

    def unzip(self, zip_file: str, save_path: str = "./"):
        """
        解压 原路径结构 中文会出现乱码（原因未知）
        :param zip_file:
        :param save_path:可以不存在
        :return:
        """
        file_split = self.folder.split_path(zip_file)
        save_folder = self.folder.merge_path([save_path, file_split[-1].split(".")[0]])
        self.folder.create_folder(save_folder)

        file_name = file_split[-1]

        if zip_file.lower().endswith(".zip"):
            with ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(save_folder)
        elif zip_file.lower().endswith(".rar"):
            with rarfile.RarFile(zip_file) as rar_file:
                rar_file.extractall(save_folder)
        elif zip_file.lower().endswith(".gz"):
            with gzip.open(zip_file, 'rb') as gz_file, \
                    open(self.folder.merge_path([save_folder, file_name]), 'wb') as output_file:
                output_file.write(gz_file.read())
        else:
            raise ValueError("不支持的格式:{}".format(zip_file))
        # 删除已经解压的压缩文件
        self.folder.remove(zip_file)
        # 遍历已经解压的压缩包内容，检查嵌套压缩文件继续解压
        self._check_zip_files(save_folder)

    @staticmethod
    def zip_files(zip_path: str, zip_name: str = "1.zip"):
        """
        压缩
        Args:
            zip_path: 待压缩目录
            zip_name: 压缩后文件路径

        Returns:

        """
        with ZipFile(zip_name, 'w') as zip:
            for folder_name, subfolders, filenames in os.walk(zip_path):
                for _zip_name in filenames:
                    file_path = os.path.join(folder_name, _zip_name)
                    arcname = os.path.relpath(file_path, zip_path)
                    zip.write(file_path, arcname)

    @staticmethod
    def unzip_file(zip_file: str, target_path: str = "./", rm: bool = False):
        """
        解压zip到指定目录
        Args:
            zip_file: 压缩文件目录
            target_path: 解压后目录
            rm:

        Returns:

        """
        # 创建解压目录
        os.makedirs(target_path, exist_ok=True)

        with ZipFile(zip_file, 'r') as unzip:
            unzip.extractall(target_path)
        # 删除zip
        if rm:
            os.remove(zip_file)
