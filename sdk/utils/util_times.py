#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC
@file: util_times.py
@time: 2023/6/11 22:30
@desc:
"""
import time
import threading
from dateutil import relativedelta
from datetime import timedelta, datetime


class TimeProcess():
    """

    """

    def __init__(self):
        """

        """
        self.lock = threading.Lock()

    def calculate_func_running_time(self):
        """
        计算时间装饰器
        :param func:
        :return:
        """
        self.lock.acquire()

        def log(func):
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                print(
                    f"{func.__name__} 的执行时间为:{end_time - start_time} 秒")
                return result
            return wrapper
        self.lock.release()
        return log

    @staticmethod
    def get_normal_date(format='%Y-%m-%d %H-%M-%S'):
        """
        获取当前时间戳对应的标准时间
        :param format:
        :return:
        """
        return time.strftime(format, time.localtime())

    @staticmethod
    def get_stamp_date(stamp, format='%Y-%m-%d %H-%M-%S'):
        """
        获取指定时间戳对应的标准时间
        :param format:
        :return:
        """
        return time.strftime(format, time.localtime(stamp))

    @staticmethod
    def get_differ_hours_date(
            days: int = 0,
            hours: int = 0,
            minutes: int = 0,
            seconds: int = 0,
            format='%Y-%m-%d %H:%M:%S'):
        """
        获取与当前时间相距+3/-3 小时，分钟，秒的时间
        :param hours:
        :param minutes:
        :param seconds:
        :param format:
        :return:
        """
        return datetime.strptime(datetime.now().strftime(
            format), format) + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    @staticmethod
    def get_timestamp(time_str: str, format="%Y-%m-%d %H:%M:%S"):
        """
        标准时间转时间戳
        :return:
        """
        return time.mktime(time.strptime(time_str, format))

    @staticmethod
    def get_hours_minutes_seconds(time_int: int) -> dict:
        """
        获取秒数对应的小时，分钟，秒
        :param time_int:
        :return:
        """
        hours = time_int // 3600
        minutes = time_int % 3600 // 60
        seconds = time_int % 3600 % 60
        return {
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
        }

    @staticmethod
    def get_diff_days(date1: datetime, date2: datetime) -> int:
        """
        获取两个时间相差天数
        :param date1:
        :param date2:
        :return:
        """
        return (date2 - date1).days

    @staticmethod
    def get_precis_diff_times(time1, time2):
        """
          2023-12-12 34:56:03
        """

        def split_times(_time):
            date1, date2 = _time.split(" ")
            year, month, day = date1.split("-")
            hour, minute, second = date2.split(":")
            return int(year), int(month), int(day), int(hour), int(minute), int(second)

        year, month, day, hour, minute, second = split_times(time1)
        _time1 = datetime(year, month, day, hour, minute, second)
        year, month, day, hour, minute, second = split_times(time2)
        _time2 = datetime(year, month, day, hour, minute, second)

        delta = relativedelta.relativedelta(_time2, _time1)
        print(f"相差:{delta.years}年 {delta.months}月 {delta.days}天 {delta.hours}小时 {delta.minutes}分钟 {delta.seconds}秒")
        return delta.years, delta.months, delta.days, delta.hours, delta.minutes, delta.seconds
