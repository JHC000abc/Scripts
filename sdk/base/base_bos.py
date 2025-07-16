#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: base_bos.py
@time: 2023/5/27 21:06
@desc:
"""
from baidubce.services.bos import storage_class
from baidubce.retry.retry_policy import BackOffRetryPolicy
from baidubce import utils
from sdk.tools.load_env import LoadEnv
from sdk.utils.util_decorate import retry
from sdk.utils.util_class import URLParser


class BaseBos(object):
    """
    bos 基类
    """

    def __init__(self):
        env = LoadEnv()
        self.ak = env.load_env("BOSAK")
        self.sk = env.load_env("BOSSK")

        self.bos_host = env.load_env("BOSHOST")
        self.bos_host_abroad = env.load_env("BOSHOSTABROAD")
        self.sts_host = env.load_env("BOSSTSHOST")
        # sts token 过期时间 36小时(一般不用考虑过期问题)
        self.duration_seconds = 129600
        self.host_list = ['bd.bcebos.com', 'bj.bcebos.com', 'hkg.bcebos.com']

    def stand_format_url(self, url):
        """

        :param url:
        :return:
        """
        url_obj = URLParser(url)
        if url_obj.host in self.host_list:
            return url
        else:
            host_split = url_obj.host.split(".")
            bucket = host_split[0]
            host = ".".join(host_split[1:])
            url = f"{url_obj.protocol}://{host}/{bucket}/{url_obj.path}/{url_obj.name}.{url_obj.tail}"
            return url

    def Config(self, config):
        """

        :param config:
        :return:
        """
        # 设置请求超时时间 ms
        config.connection_timeout_in_mills = 3000
        # 三次指数退避重试
        config.retry_policy = BackOffRetryPolicy()
        return config

    def GetBucketKey(self, url):
        """

        :param url:
        :return:
        """
        tmp_list = url.split('/')
        # 适配历史上由众测接口生成的下载文件
        if 'json-api/v1' in url:
            bucket = tmp_list[5]
            key = '/'.join(tmp_list[6:])
        elif tmp_list[2] in self.host_list:
            bucket = tmp_list[3]
            key = '/'.join(tmp_list[4:])
        else:
            bucket = tmp_list[2].split('.')[0]
            key = '/'.join(tmp_list[3:])
        return bucket, key

    @retry(retry=3)
    def _download(self, bos_client, file, bucket_name, key):
        """
        自带重试的下载
        :param bos_client:
        :param file:
        :param bucket_name:
        :param key:
        :param retry:
        :return:
        """
        bos_client.get_object_to_file(
            bucket_name, key, file, progress_callback=utils.default_progress_callback)
        return file

    @retry(retry=3)
    def _upload(self, bos_client, file, bucket_name, key, status):
        """
        自带重试的上传
        :param bos_client:
        :param file:
        :param bucket_name:
        :param key:
        :param status:
        :param retry:
        :return:
        """
        if status == 0:
            bos_client.put_object_from_file(
                bucket_name,
                key,
                file,
                storage_class=storage_class.STANDARD,
                progress_callback=utils.default_progress_callback
            )
        else:
            bos_client.put_super_obejct_from_file(
                bucket_name,
                key,
                file,
                chunk_size=5,
                storage_class=storage_class.STANDARD,
                progress_callback=utils.default_progress_callback
            )
        return file