# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: upload.py
@time: 2025/3/14 18:45 
@desc: 

"""
import os
from datetime import datetime
from sdk.temp.temp_supports import IsSolution, DM
from sdk.utils.util_class import PathParser
from sdk.utils.util_bos import BosAkSk
from sdk.utils.util_encrypt import EncryptProcess


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
        self.bos = BosAkSk()
        self.ep = EncryptProcess()
        DM.callback = self.callback

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
    def multi_upload(self, url, file, upload_status):
        """

        :param url:
        :param file:
        :param upload_status:
        :return:
        """
        return self.bos.upload(url, file, int(upload_status)), url, file

    def callback(self, status, result):
        """
        回调函数
        :param status:
        :param result:
        :return:
        """
        up_result, url, file = result
        obj = PathParser(file)
        print("--->obj.name", obj.name)
        if status:
            # self.success_lis.append([file, url])
            out = {"result": [], "url": f"{url}"}
            out = self.json.dumps(out, indent=None)

            self.success_lis.append([obj.name, out])
        else:
            # self.success_lis.append([file, ""])
            self.success_lis.append([obj.name, ""])

    def process(self, **kwargs):
        """
        处理文件

        :param kwargs: 关键字参数
        :return: 无返回值
        """
        self.in_path = kwargs["in_path"]
        self.save_path = kwargs["save_path"]
        self.folder.create_folder(self.save_path)
        print("建议批量上传前先挑选少量数据进行测试 上传模式=1有时候不好使 5M为分界线区分大小文件\n")
        mode = input("请输入链接转换类型：0:仅平台可见 1：全部可见(默认)")
        if mode not in ("0", "1"):
            raise ValueError("链接转换类型 must in 0 or 1")
        upload_status = input("请输入上传模式：0：普通模式（小文件） 1：分块上传（大文件）")
        if upload_status not in ("0", "1"):
            raise ValueError("上传模式 must in 0 or 1")
        for file, file_name in self.get_file(self.in_path, status=True):
            print(file, file_name)
            obj = PathParser(file)
            path_tail = obj.header.split(os.sep)[-1]
            now_time = datetime.now().strftime("%Y%m%d%H")
            if mode == "0":
                bos_base_path = "https://bj.bcebos.com/collection-data/jiaohaicheng/work/company/"
            else:
                bos_base_path = "https://bj.bcebos.com/petite-mark/public_read/vipshop/"

            bos_url = f"{bos_base_path}{now_time}/{path_tail}/{self.ep.make_uuid(1)}_{self.ep.make_md5(data=obj.name)}.{obj.tail}"
            print("bos_url", bos_url)
            self.multi_upload(bos_url, file, upload_status)

        DM.close_pool()
        self.excel.write(self.folder.merge_path([self.save_path, "上传结果.xlsx"]), [self.success_lis],
                         [["local", "bos"]])


if __name__ == '__main__':
    in_path = R"D:\Project\Python\baidu\crowdtest\collection-script\CR\tests\dp\imgs"
    save_path = R"D:\Desktop\2\upload"
    e = Solution()
    e.process(in_path=in_path, save_path=save_path)
