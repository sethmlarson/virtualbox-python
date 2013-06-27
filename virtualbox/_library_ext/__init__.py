import inspect

from virtualbox import library

import vboxapi
manager = vboxapi.VirtualBoxManager(None, None)

"""
 This module is responsible for bootstrapping the COM interfaces into the 
 VirthalBox and Session class interfaces.

 It is also the place to import extension classes that fix up or improve on
 the default COM API behaviour and auto generated Python library file when
 interacting through an Interface to the Main library API.
"""

# Import extension modules
from virtualbox._library_ext.keyboard import IKeyboard
from virtualbox._library_ext.guest_session import IGuestSession
from virtualbox._library_ext.guest import IGuest
from virtualbox._library_ext.machine import IMachine


# Configure ISession bootstrap to build from vboxapi getSessionObject
class ISession(library.ISession):
    __doc__ = library.ISession.__doc__
    def __init__(self, interface=None):
        if interface is None:
            self._i = manager.platform.getSessionObject(None)
        else:
            self._i = interface
    
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.unlock_machine()


# Configure IVirtualBox bootstrap to build from vboxapi getVirtualBox
class IVirtualBox(library.IVirtualBox):
    __doc__ = library.IVirtualBox.__doc__
    def __init__(self, interface=None):
        if interface is None:
            self._i = manager.getVirtualBox()
        else:
            self._i = interface


# Replace original with extension
for k, v in locals().items():
    if not inspect.isclass(v):
        continue
    if issubclass(v, library.Interface):
        setattr(library, k, v)

