import inspect

import virtualbox
from virtualbox import library

"""
 This module is responsible for shimming out the auto generated libraries found
 under librar.py.  The intension for the extension classes is to fix up or
 improve on the default COM API behaviour and auto generated Python library
 file when interacting through an Interface to the Main library API.
"""


# Import extension modules
from virtualbox.library_ext.keyboard import IKeyboard
from virtualbox.library_ext.guest_session import IGuestSession
from virtualbox.library_ext.guest import IGuest
from virtualbox.library_ext.machine import IMachine
from virtualbox.library_ext.progress import IProgress


# Configure IVirtualBox bootstrap to build from vboxapi getVirtualBox
class IVirtualBox(library.IVirtualBox):
    __doc__ = library.IVirtualBox.__doc__
    def __init__(self, interface=None, manager=None):
        if interface is not None:
            self._i = interface
        elif manager is not None:
            self._i = manager.get_virtualbox()._i
        else:
            manager = virtualbox.Manager()
            self._i = manager.get_virtualbox()._i


# Configure ISession bootstrap to build from vboxapi getSessionObject
class ISession(library.ISession):
    __doc__ = library.ISession.__doc__
    def __init__(self, interface=None, manager=None):
        if interface is not None:
            self._i = interface
        elif manager is not None:
            self._i = manager.get_session()._i
        else:
            manager = virtualbox.Manager()
            self._i = manager.get_session()._i
    
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.unlock_machine()


# Replace original with extension
for k, v in locals().items():
    if not inspect.isclass(v):
        continue
    if issubclass(v, library.Interface):
        setattr(library, k, v)

