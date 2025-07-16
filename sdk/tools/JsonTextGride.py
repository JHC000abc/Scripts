# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author  : v_jiaohaicheng@baidu.com
@des     :
    Json TextGrid 互转
"""
import re
import json
import os
from sdk.utils.util_file import FileProcess


class Tran(object):
    """

    """

    def __init__(self):
        self.file = FileProcess()
        self.fill_single = True

    def get_column(self, args: dict, key_lis: list):
        """

        :param args:
        :param key_lis:
        :return:
        """
        headers = args["headers"]
        data = args["line"]
        res = {}
        for key in key_lis:
            res[key] = data[headers.index(key)]
        return res

    def save_result(self, file, data):
        """

        :param file:
        :param data:
        :return:
        """
        with open(file, "w", encoding="utf-8")as fp:
            fp.write(data)

    def get_answer(self, args: dict, answer_list: list = [
                   "验收答案", "拟合答案", "质检答案"]):
        """
        取答案
        :param args:FileProcess返回的dict
        :param answer_list:取答案顺序
        :return:
        """
        un_condition = ["-", "是", ""]
        for key in answer_list:
            answer = args["data"][args["headers"].index(key)]
            if answer not in un_condition:
                return answer
        num = args["num"]
        return "第 {} 行 答案为:{}".format(num, answer)

    def jsontrantext(self, file, save_path, answer_list=["最终答案"]):
        """

        :param file:
        :param save_path:
        :return:
        """
        os.makedirs(save_path, exist_ok=True)
        error_log_lis = []

        def _get_main(audioDuration, size, name):
            return """File type = "ooTextFile"\nObject class = "TextGrid"\n\nxmin = 0\nxmax = {}\ntiers? <exists>\nsize = 1\nitem []:\n\titem [1]:\n\t\tclass = "IntervalTier"\n \t\tname = "{}"\n \t\txmin = 0\n \t\txmax = {}\n\t\tintervals: size = {}\n""".format(
                audioDuration, name, audioDuration, size)

        def _get_items(num, xmin, xmax, text):
            return """\t\tintervals [{}]:\n\t\t\txmin = {}\n\t\t\txmax = {}\n\t\t\ttext = \"{}\"""".format(
                num, xmin, xmax, text)

        # data_json = self.file.read_json(file)
        for args in self.file.read_yield(file):
            answer = self.get_answer(args, answer_list)
            # data_map = self.get_col(args,["拟合答案"])
            # answer = data_map["拟合答案"]
            if not answer.startswith("第"):
                data_json = json.loads(answer)
                name = data_json["audioFileName"].split("/")[-1]
                audioDuration = data_json["audioDuration"]
                records = data_json["records"]
                item_lis = []
                history_head = [0, 0]
                num = 0
                for args in records:
                    _time = args["time"]
                    xmin = _time["begin"]
                    xmax = _time["end"]
                    # 补充开头空白和中间空白
                    if self.fill_single:
                        if xmin != history_head[-1]:
                            num += 1
                            _item = _get_items(num, history_head[-1], xmin, "")
                            item_lis.append(_item)
                            history_head = [history_head[-1], xmin]
                            del _item

                    num += 1
                    text = args["content"]
                    _item = _get_items(num, xmin, xmax, text)
                    history_head = [xmin, xmax]
                    item_lis.append(_item)
                    del _item

                # 补充结尾空白
                if self.fill_single:
                    if history_head[-1] < audioDuration:
                        num += 1
                        _item = _get_items(
                            num, history_head[-1], audioDuration, "")
                        item_lis.append(_item)
                        del _item

                size = len(item_lis)
                main_args = _get_main(audioDuration, size, name)
                main_args += "\n".join(item_lis)
                _save_path = os.path.join(save_path, "data")
                os.makedirs(_save_path, exist_ok=True)
                save_file = os.path.join(
                    _save_path, "{}.TxtGrid".format(name))
                self.save_result(save_file, main_args)
                del main_args
                print("成功保存:{}".format(save_file))
            else:
                error_msg = "文件:{} {}".format(file, answer)
                print("[答案存在错误]:", error_msg)
                error_log_lis.append(error_msg)

        if error_log_lis:
            print("")
            print("|---------------------------------------------|")
            print("| >>>----请检查 error.txt 文件中的错误内容----<<< |")
            print("|---------------------------------------------|")
            print("")
            self.save_result("error.txt", "\n".join(error_log_lis))

    def texttranjson(self, file, encoding="utf-8"):
        map = {}
        item_id = 0
        _temp_map = {}
        with open(file, "r", encoding=encoding)as fp:
            for i in fp:
                line = i.strip("\n")
                if line.startswith("File type = "):
                    map["file_type"] = re.findall('File type = "(.*?)"', line)[0]
                if line.startswith("Object class = "):
                    map["object_class"] = re.findall('Object class = "(.*?)"', line)[0]
                if line.startswith("xmin = "):
                    map["xmin"] = int(re.findall('xmin \\= (.*)', line)[0])
                if line.startswith("xmax = "):
                    map["xmax"] = float(re.findall('xmax \\= (.*)', line)[0])
                if line.startswith("size = "):
                    map["size"] = int(re.findall('size \\= (.*)', line)[0])

                if re.match("    item \\[\\d+\\]\\:", line):
                    item_id += 1
                    map[item_id] = {}

                if line.startswith('        class = "'):
                    map[item_id]["class"] = re.findall('        class = "(.*?)"', line)[0]

                if line.startswith('        name = "'):
                    map[item_id]["name"] = re.findall('        name = "(.*?)"', line)[0]

                if line.startswith('        xmin = '):
                    map[item_id]["xmin"] = int(re.findall('        xmin \\= (.*)', line)[0])

                if line.startswith('        xmax = '):
                    map[item_id]["xmax"] = float(re.findall('        xmax \\= (.*)', line)[0])

                if line.startswith('        intervals: size = '):
                    map[item_id]["intervals_size"] = int(re.findall('        intervals: size \\= (.*)', line)[0])

                if line.startswith('        intervals ['):
                    # print(_temp_map)
                    if _temp_map:
                        if map[item_id].get("intervals_list") is None:
                            map[item_id]["intervals_list"] = _temp_map
                        else:
                            map[item_id]["intervals_list"].update(_temp_map)
                    _temp_map = {}

                    intervals_id = int(re.findall('        intervals \\[(.*)\\]', line)[0])
                    _temp_map[intervals_id] = {}

                if line.startswith('            xmin = '):
                    _x_min = re.findall('            xmin = (.*)', line)[0]
                    x_min = float(_x_min) if "." in _x_min else int(_x_min)
                    _temp_map[intervals_id]["xmin"] = x_min

                if line.startswith('            xmax = '):
                    _x_max = re.findall('            xmax = (.*)', line)[0]
                    x_max = float(_x_max) if "." in _x_max else int(_x_max)
                    _temp_map[intervals_id]["xmax"] = x_max

                if line.startswith('            text = '):
                    _text = re.findall('            text = \"(.*?)\"', line)
                    if _text:
                        _text = _text[0]
                    _temp_map[intervals_id]["text"] = _text

            # print(map)
            return map


if __name__ == '__main__':
    t = Tran()
    # t.jsontrantext(
    #     R"D:\Desktop\1\平台导出8504912.txt",
    #     R"D:\Desktop\2")
    map = t.texttranjson(R"D:\Desktop\测试数据\清梦对话QMDH2397-QMDH2844_0.92h\TextGrid\QMDH2397.TextGrid")
    print(map)
