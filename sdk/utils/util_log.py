# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@contact: JHC000abc@gmail.com
@time: 2023/2/11 17:41 $
@desc:

"""
import logging
import os
from datetime import datetime


class TimedFileHandlerWithLock(logging.Handler):
    def __init__(self, log_dir, prefix='log'):
        """

        :param log_dir:
        :param prefix:
        """
        super().__init__()
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.prefix = prefix
        self.current_filename = self._generate_filename()

    def _generate_filename(self):
        """

        :return:
        """
        current_time = datetime.now()
        return os.path.join(self.log_dir, f"{self.prefix}_{current_time.strftime('%Y-%m-%d %H-%M-%S')}.log")

    def emit(self, record):
        """

        :param record:
        :return:
        """
        try:
            current_filename = self._generate_filename()
            if current_filename != self.current_filename:
                self.current_filename = current_filename
            with open(self.current_filename, 'a', encoding='utf-8') as f:
                log_msg = self.format(record)
                f.write(log_msg + '\n')
        except Exception:
            self.handleError(record)


class MyLogger(object):
    """

    """

    def __init__(self, log_dir, prefix='log'):
        self.log_dir = log_dir
        self.prefix = prefix
        self.format = '%(asctime)s-%(threadName)s:%(thread)d-[%(filename)s:%(lineno)d]-%(levelname)s: %(message)s'

    def get_config(self):
        """

        :return:
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        handler = TimedFileHandlerWithLock(self.log_dir, self.prefix)
        formatter = logging.Formatter(self.format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(self.format)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        return logger
