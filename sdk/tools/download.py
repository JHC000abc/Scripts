# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author  : v_jiaohaicheng@baidu.com
@des     :bos 批量下载工具

"""

from sdk.temp.temp_supports import IsSolution
from sdk.utils.util_bos import BosAkSk
from cup.util import ThreadPool


class Solution(IsSolution):
    def __init__(self, **kwargs):
        super(Solution, self).__init__()
        self.__dict__.update({k: v for k, v in [
                             i for i in locals().values() if isinstance(i, dict)][0].items()})
        self.bos = BosAkSk()
        self.pool = ThreadPool(minthreads=2, maxthreads=20)
        self.pool.start()

    def process(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        in_path = kwargs["in_path"]
        save_path = kwargs["save_path"]
        for file in self.get_file(in_path):
            for args in self.read_line_col(file, key_lis=["url", "folder", "name"]):
                url = args["url"]
                folder = args["folder"]
                name = args["name"]
                _save_path = self.folder.merge_path([save_path, folder])
                self.folder.create_folder(_save_path)
                save_file = self.folder.merge_path([_save_path, name])
                self.pool.add_1job(
                    self.bos.download,
                    url,
                    save_file
                )
                # self.bos.download(url, save_file)
        self.pool.stop()


if __name__ == '__main__':
    vt = Solution()
    in_path = R"D:\Desktop\1"
    out_path = R"D:\Desktop\2"
    vt.process(in_path=in_path, out_path=out_path)
