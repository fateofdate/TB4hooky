"""
coding: utf-8
@Software: PyCharm
@Time:  0:41
@Author: Fake77
@Module Name:
"""
import sys
from TB4hooky.Utils.LinkDealer import LinksDealer
import os
from loguru import logger
from aiohttp import ClientSession
import asyncio
import aiohttp
from tqdm import tqdm


class FileHandle(object):
    """
    package = FileHandle("http://127.0.0.1:9000", 'torch')
    package.start_remote_import()

    """

    def __init__(self, _endpoint: str, package: str, loop):
        # 判断是否为dist-info 包文件
        if package.endswith("dist-info"):
            package = package
        else:
            package = package.replace(".", '/')
        # 生成根路径
        self._root_path = _endpoint
        # 包路径
        self._endpoint = _endpoint + '/' + package
        self._package = package
        # 初始化链接库
        self._links = LinksDealer.get_filehandle_links(_endpoint + '/' + package)
        # 获取当前安装目录
        self._install_path = FileHandle.get_install_path()
        # 如果获取不到安装目录则在当前文件夹下创建安装目录
        if self._install_path is None:
            self._install_path = '\\site-packages'
        # 下载文件列表
        self._files = []
        # 事件循环
        self._event_loop = loop
        # 设置并发信号量
        self.semaphore = asyncio.Semaphore(100)
        # 设置重发列表
        self._retry = []

    @staticmethod
    def get_install_path():
        """
        获取安装路径 一般为 site-packages
        """
        for path in sys.path:
            if path.split('\\')[-1] == 'site-packages':
                return path

    @staticmethod
    def is_directory(path):
        """
        判断是否为文件
        directory/ 目录 -> True
        hello.txt 文件 -> False
        """
        if path[-1] == '/':
            return True
        return False

    async def download_file(self, path: str, pbar: tqdm):
        """
        下载文件
        :param: path: url
        :param: pbar: tqdm object
        """
        async with self.semaphore:
            try:
                async with ClientSession() as session:
                    async with session.get(path) as content:
                        filepath = self._install_path + path[len(self._root_path):].replace("/", '\\')

                        directory_path = "\\".join(filepath.split('\\')[:-1])

                        if not os.path.exists(directory_path):
                            os.makedirs(directory_path)

                        with open(filepath, 'wb') as f:
                            f.write(await content.read())
                        pbar.update(1)
            except aiohttp.client_exceptions.ClientOSError:
                self._retry.append(path)

    def get_all_file(self, endpoint: str):
        """
        遍历当前endpoint目录下的全部文件
        """
        # 递归获取该包的全部文件
        for sub_path in LinksDealer.get_filehandle_links(endpoint):
            if endpoint[-1] != '/':
                path = endpoint + '/' + sub_path
            else:
                path = endpoint + sub_path
            if self.is_directory(path):
                self.get_all_file(path)
            else:
                self._files.append(path)

    async def main(self, link_lst, pbar):
        tasks = []
        for url in link_lst:
            tasks.append(asyncio.create_task(self.download_file(url, pbar)))
        await asyncio.wait(tasks)

    def start_remote_import(self):
        # 提交远程文件路径到self._files
        self.get_all_file(self._endpoint)

        # 判断远程包是否存在
        if len(self._files) == 0:
            raise ImportError(f"Not such Package {self._package} in {self._endpoint}.")

        logger.info(f"remote import {self._package} from {self._endpoint} total file: {len(self._files)}")

        # fetch 远程包
        with tqdm(total=len(self._files)) as pbar:
            self._event_loop.run_until_complete(self.main(self._files, pbar))
            if len(self._retry) != 0:
                self._event_loop.run_until_complete(self.main(self._retry, pbar))

