"""
coding: utf-8
@Software: PyCharm
@Time:  7:06
@Author: Fake77
@Module Name:
"""
import sys


class GlobalException(object):

    def __init__(self, exc_handle):
        sys.excepthook = exc_handle

    @classmethod
    def register_global_exception(cls, exc_handle):
        cls(exc_handle)

