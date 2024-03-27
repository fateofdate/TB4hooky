import importlib.abc
from netLoader.ModuleLoader import RemoteModuleLoader
from Utils.LinkDealer import LinksDealer
from netLoader.PackageLoader import RemoteModuleLoader, RemotePackageLoader


class RemotePathFinder(importlib.abc.PathEntryFinder):
    def __init__(self, base_addr):
        self._links = None
        self._loader = RemoteModuleLoader(base_addr)
        self._base_addr = base_addr

    def find_module(self, fullname):
        parts = fullname.split('.')
        base_name = parts[-1]

        # 检查 link 缓存 如果为空则用LinkDealer 去获取links
        if self._links is None:
            self._links = []
            self._links = LinksDealer.get_link(self._base_addr)

        # 检查是否 package
        if base_name in self._links:
            full_addr = self._base_addr + '/' + base_name
            loader = RemotePackageLoader(full_addr)
            try:
                loader.load_module(fullname)
            except ImportError as e:
                loader = None
            return loader, [full_addr]

        # 检查是否为 module
        remote_filename = base_name + '.py'
        if remote_filename in self._links:
            return self._loader, []
        return None, []

    def invalidate_caches(self):
        self._links = None

