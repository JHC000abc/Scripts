# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: util_secret.py
@time: 2024/1/27 23:49
@desc:

"""
# pyotp 2.9.0
import pyotp
import secrets
# python-jose 3.3.0
from jose import jwt, ExpiredSignatureError
from datetime import datetime, timedelta
# passlib 1.7.4
from passlib.context import CryptContext
from sdk.utils.util_encrypt import EncryptProcess


class TotpHandler(object):
    """
    Totp 验证
    """

    def __init__(self, interval=30):
        """

        """
        # 密钥
        self.secret = "fb565ca799a431a5a4102d10ff84cb3661bb0cf0f415e7" \
                      "8cc389ad42ced61fa4dcb3c635a4f5568697526549ed5dee3" \
                      "a5e791d100ce4f9a95c0728e3b617dc07f575edea41ee6152f08" \
                      "6651719606abba2806ea8845ea4d53a2a91e14c31f1ae825a8c00" \
                      "47b05bf580108cb9af7db40a6ed9f0fb2a1802b6eb1823528b68706b"
        # 过期时间
        self.interval = interval
        # 加密类
        self.ep = EncryptProcess()

    def create_secret(self):
        """
        生成128位随机密钥
        :return:
        """
        return secrets.token_hex(128)

    def create_totp(self):
        """

        :return:
        """
        totp = pyotp.TOTP(self.ep.encode_base32(self.ep.tran_byte_str(self.secret)), interval=self.interval)
        return totp, totp.now()

    def verify(self, totp, key):
        """
        验证
        :param totp:
        :param key:
        :return:
        """
        return totp.verify(key)


class JwtHandler(object):
    """
    JWT 验证
    """

    def __init__(self, interval=30, secret=None):
        """

        """
        # 密钥
        self.secret = "fb565ca799a431a5a4102d10ff84cb3661bb0cf0f415e7" \
                      "8cc389ad42ced61fa4dcb3c635a4f5568697526549ed5dee3" \
                      "a5e791d100ce4f9a95c0728e3b617dc07f575edea41ee6152f08" \
                      "6651719606abba2806ea8845ea4d53a2a91e14c31f1ae825a8c00" \
                      "47b05bf580108cb9af7db40a6ed9f0fb2a1802b6eb1823528b68706b"
        # 加密算法
        self.algorithm = "HS256"
        # 默认30秒过期
        self.interval = interval
        # 密钥对象
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_hash_code(self, pwd):
        """
        获取密码对应的 hash 值
        :param pwd:
        :return:
        """
        return self.pwd_context.hash(pwd)

    def verify_hash_code(self, pwd, hash_code):
        """
        验证密码和hash是否匹配
        :param pwd:
        :param hash_code:
        :return:
        """
        return self.pwd_context.verify(pwd, hash_code)

    def create_token(self, key: str = None, data: dict = None):
        """
        创建带exp字段的JWT字符串
        :param data:
        :param expires_delta:
        :return:
        """
        if not (key or data):
            raise ValueError("key or data must be provided")

            # 创建一个包含key（如果提供）和用户数据的字典
        payload = {}
        if key:
            payload['key'] = key
        if data:
            payload.update(data)

        # 设置过期时间
        expires_delta = timedelta(weeks=self.interval)
        expire = datetime.utcnow() + expires_delta

        # 将过期时间添加到payload中
        payload['exp'] = int(expire.timestamp())

        # 使用SECRET_KEY对声明集进行签名并编码为JWT字符串
        token = jwt.encode(payload, self.secret, algorithm=self.algorithm)

        return token

    def decrypt_token(self, token):
        """
        解析 token
        :param token:
        :return:
        """
        try:
            jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return True
        except ExpiredSignatureError:
            return False


if __name__ == '__main__':
    #     totp = Totp()
    #     t_o,t = totp.create_totp()
    #     print(totp.verify_images(t_o, t))
    #     time.sleep(30)
    #     print(totp.verify_images(t_o, t))
    #     time.sleep(30)
    #     print(totp.verify_images(t_o, t))
    #     time.sleep(30)
    #     print(totp.verify_images(t_o, t))
    #
    # form_data = {
    #     "username": "johndoe",
    #     "password": "Abc123."
    # }
    # jh = JwtHandler(interval=8)
    # hash_code = jh.get_hash_code(form_data.get("password"))
    # print("hash_code", hash_code)
    # verify_images = jh.verify_hash_code('Abc123.', "$2b$12$irhUbcZ06qJdvGSKPx7rmeHqjjxl2kLw4sRixoePl6COlmyDZKgj2")
    # print("verify_images", verify_images)
    # token = jh.create_token(data=form_data)
    # # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJqb2hu
    # ZG9lIiwiZXhwIjoxNzE3NDYwNzA5fQ.LZbMYaZyUY_jqLdJy6p4U-zMZFqBNMo0V_Rn4F_uOlY"
    # import time
    #
    # print("token", token)
    # print(jh.decrypt_token(token))
    # time.sleep(3)
    # print(jh.decrypt_token(token))
    # time.sleep(35)
    # print(jh.decrypt_token(token))

    import jwt
    import datetime

    # 准备头部和载荷
    header = {
        "alg": "HS256",
        "typ": "JWT",
        "type": "jwt"
    }

    payload = {
        "createTime": "2024-06-26 17:10:47.280",
        "exp": 1719375527,
        "userId": "fin65024",
        "expiredTime": "2024-06-26 17:23:47.280"
    }

    # 用于签名的密钥
    secret_key = ("RFBBUEkBAAAA0Iyd3wEV0RGMegDAT8KX6wEAAADdt0+9kg2hS6SuUDBK7Xb"
                  "kAAAAAAIAAAAAAANmAADAAAAAEAAAABqNO6V09AE9xIsYmve6m0UAAAAABI"
                  "AAAKAAAAAQAAAAewU1dvxN9nyH6qVOTzL1CygAAACalLNeTRrv59hGfyCHn"
                  "c1Z9P/EBUvj4WiBmD0zpxClld3YJ5JZ5nIIFAAAANokzJsxK4aAjZOQ4iEAHfCi/XRq")
    print(len(secret_key))

    # 生成JWT
    token = jwt.encode(payload, secret_key, algorithm="HS256", headers=header)

    print("Generated JWT:", token)
