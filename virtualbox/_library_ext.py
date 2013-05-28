import inspect

from virtualbox import library

import vboxapi
manager = vboxapi.VirtualBoxManager(None, None)

"""
 This module is responsible for bootstrapping the COM interfaces into the 
 VirthalBox and Session class interfaces.

 It is also the place to default COM API behaviour and the Interfaces defined
 within the Main library API.
"""


class IVirtualBox(library.IVirtualBox):
    __doc__ = library.IVirtualBox.__doc__
    def __init__(self, interface=None):
        if interface is None:
            self._i = manager.getVirtualBox()
        else:
            self._i = interface


class ISession(library.ISession):
    __doc__ = library.ISession.__doc__
    def __init__(self, interface=None):
        if interface is None:
            self._i = manager.platform.getSessionObject(None)
        else:
            self._i = interface


# Replace original with extension
for k, v in locals().items():
    if not inspect.isclass(v):
        continue
    if issubclass(v, library.Interface):
        setattr(library, k, v)

