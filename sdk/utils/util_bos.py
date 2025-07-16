#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: util_bos.py
@time: 2023/5/27 21:12
@desc:
"""
import time
import baidubce
from baidubce.services.sts.sts_client import StsClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.services.bos.bos_client import BosClient
from sdk.base.base_bos import BaseBos
from sdk.utils.util_encrypt import EncryptProcess
from sdk.utils.util_network import NetWorkRequests


class BosAkSk(BaseBos):
    """
    BosAkSk
    """

    def __init__(self, ):
        super(BosAkSk, self).__init__()
        self.bos_client = None

    def init_bos_client(self, network="CN"):
        """
        初始化 bosclient
        :param network:
        :return:
        """
        if network == "CN":
            endpoint = self.bos_host
        else:
            endpoint = self.bos_host_abroad
        if not self.bos_client:
            config = BceClientConfiguration(
                credentials=BceCredentials(
                    self.ak,
                    self.sk
                ),
                protocol=baidubce.protocol.HTTPS,
                endpoint=endpoint)
            config = self.Config(config)
            self.bos_client = BosClient(config)

    def upload(self, url, file, status=0, network="CN", tran_url=False):
        """
        上传
        :param url:
        :param file:
        :param status:
        :param network:
        :param tran_url:
        :return:
        """
        if tran_url:
            url = self.stand_format_url(url)
        bucket_name, key = self.GetBucketKey(url)
        self.init_bos_client(network)
        return self._upload(self.bos_client, file, bucket_name, key, status)

    def download(self, url, file, network="CN", tran_url=False):
        """
        下载
        :param url:
        :param file:
        :param network:
        :param tran_url:
        :return:
        """
        if tran_url:
            url = self.stand_format_url(url)
        bucket_name, key = self.GetBucketKey(url)
        self.init_bos_client(network)
        return self._download(self.bos_client, file, bucket_name, key)

    def get_download_url(self, url, network="CN", tran_url=False):
        """

        :param url:
        :param network:
        :param tran_url:
        :return:
        """
        if tran_url:
            url = self.stand_format_url(url)
        bucket_name, key = self.GetBucketKey(url)
        self.init_bos_client(network)
        return self.bos_client.generate_pre_signed_url(
            bucket_name, key, time.time(), -1).decode("utf-8")


class BosSTS(BaseBos):
    """
    获取 sts
    """

    def __init__(self):
        super(BosSTS, self).__init__()
        self.sts_client = None
        self.bos_client = None
        self.register_time = 0

    def init_sts_client(self):
        """
        初始化 stsclient
        :return:
        """

        def __init():
            config = BceClientConfiguration(
                credentials=BceCredentials(
                    self.ak,
                    self.sk
                ),
                protocol=baidubce.protocol.HTTPS,
                endpoint=self.sts_host)
            self.sts_client = StsClient(config)
            self.register_time = time.time()

        if not self.sts_client:
            __init()
        else:
            now_time = time.time()
            # token 超时 重新初始化
            if now_time - self.register_time >= self.duration_seconds:
                __init()

    def get_sts(self):
        """

        :return:
        """
        access_dict = {}
        access_dict["service"] = "*"
        access_dict["region"] = "bj"
        access_dict["effect"] = "Allow"
        access_dict["resource"] = ["*"]
        access_dict["permission"] = ["READ", "WRITE"]
        access_control_list = {"accessControlList": [access_dict]}
        # 获取token
        response = self.sts_client.get_session_token(
            acl=access_control_list,
            duration_seconds=self.duration_seconds
        )
        sts_ak = str(response.access_key_id)
        sts_sk = str(response.secret_access_key)
        token = response.session_token
        return (sts_ak, sts_sk, token)

    def init_bos_client(self):
        """
        初始化 bosclient
        :param sts_client:
        :return:
        """
        self.init_sts_client()
        if not self.bos_client:
            sts_ak, sts_sk, token = self.get_sts()
            # 配置BceClientConfiguration
            config = BceClientConfiguration(
                credentials=BceCredentials(sts_ak, sts_sk),
                endpoint=self.bos_host,
                security_token=token
            )
            config = self.Config(config)
            self.bos_client = BosClient(config)

    def download(self, url, file, tran_url=False):
        """
        下载
        :param url:
        :param file:
        :param tran_url:
        :return:
        """
        if tran_url:
            url = self.stand_format_url(url)
        bucket_name, key = self.GetBucketKey(url)
        self.init_bos_client()
        return self._download(self.bos_client, file, bucket_name, key)

    def upload(self, url, file, status=0, tran_url=False):
        """
        上传
        :param url:
        :param file:
        :param status:
        :param tran_url:
        :return:
        """
        if tran_url:
            url = self.stand_format_url(url)
        bucket_name, key = self.GetBucketKey(url)
        self.init_bos_client()
        return self._upload(self.bos_client, file, bucket_name, key, status)

    def get_download_url(self, url, tran_url=False):
        """

        :param url:
        :param tran_url:
        :return:
        """
        if tran_url:
            url = self.stand_format_url(url)
        bucket_name, key = self.GetBucketKey(url)
        self.init_bos_client()
        return self.bos_client.generate_pre_signed_url(
            bucket_name, key, time.time(), -1).decode("utf-8")


from sdk.utils.util_decorate import retry
from baidubce import utils
from baidubce.services.bos import storage_class
from sdk.utils.util_class import URLParser


class Online(object):
    """

    """

    def __init__(self):
        self.slat = "sts"
        self.duration_seconds = 129600
        self.bos_client = None
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
        elif tmp_list[2] in ['bd.bcebos.com', 'bj.bcebos.com', 'hkg.bcebos.com', 'cdn.bcebos.com']:
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


class BosOnline(Online):
    """
    正式
    """

    def __init__(self):
        super().__init__()
        self.encrypt = EncryptProcess()
        self.net = NetWorkRequests()

    def init_bos_client(self, url):
        """

        :return:
        """
        if not self.bos_client:
            data = self.get_temp_token(url)
            if data:
                config = BceClientConfiguration(
                    credentials=BceCredentials(data["access_key_id"], data["secret_access_key"]),
                    endpoint=data["host"], security_token=data['session_token'])
                self.bos_client = BosClient(config)
        return self.bos_client

    def get_temp_token(self, url):
        """

        :return:
        """
        result = {}
        bucket_name, key = self.GetBucketKey(url)
        folder = key.split("/")[0]
        host = url.split(bucket_name)[0][0:-1]
        params = {
            'timestamp': int(time.time()),
            'sign': '',
            'source': 1,
            'ct_user_id': 19999,
            'bucket': bucket_name,
            'permission': 'WRITE,READ',
            'region': 'bj',
            'object': f'{folder}/*',
            'duration_seconds': self.duration_seconds,
        }
        tmp = ['{}={}'.format(key, params[key]) for key in sorted(params) if key != 'sign']
        tmp.append(f'key={self.slat}')
        params['sign'] = self.encrypt.make_md5(data='&'.join(tmp))
        url = 'https://test.baidu.com/collection/api/getBosStsCredential'
        status, response = self.net.requests(url=url, data=params)
        response.encoding = "utf-8"
        if status:
            data = response.json()
            result = data["result"]
            result["host"] = host

        return result

    def upload(self, url, file, status=0, tran_url=False):
        """
        上传
        :param url:
        :param file:
        :param status:
        :param tran_url:
        :return:
        """
        if tran_url:
            url = self.stand_format_url(url)
        bucket_name, key = self.GetBucketKey(url)
        self.init_bos_client(url)
        return self._upload(self.bos_client, file, bucket_name, key, status)

    def download(self, url, file, tran_url=False):
        """
        下载
        :param url:
        :param file:
        :param tran_url:
        :return:
        """
        if tran_url:
            url = self.stand_format_url(url)
        bucket_name, key = self.GetBucketKey(url)
        self.init_bos_client(url)
        return self._download(self.bos_client, file, bucket_name, key)

    def get_download_url(self, url, tran_url=False):
        """

        :param url:
        :param tran_url:
        :return:
        """
        if tran_url:
            url = self.stand_format_url(url)
        bucket_name, key = self.GetBucketKey(url)
        self.init_bos_client(url)
        return self.bos_client.generate_pre_signed_url(
            bucket_name, key, time.time(), -1).decode("utf-8")


if __name__ == '__main__':
    bos = BosAkSk()
    url = "https://bj.bcebos.com/collection-data/jiaohaicheng/work/company/l72/videoplayback.mp4"
    local = r"C:\Users\v_jiaohaicheng\Downloads\videoplayback.mp4"
    res = bos.upload(url, local)
    # bos.download(url, local)
    # print(res)
    # print(bos.get_download_url(url))
