from __future__ import absolute_import
import inspect

import virtualbox
from virtualbox import library

"""
 This module is responsible for shimming out the auto generated libraries found
 under library.py.  The intension for the extension classes is to fix up or
 improve on the default COM API behaviour and auto generated Python library
 file when interacting through an Interface to the Main library API.
"""


# Import extension modules
from .vbox import IVirtualBox
from .session import ISession
from .keyboard import IKeyboard
from .guest_session import IGuestSession
from .guest import IGuest
from .host import IHost
from .machine import IMachine
from .progress import IProgress
from .console import IConsole
from .event_source import IEventSource
from .mouse import IMouse
from .process import IProcess
from .guest_process import IGuestProcess
from .appliance import IAppliance
from .virtual_system_description import IVirtualSystemDescription


# Replace original with extension
for k, v in [a for a in locals().items()]:
    if not inspect.isclass(v):
        continue
    if issubclass(v, library.Interface):
        setattr(library, k, v)

