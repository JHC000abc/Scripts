#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: util_encrypt.py
@time: 2023/5/28 14:17
@desc:
"""
import base64
import hashlib
import uuid
import random


class EncryptProcess(object):
    """
    加密
    """

    def make_md5(self, file: str = None, data: str = None, salt: bytes = b""):
        """
        生成md5
        :param file:
        :param data:
        :param salt:
        :return:
        """
        if file:
            hash = hashlib.md5(salt)
            with open(file, 'rb') as fp:
                hash.update(fp.read())
            return hash.hexdigest()
        if data:
            md5_machine = hashlib.md5(salt)
            md5_machine.update(data.strip().encode('utf-8'))
            return md5_machine.hexdigest()

    def encode_base32(self, data: bytes, retype=None):
        """
        base32 编码
        :param data:
        :param retype:
        :return:
        """
        if not retype:
            return base64.b32encode(data)
        else:
            return self.tran_byte_str(base64.b32encode(data))

    def encode_base64(self, data: bytes, retype=None):
        """
        base64 编码
        :param data:
        :param retype: 默认返回字符串类型，还支持返回bytes
        :return:
        """
        if not retype:
            return base64.b64encode(data).decode("utf-8")
        else:
            return base64.b64encode(data)

    def decode_base64(self, data) -> str:
        """
        base64 解码
        :param data:bytes/str都支持
        :return:
        """
        return base64.urlsafe_b64decode(data).decode("utf-8")

    def tran_byte_str(self, data):
        """
        bytes str 互转
        """
        if isinstance(data, bytes):
            return data.decode("utf-8")
        elif isinstance(data, str):
            return data.encode()
        else:
            type_data = type(data)
            raise TypeError(f"data must in type of str or bytes not {type_data}")

    def decode_unicode(self, data) -> str:
        """
        unicode转中文，支持bytes和str类型输入
        """
        if isinstance(data, str):
            return data.encode().decode("unicode_escape")
        elif isinstance(data, bytes):
            return data.decode("unicode_escape")
        else:
            raise ValueError('输入类型错误{}{}'.format(data, type(data)))

    def make_uuid(self, status: int = 0):
        """
        生成uuid
        :param status:
        :return:
        """
        if status == 0:
            return str(uuid.uuid4())
        elif status == 1:
            return str(uuid.uuid4()).replace("-", "_")

    def get_random_str(self, secret_len=4, random_char_status=False):
        """

        :param secret_len:
        :param random_char_list:
        :return:
        """
        result = [str(i) for i in range(secret_len)]
        if random_char_status:
            random_char_list = ["#", "*", "_", "-", ".", "$", "@"]
        else:
            random_char_list = None
        for i in range(secret_len):
            random_num = str(random.randint(0, 9))
            random_low_alpha = chr(random.randint(97, 122))
            random_up_alpha = chr(random.randint(97, 122)).upper()
            if random_char_list:
                random_char = random.choice(random_char_list)
                result[i] = random.choice(
                    [random_num, random_low_alpha, random_up_alpha, random_char])
            else:
                result[i] = random.choice(
                    [random_num, random_low_alpha, random_up_alpha])
        return result
