# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: setting.py
@time: 2024/2/29 21:43
@desc:

"""
LOGGING_DICT = {
    "version": 1.0,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(threadName)s:%(thread)d - "
                      "%(filename)s[%(name)s:%(lineno)d] - %(levelname)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "simple": {
            "format": "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "test": {
            "format": "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "filters": {},
    "handlers": {
        "console_debug_handler": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file_info_handler": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": "info.log",
            "maxBytes": 800,
            "backupCount": 10,
            "encoding": "utf-8",
        },
        "file_debug_handler": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": "debug.log",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "LOGGER_DEBUG": {
            "handlers": ["console_debug_handler"],
            "level": "DEBUG",
            "propagate": False,
        },
        "LOGGER_ONLINE": {
            "handlers": ["console_debug_handler", "file_info_handler"],
            "level": "INFO",
            "propagate": False,
        },
        "": {
            "handlers": ["file_debug_handler", "console_debug_handler"],
            "level": "DEBUG",
            "propagate": False,
        }

    }
}
