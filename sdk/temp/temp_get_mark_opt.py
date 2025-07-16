#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: temp_get_mark_opt.py
@time: 2023/6/12 20:14
@desc:

"""
import traceback
from sdk.utils.util_json import JsonProcess
from sdk.utils.util_file import FileProcess
from sdk.utils.util_img import MarkProcess


class Mark(MarkProcess):
    """
    Mark
    """

    def __init__(self):
        super(Mark, self).__init__()
        self.json = JsonProcess()
        self.file = FileProcess()

    def _init_mark_normal_process(self, file, answer, save_file, color_map=None):
        """
        常规标注处理流程
        1.初始化参数 2.获取标注参数 3.读取原始图片 4.标框 5.标文字 6.保存标注好的图片
        :param file:
        :param answer:
        :param save_file:
        :param color_map:
        :return:
        """
        try:
            map = self.make_map(data=answer)
            img = self.read_image(file)
            img = self.mark(img, map, color_map)
            img = self.add_words(img, map)
            self.save_image(img, save_file)
        except Exception as e:
            msg = traceback.print_exc()
            print(e.__traceback__.tb_lineno, e)
            print("[except _init_mark_normal_process]", msg)
            mark_status = False
        else:
            mark_status = True
            msg = ""
        finally:
            return {
                "mark_data": self.json.dumps(map, indent=None),
                "origin_file": file,
                "mark_file": save_file,
                "mark_status": mark_status,
                "msg": msg
            }

    def make_map(self, file=None, data=None):
        """
        从不同源 读取数据生成 map
        :param file: txt
        :param data: excel
        :return:
        """
        map = {}
        if file:
            for args in self.file.read_yield(file):
                data = args["data"]
                headers = args["headers"]
                num = args["num"]
                insert_args = {
                    "opt": [
                        [int(i["x"]), int(i["y"])]
                        if len(data[headers.index("points")]) != 1
                        else [int(i["x"]), int(i["y"]), 1]
                        for i in data[headers.index("points")]
                    ],
                    "text": data[headers.index("text")],
                }
                map[str(num)] = insert_args
        if data:
            json_data = self.json.loads(data)
            if json_data.get("result"):
                for result in json_data["result"]:
                    for index, element in enumerate(result["elements"]):
                        insert_args = {
                            "opt": [
                                [int(i["x"]), int(i["y"])]
                                if len(element["points"]) != 1
                                else [int(i["x"]), int(i["y"]), 1]
                                for i in element["points"]
                            ],
                            "text": element["text"]
                        }
                        num = index + 1
                        map[str(num)] = insert_args
            else:
                for index, element in enumerate(json_data["elements"]):
                    insert_args = {
                        "opt": [
                            [int(i["x"]), int(i["y"])] if len(element["points"]) != 1 else [int(i["x"]), int(i["y"]), 1]
                            for i in element["points"]],
                        "text": element["text"]
                    }
                    num = index + 1
                    map[str(num)] = insert_args

        return map

    def get_answer(self, args: dict, answer_list=None):
        """
        取答案
        :param args:FileProcess返回的dict
        :param answer_list:取答案顺序
        :return:
        """
        if answer_list is None:
            answer_list = ["验收答案", "拟合答案", "质检答案"]
        num = args["num"]
        un_condition = ["-", "是"]
        for key in answer_list:
            answer = args["line"][args["headers"].index(key)]
            if answer not in un_condition:
                return answer
        return "[answer error] line num:{} answer:{}".format(num, answer)
