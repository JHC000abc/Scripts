# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author  : v_jiaohaicheng@baidu.com
@des     :

"""
import random
import time
import uuid
import copy
from typing import Type
import datetime
import traceback
from functools import wraps
from cup.util import ThreadPool


class SingletonDecorator:
    """

    """

    def __init__(self, cls):
        self._cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self._cls(*args, **kwargs)
        return self.instance


@SingletonDecorator
class DecorateMultiThread(object):
    """
    多线程装饰器(线程池实现)
    """

    def __init__(self, maxthreads=10):
        """
        初始化线程池
        """
        self.pool = ThreadPool(minthreads=3, maxthreads=maxthreads, daemon_threads=True)
        self.pool.start()

    def callback(self, status, result):
        """
        默认回调函数
        :param status:
        :param result:
        :return:
        """
        print(status, result)

    def add_project(self):
        """
        装饰器函数
        :return:
        """

        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return self.pool.add_1job_with_callback(self.callback, func, *args, **kwargs)

            return wrapper

        return decorate

    def get_pool_status(self):
        """
        获取线程池状态
        :return:
        """
        return self.pool.get_stats()

    def start_pool(self):
        """
        开始 pool
        :return:
        """
        if self.pool:
            self.pool.start()

    def close_pool(self):
        """
        关闭 pool
        :return:
        """
        if self.pool:
            self.pool.stop()


class DecorateFunction(object):
    """
    函数运行装饰器
    """

    def __init__(self, **kwargs):
        self.__dict__.update({k: v for k, v in [
            i for i in locals().values() if isinstance(i, dict)][0].items()})

    def __call__(self, func):
        """
        计算程序运行时间，及记录程序开始和结束状态，装饰器
        :param func:
        :return:
        """

        @wraps(func)
        def decorate(*args, **kwargs):
            func_single = uuid.uuid4()
            func_name = func.__name__
            start_time = self.func_start(func_single, func_name)
            result = func(*args, **kwargs)
            end_time = self.func_start(func_single, func_name)
            self.diff_start_end(func_name, start_time, end_time)
            return result

        return decorate

    def func_start(self, single, name):
        """
        程序开始
        :param single:
        :param name:
        :return:
        """
        start_time = time.time()
        print("{}-{}-{}-函数开始".format(single, datetime.datetime.now(), name))
        return start_time

    def func_end(self, single, name):
        """
        程序开始
        :param single:
        :param name:
        :return:
        """
        func_end = time.time()
        print("{}-{}-{}-函数结束".format(single, datetime.datetime.now(), name))
        return func_end

    def diff_start_end(self, name, start, end):
        """

        :param start:
        :param end:
        :return:
        """
        print("函数{}总执行时间:{}".format(name, end - start))


class ResultTemp:
    """

    """
    status: bool
    result: any
    retry: int

    def __init__(self):
        self.data = None

    @property
    def check_result(self):
        """

        :return:
        """
        if self.data.status:
            if self.data.result:
                return self.data.result
            else:
                raise ValueError("返回值为空")
        else:
            raise ValueError("超过最大重试次数")

    @check_result.setter
    def check_result(self, value):
        self.data = value

    @check_result.deleter
    def check_result(self):
        del self.data.status
        del self.data.result
        del self.data.retry
        del self.data


def retry_new(**params):
    """
    新版重试装饰器
    :param params:
    :return:
    """

    def decorate(func):
        """

        :param func:
        :return:
        """

        @wraps(func)
        def wrapper(*args, **kwargs) -> Type[ResultTemp]:
            """

            :param args:
            :param kwargs:
            :return:
            """
            retry = params.get("retry")
            interval = params.get("interval")
            flag = False
            if not retry:
                retry = 3
            if not interval:
                interval = 3

            retry_recode = copy.deepcopy(retry)
            result = ""
            now_retry_times = None
            total_time_taken = datetime.timedelta()

            while not flag and retry > 0:
                start_time = datetime.datetime.now()
                now_retry_times = retry_recode - retry + 1
                try:
                    print(f"方法 {func.__name__} 开始第 {now_retry_times} 次尝试")
                    result = func(*args, **kwargs)
                    flag = True
                    print(f"方法 {func.__name__} 第 {now_retry_times} 次尝试 【成功】")
                except:
                    print(f"方法 {func.__name__} 第 {now_retry_times} 次尝试 【失败】, 原因: {traceback.format_exc()}")
                    retry -= 1
                    time.sleep(interval)
                finally:
                    end_time = datetime.datetime.now()
                    time_taken = end_time - start_time
                    total_time_taken += time_taken
                    print(f"方法 {func.__name__} 第 {now_retry_times} 次尝试耗时: {time_taken}")

            ResultTemp.status = flag
            ResultTemp.result = result
            ResultTemp.retry = now_retry_times
            print(f"方法 {func.__name__} 执行总耗时: {total_time_taken}")
            return ResultTemp

        return wrapper

    return decorate


def retry(**params):
    """
    重试装饰器
    :param retry: 重试次数，默认为3
    :param sleep: 重试之间的最大等待时间，默认为3秒
    :return:
    """

    def _get_args(params):
        """
        解析参数
        :param params:
        :return:
        """
        if params.get("retry") is None:
            retry = 3
        else:
            retry = params["retry"]
        result = f"重试次数:{retry} 用尽"
        if params.get("sleep") is None:
            sleep = 3
        else:
            sleep = params.get("sleep")
        # 复制重试次数以便输出剩余重试次数
        _retry = copy.deepcopy(retry)
        return retry, sleep, _retry, result

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            flag = False
            retry, sleep, _retry, result = _get_args(params)
            while retry > 0:
                try:
                    result = func(*args, **kwargs)
                    flag = True
                    return flag, result  # 直接返回原函数的执行结果
                except Exception as e:  # 捕获所有异常
                    #
                    retry -= 1
                    # print("重试:{}".format(_retry - retry))
                    if retry == 0:
                        # raise e  # 如果重试次数用尽，则抛出异常
                        print(traceback.format_exc())
                        return flag, result
                finally:
                    time.sleep(random.randint(1, sleep))  # 重试间隔随机等待

        return wrapper

    return decorate
