# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: util_video.py
@time: 2024/1/9 11:40
@desc:

"""
from moviepy.video.io.VideoFileClip import VideoFileClip


def decorate_close(func):
    """
    装饰器自动关闭
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        try:
            result = func(*args, **kwargs)
            args[0].close(args[1])
        finally:
            return result
    return wrapper


class VideoProcess(object):
    """
    VideoProcess
    """

    def __init__(self):
        pass

    def read_video(self, file):
        """

        :param file:
        :return:
        """
        video = VideoFileClip(file)
        return video

    @decorate_close
    def get_video_durations(self, video):
        """
        获取视频时长
        :param video:
        :return:
        """
        duration = video.duration
        return duration

    def close(self, video):
        """

        :param video:
        :return:
        """
        video.close()


if __name__ == '__main__':
    vp = VideoProcess()
    video = vp.read_video(R"C:\Users\JHC00\Downloads\videoplayback.mp4")
    print(vp.get_video_durations(video))
