from TB4hooky.netLoader.ModuleLoader import RemoteModuleLoader
from types import ModuleType


class RemotePackageLoader(RemoteModuleLoader):
    def load_module(self, fullname: str) -> ModuleType:
        mod = super(RemoteModuleLoader, self).load_module(fullname)
        mod.__path__ = [self._endpoint]
        mod.__package__ = fullname

        return mod

    def get_filename(self, fullname: str) -> str:
        return f"{self._endpoint}/__init__.py"

    def is_package(self, fullname: str) -> bool:
        return True
