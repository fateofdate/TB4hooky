from importlib.abc import (
    SourceLoader,
)
import sys
from types import ModuleType
from TB4hooky.netLoader.SourceCodeManager import SourceCodeManager


class RemoteModuleLoader(SourceLoader):
    def __init__(self, endpoint: str, source_code_manager: SourceCodeManager) -> None:
        self._endpoint = endpoint
        self._source_code_manager = source_code_manager

    def load_module(self, fullname: str) -> ModuleType:
        code = self.get_code(fullname)
        mod = sys.modules.setdefault(fullname, ModuleType(fullname))
        mod.__file__ = self.get_filename(fullname)
        mod.__loader__ = self
        mod.__package__ = fullname.rpartition('.')[0]
        exec(code, mod.__dict__)
        return mod

    def get_code(self, fullname: str) -> str:
        filename = self.get_filename(fullname)
        return self._source_code_manager.get_complied_code(filename)

    def get_data(self, path: str) -> bytes: ...

    def get_filename(self, fullname: str) -> str:
        basename = fullname.split('.')[-1]
        return f"{self._endpoint}/{basename}.py"

    def get_source(self, fullname: str) -> str:
        filename = self.get_filename(fullname)
        try:
            return self._source_code_manager.get_source_code(fullname, filename)
        except Exception as _:
            raise ImportError(f"Can't import {filename}.")

    def is_package(self, fullname: str) -> bool:
        return False
