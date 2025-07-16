# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: merge_excels.py
@time: 2025/4/9 19:38 
@desc: 

"""

from sdk.temp.temp_supports import IsSolution, DM
from sdk.utils.util_class import PathParser


class Solution(IsSolution):
    """
    Solution
    """

    def __init__(self, **kwargs):
        """
        初始化函数
        :param kwargs: 字典类型的参数字典，包含可选的关键字参数
        """
        super(Solution, self).__init__()
        self.__dict__.update({k: v for k, v in [
            i for i in locals().values() if isinstance(i, dict)][0].items()})

    def exit_handler(self):
        """
        程序退出自动执行
        :return:
        """
        print("程序退出")

    # @DM.add_project()
    def muti_thread_function(self, args):
        """
        处理数据函数
        :param args:
        :return:
        """

        return None

    def process(self, **kwargs):
        """
        处理文件

        :param kwargs: 关键字参数
        :return: 无返回值
        """
        self.in_path = kwargs["in_path"]
        self.save_path = kwargs["save_path"]
        self.folder.create_folder(self.save_path)
        main_headers = []
        recode_nums = 0
        for file, file_name in self.get_file(self.in_path, status=True):
            print(file, file_name)
            obj = PathParser(file)
            if obj.tail != "xlsx":
                continue
            recode_nums += 1
            for args in self.excel.read_yield_xlsx_by_xlrd(file):
                headers = args["headers"]
                if main_headers == []:
                    main_headers = headers
                if headers != main_headers:
                    print("not match headers")
                    continue
                self.success_lis.append(args["line"])

        DM.close_pool()
        self.excel.write(self.folder.merge_path([self.save_path, f"merge_result_{recode_nums}.xlsx"]),
                         [self.success_lis], [main_headers])
        self.success_lis = []


if __name__ == '__main__':
    in_path = R"D:\Desktop\2\r_2013"
    save_path = R"D:\Desktop\2\merge_excels"
    e = Solution()
    e.process(in_path=in_path, save_path=save_path)
