from TB4hooky.netLoader.MetaFinder import RemoteMetaFinder
from TB4hooky.netLoader.SourceCodeManager import SourceCodeManager
import sys

_meta = {}
_scm = SourceCodeManager()


def register(endpoint: str) -> None:
    if not hasattr(_meta, endpoint):
        finder = RemoteMetaFinder(endpoint, _scm)
        _meta[endpoint] = finder
        sys.meta_path.append(finder)


def unload(endpoint: str) -> None:
    if hasattr(_meta, endpoint):
        finder = _meta.pop(endpoint)
        sys.meta_path.remove(finder)
