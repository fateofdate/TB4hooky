"""
coding: utf-8
@Software: PyCharm
@Time:  0:32
@Author: Fake77
@Module Name:
"""
from TB4hooky.Utils.ImportUtil import FileHandle
from importlib import import_module
import time


class AddressInjection(object):
    ADDRESS = None

    @staticmethod
    def register_backup_imp_server(_f):
        AddressInjection.ADDRESS = _f

    def __call__(self, func):

        def arg(*args, **kwargs):
            result = func(*args, **kwargs, remote_addr=self.ADDRESS)
            return result

        return arg


@AddressInjection()
def handle_exception(excType, excValue, tb, remote_addr):
    if excType is ModuleNotFoundError or ImportError:
        module_name = str(excValue).split("'")[-2]
        try:
            FileHandle(remote_addr, module_name).start_remote_import()
            time.sleep(0.5)
            globals()[module_name] = import_module(module_name)

        except Exception as e:
            print(e)
            return

    else:
        raise excType(excValue, tb)
