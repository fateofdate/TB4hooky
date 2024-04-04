"""
coding: utf-8
@Software: PyCharm
@Time:  3:32
@Author: Fake77
@Module Name:
"""
from TB4hooky.hooky.Hooker import CodeHooker

__all__ = [
    'REMOTE_FUNCTION_MAPPING',
    'ServerSerialize',
]

REMOTE_FUNCTION_MAPPING = {}


class ServerSerialize(object):
    def __init__(self, count):
        self.count = count

    def __call__(self, func):
        def recv_args():
            # func callable校验
            assert callable(func)
            func_serialize = CodeHooker.serialize_init(func)
            serialize_result = func_serialize.serialize_func(self.count)
            if func.__name__ in REMOTE_FUNCTION_MAPPING:
                return func
            REMOTE_FUNCTION_MAPPING[func.__name__] = serialize_result
            return func
        return recv_args()

