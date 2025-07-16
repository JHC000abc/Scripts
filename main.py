# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@contact: JHC000abc@gmail.com
@time: 2023/2/11 17:41 $
@desc:

"""
# import webbrowser
# from supports.Export.r_9774 import Solution
# from supports.Export.up_imgs import Solution
# from supports.match_files import Solution
# from supports.requirements.r_2013 import Solution
# from supports.requirements.r_2013 import Solution
# from supports.requirements.llm.l_149 import Solution
from sdk.tools.upload import Solution
# from sdk.tools.upload import Solution
# from supports.requirements.llm.l_75 import Solution

# from supports.split_excel import Solution
# from supports.Export.out.wangyi2 import Solution
# from supports.Export.merge_file_10000 import Solution
# from supports.Export.voice_split import Solution
# from supports.voice.r_9676 import Solution
# from tests.GoogleSearch.test import Solution
# from supports.mini_tools.req_9555.test_2 import Solution
# from tests.KS.test_download import Solution
# from supports.mini_tools.req_9555.test_2 import Solution
# from supports.img.r_9599 import Solution
# from sdk.tools.merge import Solution
# from tests.redduce_img_size import Solution
# from sdk.tools.download import Solutionr
# from supports.voice.add_project import Solution
# from supports.text_process.booker import Solution
# from supports.voice.add_project import Solution
from sdk.utils.util_times import TimeProcess
# 忽略 bos ssl 证书验证
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# # 适配Windows 系统出现 Lorem ipsum.txt 相关问题 降级
# pip install setuptools==58.0.4


Validity = 7
status_date = True
# 是否需要输入选项
single_in = True
single_out = True
single_other = False
single_thread = False

EXENAME = "r_2013"
time_stand = "2022-11-30 23:27:56"

print("******************程序启动*********************")
print("")
print("***************{}***************".format(EXENAME))
print("程序使用教程及常见问题: https://ku.baidu-int.com/d/5Oue5Z_nFefd2f 【程序运行后,自动启动默认浏览器打开使用教程】")


# try:
#     webbrowser.open("https://ku.baidu-int.com/d/5Oue5Z_nFefd2f")
# except BaseException:
#     print("默认浏览器自动启动失败，请手动复制上边的链接并用浏览器打开")


def normal_settings():
    """

    :return:
    """
    global thread_nums, e, in_path, save_path, base_split
    if single_thread:
        thread_nums = input("输入线程数:")
        if not thread_nums or int(thread_nums) <= 3:
            thread_nums = "5"
        e = Solution(thread_nums=int(thread_nums))
    else:
        e = Solution()
    if single_in:
        in_path = input("输入待处理文件所在的文件夹路径(路径下可以有多个文件同时处理):")
    else:
        in_path = ""
    if single_out:
        save_path = input("输入新文件保存路径(不要和输入路径在同一文件夹下):")
    else:
        save_path = ""
    if single_other:
        base_split = input("输入域名:")
        e.process(in_path=in_path, save_path=save_path, base_split=base_split)
    else:
        e.process(in_path=in_path, save_path=save_path)


if not status_date:
    time_now = TimeProcess().get_normal_date('%Y-%m-%d %H:%M:%S')
    diff_times = TimeProcess().get_precis_diff_times(time_stand, time_now)
    if diff_times[0] == 0 and diff_times[1] == 0 and diff_times[2] < Validity:
        if diff_times == Validity - 1:
            if diff_times[3] <= 12 and diff_times[4] < 60 and diff_times[-1] < 60:
                status_date = True
        else:
            status_date = True

    if not status_date:
        print("软件过期")
    else:
        normal_settings()
else:
    normal_settings()

print("\n")
input("文件夹下所有待处理文件处理完成,回车退出")
