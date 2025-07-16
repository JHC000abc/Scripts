#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: temp_supports.py
@time: 2023/6/20 21:57
@desc:
"""
import re
import math
import atexit
import random
from sdk.utils import util_file, util_folder, util_json, util_encrypt, util_log
from sdk.utils.util_decorate import DecorateMultiThread
from abc import ABCMeta, abstractmethod
from sdk.utils.util_compress import ZipProcess
from sdk.utils.util_excel import ExcelProcess
from sdk.utils.util_csv import CSV
from sdk.utils.util_jsonl import JSONL
from itertools import permutations
from sdk.utils.util_encrypt import EncryptProcess
from sdk.utils.util_times import TimeProcess

DM = DecorateMultiThread(50)


class IsSolution(object, metaclass=ABCMeta):
    """

    """

    def __init__(self):
        atexit.register(self.exit_handler)
        self.file = util_file.FileProcess()
        self.folder = util_folder.FolderProcess()
        self.json = util_json.JsonProcess()
        self.encrypt = util_encrypt.EncryptProcess()
        self.success_lis = []
        self.error_lis = []
        self.zip = ZipProcess()
        self.logger = util_log.MyLogger("logs").get_config()

        self.csv = CSV()
        self.jsonl = JSONL()
        self.excel = ExcelProcess()
        self.ep = EncryptProcess()
        self.time = TimeProcess()
        self.now = self.time.get_normal_date("%Y-%m-%d-%H-%M-%S")

    def exit_handler(self):
        """
        程序退出自动执行
        :return:
        """
        print("程序退出")

    def get_data_from_args(self, args, tag):
        """

        :param args:
        :param tag:
        :return:
        """
        return args["line"][args["headers"].index(tag)]

    def get_file(self, folder: str, remove_list=None, status=False):
        """

        :param folder:
        :return:
        """
        if remove_list is None:
            remove_list = [".DS_Store", "desktop.ini"]
        for args in self.folder.get_all_files(folder):
            file = args["file"]
            if args["name"] not in remove_list:
                if not status:
                    yield file
                else:
                    name = args["name"]
                    yield file, name

    def get_column(self, args: dict, key_lis: list) -> dict:
        """

        :param args:
        :param key_lis:
        :return:
        """
        headers = args["headers"]
        data = args["line"]
        num = args["num"]
        res = {}
        for key in key_lis:
            if headers.index(key) >= len(data):
                res[key] = ""
            else:
                res[key] = data[headers.index(key)]
        # res["num"] = num
        return res

    def get_url_list(self, args):
        """

        :param args:
        :return:
        """
        url_str = args["line"][args["headers"].index("url")]
        try:
            url_list = self.json.loads(url_str)
        except BaseException:
            url_list = [url_str]
        return url_list

    def get_answer_list(self, args, answer_list, un_condition=None):
        """

        :param args:
        :return:
        """
        if un_condition is None:
            un_condition = ["-", "是", "否", "{}", ""]
        answer_str = self.get_answer(args, answer_list=answer_list, un_condition=un_condition)
        if not answer_str.startswith("[answer error] "):
            answer_json = self.json.loads(answer_str)
            return answer_json["result"]
        else:
            raise ValueError("答案获取失败：{}".format(answer_str))

    def read_line(self, file: str, headers: list = None,
                  _id=False, spliter="\t", encoding="utf-8", mode="r"):
        """

        :param file:
        :param headers:
        :return:
        """
        for args in self.file.read_yield(
                file=file, headers=headers, spliter=spliter, encoding=encoding, mode=mode):
            if _id:
                id = args["line"][args["headers"].index("题目id")]
                if id == str(_id):
                    yield args
            else:
                yield args

    def read_line_col(self, file: str, header: list = None,
                      key_lis: list = None):
        """

        :param folder:
        :param header:
        :param key_lis:
        :return:
        """
        for args in self.file.read_yield(file=file, headers=header):
            data_json = self.get_column(args, key_lis)
            yield data_json

    def get_answer(self, args: dict, answer_list=None, un_condition=None):
        """
        取答案
        :param args:FileProcess返回的dict
        :param answer_list:取答案顺序
        :return:
        """
        if answer_list is None:
            answer_list = ["验收答案", "拟合答案", "质检答案"]
        if un_condition is None:
            un_condition = ["-", "是", "否", "{}", ""]
        for key in answer_list:
            if key in args["headers"]:
                answer = args["line"][args["headers"].index(key)]
                if re.match(r'^\d+:{"', answer):
                    answer = ":".join(answer.split(":")[1:])
                if answer not in un_condition:
                    try:
                        if self.json.loads(answer)["result"][0].get("elements"):
                            return answer
                        else:
                            # print(args["num"], self.get_one_from_yield_args(args, "url"), key, answer)
                            continue
                    except:
                        return answer

        return None

    def calculate_sort_points(self, points, rotation=1):
        """
        计算并重新排序四边形四个顶点坐标 默认以y计算
        :param points:
        :param rotation:
        :return:
        """
        if rotation < 0:
            min_y_2 = sorted(points, key=lambda d: d['y'])[:2]

            left_upper, right_upper = sorted(min_y_2, key=lambda d: d['x'])

            max_y_2 = sorted(points, key=lambda d: d['y'])[2:]
            left_down, right_down = sorted(max_y_2, key=lambda d: d['x'])
        else:
            min_y_2 = sorted(points, key=lambda d: d['x'])[:2]

            left_upper, left_down = sorted(min_y_2, key=lambda d: d['y'])

            max_y_2 = sorted(points, key=lambda d: d['x'])[2:]
            right_upper, right_down = sorted(max_y_2, key=lambda d: d['y'])
        return [left_upper, right_upper, right_down, left_down]

    def calculate_points_rotation(self, points, point, ratation):
        """
        已知 左上 右下，围绕旋转的点坐标，旋转角度
        :param points: [{"x":"","y":""},{"x":"","y":""}]
        :param point: [1,2]
        :param ratation: -45
        :return:
        """

        def rotate_point(x, y, cx, cy, angle):
            # 角度转弧度
            angle_rad = math.radians(angle)

            # 计算旋转矩阵的分量
            cos_angle = math.cos(angle_rad)
            sin_angle = math.sin(angle_rad)

            # 将点 (x, y) 相对于中心点 (cx, cy) 旋转
            x_translated = x - cx
            y_translated = y - cy

            x_rotated = x_translated * cos_angle - y_translated * sin_angle
            y_rotated = x_translated * sin_angle + y_translated * cos_angle

            # 重新平移回原始位置
            # return (x_rotated + cx, y_rotated + cy)
            return {"x": x_rotated + cx, "y": y_rotated + cy}

        def rotate_rectangle(x1, y1, x2, y2, cx, cy, angle):
            # 计算长方形的四个角点
            points = [
                (x1, y1),  # 左上角
                (x2, y1),  # 右上角
                (x2, y2),  # 右下角
                (x1, y2)  # 左下角
            ]

            # 旋转四个角点
            rotated_points = [rotate_point(x, y, cx, cy, angle) for (x, y) in points]

            # 返回旋转后的四个角点，按左上、右上、右下、左下的顺序
            return self.calculate_sort_points(rotated_points, ratation)

        x1, y1, x2, y2 = points[0]["x"], points[0]["y"], points[1]["x"], points[1]["y"]
        return rotate_rectangle(x1, y1, x2, y2, point[0], point[1], ratation)

    def check_elements(self, answer: dict, status=True):
        """

        :param answer:
        :param status:
        :return:
        """
        if status:
            return bool(answer["result"][0].get("elements"))
        else:
            return answer["result"][0].get("elements")

    def parse_answer(self, answer, model="results"):
        """
        解析答案
        :param answer:
        :param model: results/elements/element
        :return:
        """
        if isinstance(answer, str):
            json_answer = self.json.loads(answer)
        else:
            json_answer = answer
        if json_answer.get("result"):
            result = json_answer["result"]
            if model == "results":
                yield result
                return
            else:
                for res in result:
                    if model == "elements":
                        yield res["elements"]
                        continue
                    else:
                        for element in res["elements"]:
                            if model == "element":
                                yield element
                                continue
        else:
            if model == "results":
                yield ["多帧数据，不存在result"]
                return
            else:
                if model == "elements":
                    yield json_answer["elements"]
                else:
                    for element in json_answer["elements"]:
                        if model == "element":
                            yield element
                            continue

    def calculate_center_points(self, points):
        """

        :param points: [[382.4593864251, 678.1950511312], [534.1310867377, 760.9852805595]]
        :return:
        """
        x_center = (points[-1][0] + points[0][0]) / 2
        y_center = (points[-1][-1] + points[0][-1]) / 2
        width = points[-1][0] - points[0][0]
        height = points[-1][-1] - points[0][-1]

        return x_center, y_center, width, height

    def tran_points_format(self, points):
        """

        :param points:
        :return:
        """
        new_points = []
        for i in points:
            if isinstance(i, list):
                new_points.append({"x": i[0], "y": i[1]})
            if isinstance(i, dict):
                new_points.append(list(i.values()))
        return new_points

    def get_points_new(self, points: list, mode=None, format=False):
        """
        处理 points
        points = [{"x":658.186,"y":265.4},{"x":554.35,"y":81.5},{"x":593.1,"y":84.6,"z":1.5}]
        points = [[658.17, 265.4,1.888], [554.3, 81.59], [593.89, 84.6929]]
        :param points:
        :param mode: 1:完全展开 其它保留原格式
        :param format: 格式化成int
        :return:
        """

        def process_item(item):
            if isinstance(item, dict):
                item = item.values()
            return [int(value) if format else value for value in item]

        processed_points = [process_item(point) for point in points]

        if mode == 1:
            processed_points = [value for sublist in processed_points for value in sublist]

        return processed_points

    def get_points(self, points: dict, mode=0, format=False):
        """
        获取points（兼容旧版，2024新脚本中 已废弃）
        :param points:
        :param mode:0:[[,],[,]] 2:[,,,,]
        :return:
        """
        try:
            if format:
                point_list = [[int(i["x"]), int(i["y"])] for i in points]
            else:
                point_list = [[i["x"], i["y"]] for i in points]
        except BaseException:
            pass
        if mode == 0:
            # 默认状况返回格式化后的数据
            # [[,],[,]]
            return point_list
        elif mode == -1:
            # 全展开 [,,,,,] 带x,y
            lis = []
            lis.extend(j for i in point_list for j in i)
            return lis
        elif mode == 3:
            # [[134, 409], [195, 468]] 全展开 [,,,,] 不带x,y
            return [j for i in points for j in i]
        elif mode == 2:
            return [j for i in point_list for j in i]

    def points_change_two_four(self, points, mode=0):
        """

        :param points:
        :param mode:
        :return:
        """
        if mode == 0:
            return [
                [points[0]["x"], points[0]["y"]],
                [points[-1]["x"], points[0]["y"]],
                [points[-1]["x"], points[-1]["y"]],
                [points[0]["x"], points[-1]["y"]]
            ]
        else:
            return [
                {"x": points[0]["x"], "y": points[0]["y"]},
                {"x": points[-1]["x"], "y": points[0]["y"]},
                {"x": points[-1]["x"], "y": points[-1]["y"]},
                {"x": points[0]["x"], "y": points[-1]["y"]},
            ]

    def get_points_from_two_four(self, points_list, mode=0):

        """

        :param points_list:
        :param mode: 0->list ; 1->dict
        :return:
        """

        x1, y1 = points_list[0]
        x3, y3 = points_list[-1]
        x2, y2 = x3, y1
        x4, y4 = x1, y3
        if mode == 0:
            return [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        elif mode == 1:
            return [{"x": x1, "y": y1}, {"x": x2, "y": y2}, {"x": x3, "y": y3}, {"x": x4, "y": y4}]

    def save_result(self, file: str, data, headers: list = None, mode="w", extra: dict = None, spliter="\t"):
        """

        :param file:
        :param data:
        :param headers:
        :param mode:
        :param extra: save_folder:待压缩文件所在目录,zip_file:生成的.zip文件路径
        :return:
        """
        if len(file) > 260:
            raise ValueError("文件路径过长")
        with open(file, mode=mode, encoding="utf-8") as fp:
            if headers:
                fp.write("{}\n".format("\t".join(headers)))
            if isinstance(data, str):
                fp.write(data)
            if isinstance(data, list):
                for li in data:
                    if isinstance(li, list):
                        # print("li",li)
                        fp.write("{}\n".format(spliter.join(li)))
                    else:
                        fp.write("{}\n".format(li))
            if isinstance(data, dict):
                fp.write(self.json.dumps(data))

            fp.flush()

        if extra:
            save_folder = extra["save_folder"]
            zip_file = extra["zip_file"]
            self.zip.zip_files(save_folder, zip_file)

    def make_out_path(self, base_path: str, path_list=None) -> str:
        """
        生成输出路径
        :param base_path: 根路径
        :param path_list: 根路径后拼接的路径列表
        :return: 完整的输出路径
        """
        if path_list is None:
            path_list = ["results"]
        full_path_list = [base_path] + path_list
        _save_path = self.folder.merge_path(full_path_list)
        self.folder.create_folder(_save_path)
        return _save_path

    def calculate_width_height_bbox(self, points):
        """
        计算框宽高
        :param points:
        :return:
        """
        width = points[1][0] - points[0][0]
        height = points[-1][-1] - points[0][1]
        return width, height

    def make_new_bos_url(self, uid=None, folder=None, name=None,
                         url=None, cut=4, folder_cut=3):
        """

        :param uid: 唯一标识
        :param folder:
        :param name:
        :param url:
        :param cut: 原始url保留长度
        :param folder_cut: 原始url保留层级（从后往前）
        :return:
        """
        if not uid:
            uid = self.ep.make_uuid()
        if not name:
            name = self.folder.split_path(url)[-1]
        if not folder:
            folder = "/".join(self.folder.split_path(url)
                              [-(folder_cut + 1):-1])
        if not url:
            url = "https://bj.bcebos.com/collection-data/jiaohaicheng/{}/{}/{}".format(
                uid, folder, name)
        else:
            url = "/".join(self.folder.split_path(url)[:cut]) + "/{}/{}/{}".format(
                uid, folder, name
            )
        return url

    def get_random_sample(self, num_list, _len=2, size=0):
        """
        random.sample(numbers, 5)
        :param num_list:
        :param _len:
        :param _size:
        :return:
        """
        for i in range(size):
            yield random.sample(num_list, _len)

    def get_permutations(self, num_list, _len=2, size=0):
        """
        生成指定数组的全排列
        :param num_list:
        :return:
        """
        seen_permutations = set()
        for perm in permutations(num_list, _len):
            perm_tuple = tuple(sorted(perm))
            if perm_tuple not in seen_permutations:
                seen_permutations.add(perm_tuple)
                if size > 0:
                    yield perm_tuple
                    size -= 1
                else:
                    break

    def get_one_from_yield_args(self, args, key):
        """

        :param args:
        :param key:
        :return:
        """
        res = "" if args["line"][args["headers"].index(key)] is None else args["line"][args["headers"].index(key)]
        res = res.replace(" ", "")
        return res

    def muti_thread_function(self, *args, **kwargs):
        """
        多线程处理函数
        :param args:
        :param kwargs:
        :return:
        """

    @abstractmethod
    def process(self, **kwargs):
        """
        处理流程
        """
