#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: tools_voice_tran.py
@time: 2023/5/28 14:14
@desc: 音频转写
"""
import requests
import json
from sdk.tools.load_env import LoadEnv
from sdk.utils.util_network import NetWorkRequests


class VoiceTranChinese():
    """
    百度云音频转写服务
    """

    def __init__(self):
        env = LoadEnv()
        self.client_id = env.load_env("VOICE_CLIENT_ID")
        self.client_secret = env.load_env("VOICE_CLIENT_SECRET")
        self.net = NetWorkRequests()

    def get_access_token(self):
        """
        获取 access_token
        :return:
        """
        host = 'https://aip.baidubce.com/oauth/2.0/token'
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }
        response = self.net._requests(url=host, params=params, method="GET")
        if response["status"] == 0:
            return response["msg"].json()["access_token"]

    def create_tran_client(self, url):
        """
        创建客户端
        :param url:
        :return:
        """
        data = {
            'speech_url': url,
            'format': 'wav',
            'pid': 80001,
            'rate': 16000
        }
        try:
            response = self.net._requests(url='https://aip.baidubce.com/rpc/2.0/aasr/v1/create?access_token={}'.format(self.get_access_token()), data=json.dumps(data))
            if response["status"] == 0:
                res = response["msg"].json()
                return res["task_id"]
            else:
                self.create_tran_client(url)
        except BaseException:
            self.create_tran_client(url)

    def get_tran_result(self, task_id):
        """
        获取接口转写结果
        :param task_id:
        :param token:
        :return:
        """
        if isinstance(task_id, str):
            task_ids = [task_id]
        else:
            task_ids = task_id
        data = {
            'task_ids': task_ids
        }
        try:
            response = requests.post('https://aip.baidubce.com/rpc/2.0/aasr/v1/query?access_token={}'.format(self.get_access_token()),
                                     data=json.dumps(data))
            res = response.json()
            return res
        except BaseException:
            self.get_tran_result(task_id)
