"""
coding: utf-8
@Software: PyCharm
@Time:  8:08
@Author: Fake77
@Module Name:
"""
from TB4hooky.netLoader.AdapterConnectionRemote import AdapterConnectionRemotePackage as ConnectionRemotePackage


class SourceCodeManager:
    def __init__(self) -> None:
        self._sources = {}
        self._complied_codes = {}

    def get_source_code(self, filename: str) -> str:
        source = self._sources.get(filename)
        if not source:
            with ConnectionRemotePackage() as conn:
                session = conn.get_remote_package(filename)
                if session.status_code == 200:
                    source = session.text
                    # print(filename)
                else:
                    # print(filename + 'i')
                    session = conn.get_remote_package(filename + 'i')
                    source = session.text
                self._sources[filename] = source
        return source

    def get_complied_code(self, filename: str):
        source = self.get_source_code(filename)
        complied_code = self._complied_codes.get(filename)
        if not complied_code:
            complied_code = compile(source, filename, 'exec')
            self._complied_codes[filename] = complied_code
        return complied_code

    def clear(self) -> None:
        self._sources.clear()
        self._complied_codes.clear()
