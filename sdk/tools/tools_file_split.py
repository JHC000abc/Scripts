# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: tools_file_split.py
@time: 2024/3/4 15:53
@desc:

"""

from sdk.temp.temp_supports import IsSolution


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

    def process(self, **kwargs):
        """
        处理文件

        :param kwargs: 关键字参数
        :return: 无返回值
        """
        in_path = kwargs["in_path"]
        save_path = kwargs["save_path"]
        self.folder.create_folder(save_path)
        file_split_size = 720
        for file, name in self.get_file(in_path, status=True):
            print(file, name)  # 打印文件名和名称
            _temp_lis = []
            _recode = 0
            for args in self.file.read_yield(file, headers=["jsonl"]):
                num = args["num"]
                line = args["line"]
                _temp_lis.extend(line)
                if num % file_split_size == 0:
                    _recode += 1
                    self.save_result(
                        self.folder.merge_path([save_path, f"{_recode}_[{file_split_size},{file_split_size}]_{name}"]),
                        data=_temp_lis
                    )
                    _temp_lis = []

            if len(_temp_lis) > 0:
                _recode += 1
                self.save_result(self.folder.merge_path([save_path, f"{_recode}_[{len(_temp_lis)},{file_split_size}]_{name}"]), data=_temp_lis)

            print(f"{file} 拆分为 {_recode} 个 文件")


if __name__ == '__main__':
    in_path = R"D:\Desktop\5"
    save_path = R"D:\Desktop\6"
    e = Solution()
    e.process(in_path=in_path, save_path=save_path)
