# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author  : v_jiaohaicheng@baidu.com
@des     :

"""
import subprocess


class RunCmd(object):
    """
    RunCmd
    """

    def __init__(self):
        pass

    def run(self, cmd, encoding="utf-8"):
        """

        :param cmd:
        :param encoding:
        :return:
        """
        p = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding=encoding
        )
        while p.poll() is None:
            out = p.stdout.readline().strip()
            if out:
                yield out
