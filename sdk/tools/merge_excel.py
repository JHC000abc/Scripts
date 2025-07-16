# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author  : v_jiaohaicheng@baidu.com
@des     :

"""
import xlsxwriter
import xlrd
from sdk.temp.temp_supports import IsSolution
from sdk.utils.util_excel import ExcelProcess
import pandas as pd


class Solution(IsSolution):
    def __init__(self, **kwargs):
        super(Solution, self).__init__()
        self.__dict__.update({k: v for k, v in [i for i in locals().values() if isinstance(i, dict)][0].items()})

        self.excel = ExcelProcess()

    def merge_excels(self, excel_files, save_file):
        """

        :param excel_files:
        :param save_file:
        :return:
        """
        # 创建一个空的 Excel writer 对象
        writer = pd.ExcelWriter(save_file, engine='xlsxwriter')

        # 遍历每个 Excel 文件
        for file in excel_files:
            # 读取当前文件的所有工作表数据
            xls = pd.ExcelFile(file)
            sheet_names = xls.sheet_names
            for sheet_name in sheet_names:
                df = pd.read_excel(file, sheet_name=sheet_name)
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        # 保存和关闭 Excel 文件
        writer.close()

    def process(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        in_path = kwargs["in_path"]
        save_path = kwargs["save_path"]
        self.folder.create_folder(save_path)
        excel_files = []

        for file in self.get_file(in_path):
            excel_files.append(file)

        self.merge_excels(excel_files, self.folder.merge_path([save_path, R"merge_result.xlsx"]))


if __name__ == '__main__':
    in_path = R"D:\Desktop\2\r_2013"
    save_path = R"D:\Desktop\2"
    e = Solution()
    e.process(in_path=in_path, save_path=save_path)
