#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: tools_find_face.py
@time: 2023/5/28 14:13
@desc: 面部坐标识别
"""
from sdk.tools.load_env import LoadEnv
import requests


class ApiFaceCheck():
    """
        调用百度云 api 识别人脸坐标
    """

    def __init__(self):
        env = LoadEnv()
        self.ak = env.load_env("FACE_API_KEY")
        self.sk = env.load_env("FACE_SECRET_KEY")

    def get_access_token(self):
        """
        获取token
        :param ak:
        :param sk:
        :return:
        """
        url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}".format(
            self.ak, self.sk
        )
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        payload = ""
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()["access_token"]

    def get_face_opt(self, up_url):
        """
        获取面部坐标
        :param up_url:
        :param ak:
        :param sk:
        :return:
        """
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        params = {
            "image": "{}".format(up_url),
            "image_type": "URL",
            "max_face_num": 8,
            "face_type": "LIVE"
        }
        access_token = self.get_access_token()
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        return response.json()
