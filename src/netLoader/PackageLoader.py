from netLoader.ModuleLoader import RemoteModuleLoader


class RemotePackageLoader(RemoteModuleLoader):
    def load_module(self, fullname) -> None:
        mod = super().load_module(fullname)
        mod.__path__ = [self._base_addr]
        mod.__package__ = fullname

    def get_filename(self, fullname) -> str:
        return self._base_addr + "/" + '__init.py'

    def is_package(self, fullname) -> bool:
        return True

    