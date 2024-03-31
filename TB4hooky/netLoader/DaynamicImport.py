import asyncio
import importlib
import time
from loguru import logger
from TB4hooky.netLoader.MetaFinder import RemoteMetaFinder
from TB4hooky.netLoader.SourceCodeManager import SourceCodeManager
from TB4hooky.netLoader.ComplexImport import FileHandle
from TB4hooky.Utils.LinkDealer import LinksDealer

import sys

_meta = {}
_scm = SourceCodeManager()
_endpoint = ""


def register(endpoint: str) -> None:
    global _endpoint
    _endpoint = endpoint
    if not hasattr(_meta, endpoint):
        finder = RemoteMetaFinder(endpoint, _scm)
        _meta[endpoint] = finder
        sys.meta_path.append(finder)

def remote_import(_pkg: str):
    if _endpoint:
        loop = asyncio.get_event_loop()
        links = LinksDealer.get_link(_endpoint)
        for link in links:
            if link.startswith(_pkg.split('.')[0]):
                logger.success(f"Find pkg {link.replace('/', '')}!")
                FileHandle(_endpoint, link, loop).start_remote_import()
                time.sleep(0.2)
        print(FileHandle.get_install_path())
        sys.path.append(FileHandle.get_install_path() + '\\' + _pkg.split('.')[0])
        pkg = importlib.import_module(_pkg)
        return pkg


def unload(endpoint: str) -> None:
    if hasattr(_meta, endpoint):
        finder = _meta.pop(endpoint)
        sys.meta_path.remove(finder)
