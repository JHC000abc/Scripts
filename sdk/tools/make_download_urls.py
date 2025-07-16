# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author  : v_jiaohaicheng@baidu.com
@des     :

"""

from sdk.temp.temp_supports import IsSolution
from sdk.utils.util_bos import BosAkSk


class Solution(IsSolution):
    def __init__(self, **kwargs):
        super(Solution, self).__init__()
        self.__dict__.update({k: v for k, v in [i for i in locals().values() if isinstance(i, dict)][0].items()})
        self.bos = BosAkSk()

    def process(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        in_path = kwargs["in_path"]
        save_path = kwargs["save_path"]

        out_lis = []

        for file in self.get_file(in_path):
            for args in self.read_line(file, headers=["1"]):
                url = args["line"][0]
                down_load_url = self.bos.get_download_url(url=url)
                out_lis.append([down_load_url])

        self.save_result("res.txt", data=out_lis)


if __name__ == '__main__':
    in_path = R"D:\Desktop\1"
    save_path = R"D:\Desktop\2"
    e = Solution()
    e.process(in_path=in_path, save_path=save_path)
