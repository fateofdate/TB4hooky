from importlib.abc import MetaPathFinder
from TB4hooky.netLoader.SourceCodeManager import SourceCodeManager
from TB4hooky.Utils.LinkDealer import LinksDealer
from TB4hooky.netLoader.PackageLoader import RemotePackageLoader

class RemoteMetaFinder(MetaPathFinder):
    def __init__(self, endpoint: str, source_code_manager: SourceCodeManager) -> None:
        self._endpoint = endpoint
        self._nodes = {}
        self._source_code_manager = source_code_manager

    def _is_module(self, filename: str, endpoint: str) -> bool:
        return filename in self._nodes[endpoint]

    def _is_package(self, basename: str, endpoint) -> bool:
        return basename in self._nodes[endpoint]

    def _store_node(self, node: str) -> None:
        if not hasattr(self._nodes, node):
            self._nodes[node] = LinksDealer.get_link(node)

    def _get_node(self, path: str):
        if path is None:
            return self._endpoint
        else:
            if not path[0].startswith(self._endpoint):
                return None
        return path[0]

    def find_module(self, fullname: str, path: str = None):
        # 1. 获取当前节点
        current_code = self._get_node(path)
        # 如果节点不存在中止流程
        if not current_code:
            return None
        #   1.1 缓存节点
        self._store_node(current_code)
        # 2. 获取当前的basename (模块名称)
        basename = fullname.split(".")[-1]
        # 3. 处理package
        if self._is_package(basename, current_code):
            child_location = f"{current_code}/{basename}"
            loader = RemotePackageLoader(child_location, self._source_code_manager)
            try:
                loader.load_module(fullname)
                self._nodes[child_location] = LinksDealer.get_link(child_location)
            except ImportError as _:
                loader = None
            return loader
        # 4. 处理module
        filename = f"{basename}.py"
        if self._is_module(filename, current_code):
            return RemoteModuleLoader(current_code, self._source_code_manager)
        else:
            return None

    def invalidate_caches(self) -> None:
        self._nodes.clear()
        self._source_code_manager.clear()
