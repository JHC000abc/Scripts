# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author  : v_jiaohaicheng@baidu.com
@des     :

"""

from sdk.temp.temp_supports import IsSolution


class Solution(IsSolution):
    def __init__(self, **kwargs):
        super(Solution, self).__init__()
        self.__dict__.update({k: v for k, v in [
                             i for i in locals().values() if isinstance(i, dict)][0].items()})

    def process(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        in_path = kwargs["in_path"]
        save_path = kwargs["save_path"]
        self.folder.create_folder(save_path)
        headers = kwargs["headers"]
        NUMS = 0
        with open(self.folder.merge_path([save_path, "all.txt"]), "w", encoding="utf-8")as fp:
            if headers:
                fp.write("{}\n".format("\t".join(headers)))
            for file in self.get_file(in_path):
                if headers:
                    NUMS += self.file.get_file_lines(file, 1) - 1
                else:
                    NUMS += self.file.get_file_lines(file, 1)
                for args in self.read_line(file):
                    data = args["line"]
                    fp.write("{}\n".format("\t".join(data)))
        print(NUMS)


if __name__ == '__main__':
    in_path = R"D:\Desktop\result"
    save_path = R"D:\Desktop\4"
    headers = ["folder", "url", "name"]
    e = Solution()
    e.process(in_path=in_path, save_path=save_path, headers=headers)
