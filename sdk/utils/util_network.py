# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: util_network.py
@time: 2023/7/30 22:37
@desc:

"""
import os
from sdk.utils.util_decorate import retry
import requests
from urllib3.exceptions import InsecureRequestWarning

# 禁用 InsecureRequestWarning 警告
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


# from curl_cffi import requests


class NetWorkRequests(object):
    """
    NetWorkRequests
    """

    @retry(retry=3)
    def requests(self, url, headers=None, params=None, cookies=None, timeout=(15, 15),
                 data=None, json=None, method="POST", stream=False, proxies=None):
        """

        :param url:
        :param headers:
        :param params:
        :param cookies:
        :param timeout:
        :param data:
        :param json:
        :param method:
        :param stream:
        :param proxies:
        :return:
        """
        if method == "POST":
            response = requests.post(
                url=url,
                data=data,
                json=json,
                stream=stream,
                cookies=cookies,
                headers=headers,
                proxies=proxies,
                timeout=timeout,
                verify=False
            )
        elif method == "GET":
            response = requests.get(
                url=url,
                params=params,
                stream=stream,
                cookies=cookies,
                headers=headers,
                proxies=proxies,
                timeout=timeout,
                verify=False
            )
        elif method == "HEAD":
            response = requests.head(
                url=url,
            )
        else:
            raise ValueError("ERROR Methods {}".format(method))
        return response

    def get_size(self, url, method="GET"):
        """

        :param url:
        :param method:
        :return:
        """
        content_len = 0
        try:
            response = requests.head(url)  # 使用 HEAD 请求以获取头信息
            content_len = response.headers.get('Content-Length')
        except:
            pass
        if content_len:
            return int(content_len)
        else:
            return 0

    def download_videos(self, url, file, headers=None, proxies=None, max_size=1024 * 1024 * 5, method="GET"):
        """
        支持分片下载文件
        :param url: 下载地址
        :param file: 保存路径
        :param headers: 请求头
        :param proxies: 代理
        :param max_size: 单次下载最大字节数（默认5MB）
        :param method: HTTP方法（GET/POST）
        :return: 下载结果（包含状态、分片信息等）
        """
        if headers is None:
            headers = {}

        res = {
            "status": -1,
            "url": url,
            "msg": "Failed",
            "result": []
        }

        # 首次请求（获取文件大小并测试连接）
        headers["Range"] = "bytes=0-0"  # 只请求第一个字节
        status, response = self.requests(url, headers=headers, proxies=proxies, method=method)

        if not status:
            return res

        # 从Content-Range获取完整文件大小
        content_range = response.headers.get("Content-Range", "")
        if content_range:
            content_len = int(content_range.split("/")[-1])
        else:
            # 如果服务器不支持Range请求，尝试直接下载
            try:
                with open(file, "wb") as fp:
                    for chunk in response.iter_content(chunk_size=8192):
                        fp.write(chunk)
                res.update({"status": 0, "msg": "Success"})
                return res
            except Exception as e:
                res["msg"] = f"Direct download failed: {str(e)}"
                return res

        res["content_len"] = content_len

        # 如果文件小于等于max_size，直接下载
        if content_len <= max_size:
            headers.pop("Range", None)  # 移除Range头
            try:
                with open(file, "wb") as fp:
                    for chunk in response.iter_content(chunk_size=8192):
                        fp.write(chunk)
                res.update({"status": 0, "msg": "Success"})
                return res
            except Exception as e:
                res["msg"] = f"Direct download failed: {str(e)}"
                return res

        # 分片下载逻辑
        nums = (content_len + max_size - 1) // max_size
        res["split_nums"] = nums
        download_status_all = True

        # 清空目标文件
        with open(file, "wb"):
            pass

        # 分片下载
        with open(file, "r+b") as fp:
            for i in range(nums):
                start = i * max_size
                end = min((i + 1) * max_size - 1, content_len - 1)
                headers["Range"] = f"bytes={start}-{end}"

                chunk_status, response = self.requests(
                    url, headers=headers, proxies=proxies,
                    stream=True, method=method
                )

                if not chunk_status:
                    download_status_all = False
                    res["result"].append({"status": False, "during": [start, end]})
                    continue

                fp.seek(start)
                for chunk in response.iter_content(chunk_size=8192):
                    fp.write(chunk)
                fp.flush()

                res["result"].append({"status": True, "during": [start, end]})

        # 校验文件完整性
        if download_status_all:
            downloaded_size = os.path.getsize(file)
            if downloaded_size == content_len:
                res.update({"status": 0, "msg": "Success"})
            else:
                res["msg"] = f"File size mismatch (expected {content_len}, got {downloaded_size})"

        return res
