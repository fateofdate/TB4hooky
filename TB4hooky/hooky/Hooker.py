import base64
import json
import sys
import types

LOGGER = True

from TB4hooky.netLoader.AdapterConnectionRemote import AdapterConnectionRemote as ConnectionRemote
from abc import ABCMeta, abstractmethod
from TB4hooky.typeInspect.Inspect import Inspect
from TB4hooky.hooky.CacheObject import Cache
from loguru import logger


DEFAULT_CACHE_COUNT = 64



def unable_logger():
    global LOGGER
    LOGGER = False


class MetaCodeHooker(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def extract_co_code(*args, **kwargs): ...

    @abstractmethod
    def swap_code_info(self, *args, **kwargs): ...

    @abstractmethod
    def swap_remote_code_info(self, *args, **kwargs): ...


class BaseCodeHooker(object):
    """ BaseCodeHooker """

    def __init__(self, _f, remote: bool = False, *args, **kwargs):
        if not ((3, 7) < sys.version_info < (3, 8)):
            raise NotImplemented("Not implemented yet")
        # 远程hook
        self._remote = remote
        # 实现函数对象
        self._f = _f
        # 被hook对象
        self._hook_obj = None
        # 缓存
        self._cache = None
        # 缓存计数器
        self._cache_count = None
        # 当前被hook的函数
        # remote func argument
        self.arg = args
        self.kwarg = kwargs

    # extract implement hook function 'co_code' byte code
    @staticmethod
    def extract_co_code(func):
        return BaseCodeHooker._extract_co_code(func)

    @staticmethod
    def _extract_co_code(func):
        Inspect.check_function_type(func)
        return func.__code__.co_code

    def _swap_code_info(self):
        Inspect.check_function_type(self._f)
        Inspect.check_function_type(self._hook_obj)
        _f_code = self._f.__code__
        if not self._cache:
            self._cache = BaseCodeHooker.extract_co_code(self._f)
        self._hook_obj.__code__ = types.CodeType(
            _f_code.co_argcount,
            _f_code.co_kwonlyargcount,
            _f_code.co_nlocals,
            _f_code.co_stacksize,
            _f_code.co_flags,
            self._cache,
            _f_code.co_consts,
            _f_code.co_names,
            _f_code.co_varnames,
            _f_code.co_filename,
            _f_code.co_name,
            _f_code.co_firstlineno,
            _f_code.co_lnotab,
            _f_code.co_freevars
        )

    def swap_code_info(self):
        self._swap_code_info()

    def swap_remote_code_info(self, host):
        pass


class CodeHooker(BaseCodeHooker):
    def __init__(self, _f, remote: bool = None):
        if remote:
            self._cache_count = DEFAULT_CACHE_COUNT
        super().__init__(_f, remote)

    def __call__(self, func):
        self._hook_obj = func

        def arg_recv(*args, **kwargs):
            if not self._remote:
                if LOGGER:
                    logger.success(f"Hook mod [Local], Local function"
                                   f" from [{self._f.__name__}] to Hook object [{self._hook_obj.__name__}]")

                self.swap_code_info()
            else:
                if LOGGER:
                    logger.success(f"Hook mod [Remote], Remote code "
                                   f"from host [{self._f}] to Hook object [{self._hook_obj.__name__}]")

                self.swap_remote_code_info(self._f)
            return self._hook_obj(*args, **kwargs)

        return arg_recv

    @classmethod
    def serialize_init(cls, func):
        return cls(func, remote=False)

    def _serialize_func(self, count: int) -> str:
        _f_struct = {"cache_count": count,
                     "co_argcount": self._f.__code__.co_argcount,
                     'co_kwonlyargcount': self._f.__code__.co_kwonlyargcount,
                     'co_nlocals': self._f.__code__.co_nlocals,
                     'co_stacksize': self._f.__code__.co_stacksize,
                     'co_flags': self._f.__code__.co_flags,
                     'co_codestring': base64.b64encode(self._f.__code__.co_code).decode(),
                     'co_consts': self._f.__code__.co_consts,
                     'co_names': self._f.__code__.co_names,
                     'co_varnames': self._f.__code__.co_varnames,
                     'co_filename': self._f.__code__.co_filename,
                     'co_name': self._f.__code__.co_name,
                     'co_firstlineno': self._f.__code__.co_firstlineno,
                     'co_lnotab': base64.b64encode(self._f.__code__.co_lnotab).decode(),
                     'co_freevars': self._f.__code__.co_freevars}
        return json.dumps(_f_struct)

    def serialize_func(self, count: int) -> str:
        return self._serialize_func(count)

    def _set_cache(self, serialize: dict):
        for key in serialize.keys():
            value = serialize[key]
            if key == "cache_count":
                self._cache_count = int(value)
            self._cache[key] = value

    def swap_remote_code_info(self, host, *args, **kwargs):
        self._swap_remote_code_info(host)

    def _set_hook_code(self):
        self._hook_obj.__code__ = types.CodeType(
            self._cache['co_argcount'],
            self._cache['co_kwonlyargcount'],
            self._cache['co_nlocals'],
            self._cache['co_stacksize'],
            self._cache['co_flags'],
            self._cache['co_codestring'],
            self._cache['co_consts'],
            self._cache['co_names'],
            self._cache['co_varnames'],
            self._cache['co_filename'],
            self._cache['co_name'],
            self._cache['co_firstlineno'],
            self._cache['co_lnotab'],
            self._cache['co_freevars']
        )

    def _swap_remote_code_info(self, host, *args, **kwargs):
        Inspect.check_string_type(host)
        if not self._cache_count:

            # remote cache
            with ConnectionRemote() as conn:
                remote_content = conn.get_remote_f(host, *args, **kwargs)

            # 判断分发服务器是否在线
            if 0 < (remote_content.status_code - 200) < 10:
                raise Exception(f"Remote code request Error status "
                                f"code: {remote_content.status_code} remote host: {host}.")
            remote_content = remote_content.json()

            # 取出RPC 填充 cache
            self._cache = Cache()
            self._set_cache(remote_content)
            self._cache.pop("cache_count")

        self._cache_count -= 1
        self._set_hook_code()


class InstanceCodeHooker(CodeHooker):
    _INSTANCE = {}

    def __init__(self, _f, instance):
        super().__init__(_f, remote=False)
        # 保证注册过的instance
        if instance not in self._INSTANCE.values():
            self._instance = instance
            self._INSTANCE[hash(instance)] = instance
        else:
            self._instance = self._INSTANCE[hash(instance)]
        Inspect.check_string_type(_f)
        self._f = getattr(instance, _f)

    def __call__(self, func):
        self._hook_obj = func

        def arg_recv(*args, **kwargs):
            if logger:
                logger.success(f"Hook mod [Local], Local function"
                               f" from [{self._instance.__class__.__name__}().{self._f.__name__}] to Hook object [{self._hook_obj.__name__}]")

            self.swap_code_info()

            return self._hook_obj(self._instance, *args, **kwargs)

        return arg_recv

    def swap_remote_code_info(self, host, *args, **kwargs):
        raise NotImplemented("Error 'InstanceCodeHooker' "
                             "not support remote hook should use 'CodeHooker'.")

    def _swap_remote_code_info(self, host, *args, **kwargs):
        raise NotImplemented("Error 'InstanceCodeHooker' "
                             "not support remote hook should use 'CodeHooker'.")
