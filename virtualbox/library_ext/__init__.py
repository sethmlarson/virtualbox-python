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
from virtualbox.library_ext.console import IConsole
from virtualbox.library_ext.session import ISession
from virtualbox.library_ext.event_source import IEventSource


# Configure IVirtualBox bootstrap to build from vboxapi getVirtualBox
class IVirtualBox(library.IVirtualBox):
    __doc__ = library.IVirtualBox.__doc__
    def __init__(self, interface=None, manager=None):
        if interface is not None:
            super(IVirtualBox, self).__init__(interface)
        elif manager is not None:
            self._i = manager.get_virtualbox()._i
        else:
            manager = virtualbox.Manager()
            self._i = manager.get_virtualbox()._i


# Replace original with extension
for k, v in locals().items():
    if not inspect.isclass(v):
        continue
    if issubclass(v, library.Interface):
        setattr(library, k, v)

