import imp
import importlib
import sys
import requests

from netLoader.RemoteControl import ConnectionRemotePackage


class RemoteModuleLoader(importlib.abc.SourceLoader):
    def __init__(self, addr):
        super().__init__()
        self._base_addr = addr
        self._source_cache = {}

    def module_repr(self, module):
        return f"<RemoteModule {module.__name__} from {module.__file__}>"

    # Override 'load_module' method
    def load_module(self, fullname):
        code = self.get_code(fullname)
        mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
        mod.__file__ = self.get_filename(fullname)
        mod.__loader__ = self
        mod.__package__ = fullname.rpartition(".")[0]

    def get_data(self, path):
        ...

    def get_filename(self, fullname):
        return self._base_addr + '/' + fullname.split('.')[-1] + ".py"

    def get_code(self, fullname):
        src = self.get_source(fullname)
        return compile(src, self.get_filename(fullname), 'exec')

    def get_source(self, fullname):
        filename = self.get_filename(fullname)

        if filename in self._source_cache:
            return self._source_cache[filename]
        try:
            with ConnectionRemotePackage() as conn:
                remote_pkg_content = conn.get_remote_package(filename).text
                self._source_cache[filename] = remote_pkg_content
                return remote_pkg_content
        except (ConnectionError, requests.ConnectionError, requests.HTTPError) as _:
            raise ImportError(f"Can not load {filename}")

    def is_package(self, fullname):
        return False
