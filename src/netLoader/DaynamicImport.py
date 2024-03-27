"""
reference:
        https://peps.python.org/pep-0302/
        https://python3-cookbook.readthedocs.io/zh-cn/latest/c10/p11_load_modules_from_remote_machine_by_hooks.html
"""
import sys

from netLoader.PathFinder import RemotePathFinder

from Utils.LinkDealer import LinksDealer

_addr_path_cache = {}

_installed = False


def handle_addr(path):
    if LinksDealer.filter_links(path):
        if path in _addr_path_cache:
            finder = _addr_path_cache[path]
        else:
            finder = RemotePathFinder(path)
            _addr_path_cache[path] = finder
        return finder
    else:
        pass


def register_remote_pkg_server(url):
    if _installed:
        sys.path.append(url)


def install_path_hook():
    sys.path_hooks.append(handle_addr)
    sys.path_importer_cache.clear()
    global _installed
    _installed = True


def remove_path_hook():
    if _installed:
        sys.path_hooks.remove(handle_addr)
        sys.path_importer_cache.clear()
