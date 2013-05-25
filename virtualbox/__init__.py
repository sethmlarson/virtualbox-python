import vboxapi
from virtualbox import library


manager = vboxapi.VirtualBoxManager(None, None)


class VirtualBox(library.IVirtualBox):
    def __init__(self, interface=None):
        if interface is None:
            self._i = manager.getVirtualBox()
        else:
            self._i = interface


class Session(library.ISession):
    def __init__(self, interface=None):
        if interface is None:
            self._i = manager.platform.getSessionObject(None)
        else:
            self._i = interface


