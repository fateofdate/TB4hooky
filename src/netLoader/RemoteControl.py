import requests
import types


class BaseConnection(object):
    def __init__(self): ...

    def __enter__(self):
        raise NotImplementedError("Subclasses must implement __enter__")

    def __exit__(self, exc_type, exc_val,*args, **kwargs):
        raise NotImplementedError("Subclasses must implement __exit__")

    def get_remote_f(self, remote_addr, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement 'get_remote_f'.")

    def get_remote_package(self, remote_addr, *args, **kwargs): ...


class ConnectionRemote(BaseConnection):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._session: requests.Session = None

    def __enter__(self):
        self._session = requests.Session()
        return self

    def __exit__(self, exc_type, exc_val, *args):
        self._session.close()

    def _get_remote_f(self, remote_addr, *args, **kwargs):
        resp = self._session.get(remote_addr)
        return resp

    def get_remote_f(self, remote_addr, *args, **kwargs):
        result = self._get_remote_f(remote_addr, *args, **kwargs)
        return result

    def get_remote_package(self, remote_addr, *args, **kwargs): ...


class ConnectionRemotePackage(BaseConnection):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._session: requests.Session = None

    def __enter__(self):
        self._session = requests.Session()

    def __exit__(self, exc_type, exc_val, *args, **kwargs):
        self._session.close()

    def get_remote_f(self, remote_addr, *args, **kwargs): ...

    def _get_remote_package(self, remote_addr, *args, **kwargs) -> requests.Response:
        result = self._session.get(remote_addr, *args, **kwargs)
        return result

    def get_remote_package(self, remote_addr, *args, **kwargs) -> requests.Response:
        return self._get_remote_package(remote_addr, *args, **kwargs)
