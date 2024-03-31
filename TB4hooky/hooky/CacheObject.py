"""
coding: utf-8
@Software: PyCharm
@Time:  6:23
@Author: Fake77
@Module Name:
"""
import base64


class CacheMinx:
    __slots__ = ()

    def __setitem__(self, key, value):
        if key in ("co_lnotab", "co_codestring"):
            value = base64.b64decode(value.encode())
        if key in ("co_argcount", "co_kwonlyargcount", "co_nlocals",
                   "co_stacksize", "co_flags", "co_firstlineno"):
            value = int(value)
        if key in ("co_consts", "co_names", "co_varnames", "co_freevars"):
            value = tuple(value)
        return super().__setitem__(key, value)


class Cache(CacheMinx, dict):
    ...
