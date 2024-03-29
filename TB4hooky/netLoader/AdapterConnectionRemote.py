from TB4hooky.netLoader.RemoteControl import ConnectionRemote, ConnectionRemotePackage


class AdapterConnectionRemote(ConnectionRemote):
    """
    For modify the method 'get_remote_f' should
    override method '_get_remote_f' and '__exit__', '__enter__' method
    you can save the IO object(example save the process buffer object) in 'self._session'
    or implement you own protocol.
    """
    pass


class AdapterConnectionRemotePackage(ConnectionRemotePackage):
    """
    For modify the method 'get_remote_package' should
    override method '_get_remote_package' and '__exit__', '__enter__' method
    you can save the IO object(example save the process buffer object) in 'self._session'
    or implement you own protocol.
    """
    pass

