# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: re_upload_by_files.py
@time: 2025/4/28 12:39 
@desc: 

"""
import os
from sdk.utils.util_bos import BosOnline
from sdk.temp.temp_supports import IsSolution, DM


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
        self.bos = BosOnline()

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

    @DM.add_project()
    def upload(self, file, url):
        """

        :param file:
        :param url:
        :return:
        """
        return self.bos.upload(url, file)

    def process(self, **kwargs):
        """
        处理文件

        :param kwargs: 关键字参数
        :return: 无返回值
        """
        self.in_path = kwargs["in_path"]
        self.save_path = kwargs["save_path"]
        self.folder.create_folder(self.save_path)
        file = r"C:\Users\v_jiaohaicheng\Downloads\result_llm_72_2025-05-16 16-40-42.xlsx"
        for args in self.excel.read_yield_xlsx_by_xlrd(file):
            print(args)
            local = self.get_one_from_yield_args(args, "org")
            bos_url = self.get_one_from_yield_args(args, "url")
            # bos = self.json.loads(bos)
            # bos_url = bos["url"]
            # local = rf"D:\Desktop\1\upload\mmbench-video\{local}.mp4"
            # print(local,bos_url)
            if not os.path.exists(local):
                print("not found")
            self.upload(local, bos_url)
            # break
        DM.close_pool()


if __name__ == '__main__':
    in_path = R"D:\Desktop\1\re_upload_by_files"
    save_path = R"D:\Desktop\2\re_upload_by_files"
    e = Solution()
    e.process(in_path=in_path, save_path=save_path)
