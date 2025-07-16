#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: util_img.py
@time: 2023/5/28 14:26
@desc:
"""
import os
import json
import cv2 as cv
import numpy as np
import copy
from io import BytesIO
import PIL.JpegImagePlugin
from PIL import ImageFont, Image, ImageDraw
from sdk.utils.util_file import FileProcess
from sdk.utils.util_folder import FolderProcess


class MarkProcess(object):
    """
    图像标注转化处理类
    """

    def __init__(self):
        # 是否标注文字
        self.TEXT = True
        # 是否标注文字序号
        self.INDEX = False
        # 是否标注后缀
        self.TEXT_TAIL = False
        # 标注文本后缀
        self.text_tail = "中文"
        # 是否标注线，框
        self.MARK = True
        # 标注文字大小
        self.SIZE = 25
        # 文字位置 True:左上，False:右下
        self.WORD_POS = False

        # 标注框颜色
        self.COLOR = (255, 0, 0)
        # 标注字颜色
        self.TXT_COLOR = "red"
        # 标注线粗
        self.THICKNESS = 0
        # 圆圈线粗
        self.THICKNESS_CIRCLE = -1
        # 是否闭合 默认闭合
        self.isClosed = True
        # 绘制 框/线 0:线 1:框
        self.LINE = 1
        # # 标注线类型
        # self.LINE_TYPE = cv.LINE_8
        # self.LINE_TYPE = cv.LINE_4
        self.LINE_TYPE = cv.LINE_AA

        # 加载文本处理类(自定义的)
        self.file = FileProcess()
        # 标注字体格式
        # self.Font = "plugins/SourceHanSerifSC-Bold.otf"
        self.folder = FolderProcess()

        if not os.path.exists("SourceHanSerifSC-Bold.otf"):
            path = self.folder.split_path(os.path.realpath(__file__), "sdk")
            self.Font = self.folder.merge_path(
                [path[0], "sdk", "plugins", "SourceHanSerifSC-Bold.otf"])
        else:
            self.Font = "SourceHanSerifSC-Bold.otf"

        # 印地语
        # self.Font = R"C:\Windows\Fonts\NirmalaS.ttf"
        # 泰语
        # self.Font = R"C:\Windows\Fonts\tahoma.ttf"

    def get_copy(self, args: [dict, list, str, int, tuple, json]) -> copy:
        """
        返回拷贝
        :param args:
        :return:
        """
        return copy.deepcopy(args)

    def read_image(self, file: str, mode: int = 1) -> np:
        """
        读取图片，支持中文路径
        :param file:
        :return:
        """
        if mode == 1:
            return np.asarray(Image.open(file))
        else:
            return Image.open(file)

    def tran_type(self, img):
        """
        格式转换 np 与 PI:
        :param img:
        :return:
        """
        if isinstance(img, PIL.Image.Image):
            return np.asarray(Image.fromarray(np.uint8(img)))
        elif isinstance(img, np.ndarray):
            return Image.fromarray(img)

    def make_mix_img(self, width=120, height=35, color=0):
        """

        :param width:
        :param height:
        :param color:
        :return:
        """
        return Image.new(mode='RGB', size=(width, height), color=color)

    def make_new_img(self, img: np.ndarray, mode: int = -1):
        """
        创建一张和给定图一样尺寸的纯黑、纯白图
        :param img:
        :param mode:-1:black 1:white
        :return:
        """
        if mode == -1:
            img = np.zeros_like(img)
        elif mode == 1:
            img = np.ones_like(img) * 255
        else:
            raise ValueError("unsupport mode:{}".format(mode))
        return img

    def tran_gray(self, img: np) -> np:
        """
        转灰度图
        :param img:
        :return:
        """
        return cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    def tran_binary(self, img: np) -> np:
        """
        二值化
        :param img:
        :return:
        """
        if not self.check_is_gray(img):
            img = self.tran_gray(img)
        ret2, img = cv.threshold(
            img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        return img

    def check_is_gray(self, img: np) -> bool:
        """
        判断图像是否为灰度图
        :param img:
        :return:
        """
        img = Image.fromarray(np.uint8(img))
        return img.mode == "L" or img.mode == "LA"

    def get_img_shape(self, img: np) -> tuple:
        """
        获取图像 shape
        :param img:
        :return:(h,w,b)
        """
        return img.shape

    def resize(self, img: np,
               newsize: tuple[int, int] = None, rate: int = None) -> np:
        """
        调整图像大小
        :param img:
        :param size:
        :return:
        """
        if rate:
            origin_h, origin_w, byway = self.get_img_shape(img)
            if rate >= 0:
                new_h = int(origin_h * rate)
                new_w = int(origin_w * rate)
            else:
                new_h = int(origin_h / abs(rate))
                new_w = int(origin_w / abs(rate))
            newsize = (new_h, new_w)

        return np.asarray(Image.fromarray(np.uint8(img)).resize(newsize))

    def transpose_image(
            self, img: [np.ndarray, PIL.JpegImagePlugin.JpegImageFile], key: int = 0) -> np:
        """
        旋转,逆时针
        :param img:
        :param key:
        :return:
        """
        if isinstance(img, np.ndarray):
            return np.asarray(Image.fromarray(np.uint8(img)).rotate(key))
        if isinstance(img, PIL.JpegImagePlugin.JpegImageFile):
            return img.rotate(key)
        else:
            raise ValueError("type error {}".format(type(img)))

    def mirror(self, img: np, key: int):
        """
        镜像
        :param img:
        :param key:0:垂直翻转,1:水平翻转
        :return:
        """
        return cv.flip(img, key)

    def check_img_mode(self, img: np):
        """
        检查图片是RGB/IR(L)
        :param img:
        :return:
        """
        return self.tran_type(img).mode

    def save_image(self, img: np, file: str, mode="RGB"):
        """
        保存图片
        :param img:
        :param file:
        :param mode: IR 存储的img也必须是IR
        :return:
        """
        if mode == "RGB":
            cv.imencode(
                ".{}".format(self.file.get_file_tail(file)), cv.cvtColor(
                    img, cv.COLOR_RGB2BGR))[1].tofile(file)
        elif mode == "IR":
            cv.imencode(
                ".{}".format(self.file.get_file_tail(file)), img)[1].tofile(file)
        else:
            raise ValueError("error mode")

    def add_word(self, img: PIL.JpegImagePlugin.JpegImageFile,
                 index: int, text: str, color=0, size=30) -> np:
        """
        绘制文字
        :param img:
        :param opt:
        :param text:
        :return:
        """
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(self.Font, size=size)
        draw.text((10 + index * 30, -2), text, color, font=font)

    def add_words(self, img: np, map: dict) -> np:
        """
        添加文字 支持中，英文
        :param img:
        :param map:{
            "index":{
                "text":"",
                "opt":[]
            }
        }
        :return:
        """
        font = ImageFont.truetype(self.Font, size=self.SIZE)
        for index, value in map.items():
            img = Image.fromarray(np.uint8(img))
            draw = ImageDraw.Draw(img)
            min_x, max_y = self.get_m_opt(value["opt"])

            if self.WORD_POS:
                xy = min_x
            else:
                xy = max_y

            if not self.TEXT:
                value["text"] = ""

            if self.INDEX:
                text = "{}.{}".format(int(index) + 1, value["text"])
                # 去掉 .
                if not self.TEXT:
                    text = text[:-1]
            else:
                text = value["text"]
            # 在只标注索引情况下，不显示后缀的标注
            if self.TEXT:
                if self.TEXT_TAIL:
                    text = "{}_{}".format(text, self.text_tail)
            draw.text(
                xy=xy,
                text=text,
                font=font,
                fill=self.TXT_COLOR,
            )

            img = cv.cvtColor(np.asarray(img), cv.COLOR_RGB2RGBA)

        return img

    def get_m_opt(self, list: list) -> tuple[list, list]:
        """
        获取 右上角坐标，左下角坐标 附带偏移量
        :param list:
        :return:
        """
        min_x = [100000000, 100000000]
        max_y = [0, 0]
        for args in list:
            # 赋值时复制个副本操作，避免下边计算偏移量时影响原值
            if args[0] < min_x[0]:
                min_x = args[::]
            if args[1] > max_y[1]:
                max_y = args[::]
        # 计算偏移量
        min_x[1] = min_x[1] - self.SIZE - 5
        max_y[1] = max_y[1] - self.SIZE - 5

        return (min_x, max_y)

    def mark(self, img: np, map: dict, color_map=None) -> np:
        """
        添加 框、线、圆
        :param img:
        :param map:
        :param color_map: color_map = {
            "地图": (255, 255, 0),
            "枪械": (144, 238, 144),
            "技能": (255, 0, 0),
            "方向": (0, 255, 0),
            "工具": (255, 193, 37),
            "方向辅助": (0, 0, 0),

        }
        :return:
        """

        if self.MARK:
            for index, value in map.items():
                single = False
                args = value["opt"]
                # 画矩形
                if len(args) == 2:
                    if self.LINE == 1:
                        cv.rectangle(
                            img=img,
                            pt1=tuple(args[0]),
                            pt2=tuple(args[1]),
                            color=color_map.get(value["text"]) if color_map else self.COLOR,
                            thickness=self.THICKNESS,
                            lineType=self.LINE_TYPE,
                        )
                        single = True
                # 画圆
                if len(args) == 1:
                    cv.circle(img=img,
                              center=(args[0][0], args[0][1]),
                              radius=args[0][-1],
                              color=color_map.get(value["text"]) if color_map else self.COLOR,
                              thickness=self.THICKNESS_CIRCLE,
                              lineType=self.LINE_TYPE
                              )
                    single = True

                if single:
                    continue
                img = cv.polylines(
                    img=img,
                    pts=[np.array(args, dtype=np.int32)],
                    isClosed=self.isClosed,
                    color=color_map.get(value["text"]) if color_map else self.COLOR,
                    thickness=self.THICKNESS,
                    lineType=self.LINE_TYPE,

                )

        return img

    def fill_area(self, img, opt, color=(255, 255, 255)):
        """
        区域填充色彩
        :param img:
        :param opt:
        :param color:
        :return:
        """
        img = cv.fillPoly(img, np.array([opt], dtype=np.int32), color=color)
        return img

    def add_mosaic(self, img: np, opt: list[[int, int], [
        int, int]], neighbor: int = 5, debug=False) -> np:
        """
        添加马赛克
        :param img:
        :param opt:[左上，右下]
        :param neighbor:
        :param debug:调试模式 输出的是红框非马赛克
        :return:
        """

        if debug:
            cv.rectangle(
                img=img,
                pt1=tuple(opt[0]),
                pt2=tuple(opt[1]),
                color=self.COLOR,
                thickness=self.THICKNESS,
                lineType=self.LINE_TYPE,
            )
        else:
            fh, fw, fb = self.get_img_shape(img)
            x, y = opt[0]
            w, h = opt[1][0] - opt[0][0], opt[1][1] - opt[0][1]
            if (y + h > fh) or (x + w > fw):
                pass
            else:
                for i in range(0, h - neighbor, neighbor):
                    for j in range(0, w - neighbor, neighbor):
                        rect = [j + x, i + y, neighbor, neighbor]
                        color = tuple(img[i + y][j + x].tolist())
                        left_up = (rect[0], rect[1])
                        right_down = (
                            rect[0] + neighbor - 1,
                            rect[1] + neighbor - 1)
                        img = cv.rectangle(img, left_up, right_down, color, -1)

        return img

    def cut_img(self, img: np, opt: list[[int, int], [int, int]]) -> np:
        """
        裁切图片
        :param img:
        :param opt:([左上]，[右下])
        :return:
        """

        return img[opt[0][1]:opt[1][1], opt[0][0]:opt[1][0]]

    def change_light_contrast(
            self, img: np, light: int = None, contrast: float = None) -> np:
        """
        调整亮度 对比度
        :param img:
        :param light:(-250,250)
        :param contrast:(0,1.5)
        :return:
        """
        if light:
            blank = np.zeros(img.shape, img.dtype)
            img = cv.addWeighted(img, 1, blank, 0, light)
        if contrast:
            img = cv.convertScaleAbs(img, contrast, contrast * 10)

        return img

    def get_img_date(self, file):
        """

        :param img_file:
        :return:
        """
        image_file = open(file, 'rb')
        image_data = BytesIO(image_file.read())
        image_file.close()
        return image_data

    def merge_images(self, files, save_file, col=1):
        """

        :param files:
        :param save_file:
        :param mode:
        :return:
        """
        if col <= 0:
            col = 1
        if len(files) <= 1:
            raise ValueError("files len must > 1")
        images = [Image.open(img_file) for img_file in files]
        widths, heights = zip(*(img.size for img in images))

        total_width = sum(widths)
        max_width = max(widths)
        max_height = max(heights)
        _col = len(files) / col
        _col = int(_col) if _col == int(_col) else int(_col) + 1
        new_total_width = col * max_width
        new_total_height = _col * max_height
        if total_width < new_total_width:
            new_total_width = total_width
            col = len(images)
        new_img = Image.new('RGB', (new_total_width, new_total_height))
        x_offset = 0
        y_offset = 0
        for index, img in enumerate(images, 1):
            new_img.paste(img, (x_offset, y_offset))
            if col != 1:
                x_offset += img.width

            if index % col == 0:
                if col != 1:
                    y_offset += img.height
                    x_offset = 0
                else:
                    y_offset += img.height

        new_img.save(save_file)


if __name__ == '__main__':
    ip = MarkProcess()
    file = R"D:\Desktop\2\1.jpg"
    save_file = R"D:\Desktop\2\1_1.png"
    img = ip.read_image(file)

    img = ip.add_mosaic(img, [[100, 150], [180, 270]])

    img = ip.transpose_image(img, 0)
    map = {
        "0": {
            "text": "中国人",
            "opt": [[10, 5], [20, 30], [70, 20], [50, 10]],
        },
        "1": {
            "text": "新冠肺炎疫情对于全球经济产生了极其深远的影响",
            "opt": [[200, 220], [220, 300], [300, 345]]
        },
        "2": {
            "text": "脑残",
            "opt": [[150, 200], [100, 150]]
        }
    }
    img = ip.add_words(
        img, ip.get_copy(map)
    )
    img = ip.mark(img, ip.get_copy(map))
    # img = ip.resize(img, rate=2)
    # img = ip.cut_img(img, ([100, 150], [180, 270]))
    # img = ip.change_light_contrast(img, contrast=1)
    # img = ip.tran_gray(img)
    img = ip.tran_binary(img)
    img = ip.mirror(img, 1)
    ip.save_image(img, save_file)
