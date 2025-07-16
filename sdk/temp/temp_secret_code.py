#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: temp_secret_code.py
@time: 2023/6/22 23:44
@desc:  生成随机验证码图片
"""

import random
from io import BytesIO
from PIL import ImageDraw
from sdk.utils.util_img import MarkProcess
from sdk.utils.util_encrypt import EncryptProcess
from sdk.utils.util_folder import FolderProcess
import PIL
import os


class GenerateCaptchaImage():
    """
    生成验证码图片
    """

    def __init__(self):
        self.mark = MarkProcess()
        self.encrypt = EncryptProcess()
        self.folder = FolderProcess()
        path = self.folder.split_path(os.path.realpath(__file__), "sdk")
        self.mark.Font = self.folder.merge_path(
            [path[0], "sdk", "plugins", "SourceHanSerifSC-Bold.otf"])

    def random_color(self, nums=3):
        """
        获取指定数量的随机颜色值
        :param nums:
        :return:
        """
        random_num_lists = []
        while nums > 0:
            random_num = random.randint(0, 255)
            random_num_lists.append(random_num)
            nums -= 1
        return tuple(random_num_lists)

    def draw_str(self, img):
        """
        在图片上写随机字符
        :param img:
        :return:
        """
        for index, text in enumerate(self.encrypt.get_random_str(4)):
            self.mark.add_word(img, index, text, self.random_color())
        return img

    def noise(self, image, width=120, height=35, line_count=3, point_count=20):
        '''

        :param image: 图片对象
        :param width: 图片宽度
        :param height: 图片高度
        :param line_count: 线条数量
        :param point_count: 点的数量
        :return:
        '''
        draw = ImageDraw.Draw(image)
        for i in range(line_count):
            x1 = random.randint(0, width)
            x2 = random.randint(0, width)
            y1 = random.randint(0, height)
            y2 = random.randint(0, height)
            draw.line((x1, y1, x2, y2), fill=self.random_color())

            # 画点
            for i in range(point_count):
                draw.point([random.randint(0, width), random.randint(
                    0, height)], fill=self.random_color())
                x = random.randint(0, width)
                y = random.randint(0, height)
                draw.arc((x, y, x + 4, y + 4), 0, 90, fill=self.random_color())

        return image

    def get_bytes_io(self, file: str = None, img: PIL.JpegImagePlugin.JpegImageFile = None):
        """

        :param file:
        :param img:
        :return:
        """
        if not img:
            img = self.mark.read_image(file, mode=-1)

        f = BytesIO()
        img.save(f, 'png')  # 保存到BytesIO对象中, 格式为png
        data = f.getvalue()
        f.close()
        return data

    def main(self):
        """

        :return:
        """
        image = self.mark.make_mix_img(color=self.random_color(4))
        image = self.draw_str(image)
        image = self.noise(image)
        image.save('test.png')


if __name__ == '__main__':
    vy = GenerateCaptchaImage()
    data = vy.main()
