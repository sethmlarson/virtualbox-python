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
from virtualbox.library_ext.vbox import IVirtualBox
from virtualbox.library_ext.session import ISession
from virtualbox.library_ext.keyboard import IKeyboard
from virtualbox.library_ext.guest_session import IGuestSession
from virtualbox.library_ext.guest import IGuest
from virtualbox.library_ext.machine import IMachine
from virtualbox.library_ext.progress import IProgress
from virtualbox.library_ext.console import IConsole
from virtualbox.library_ext.event_source import IEventSource
from virtualbox.library_ext.mouse import IMouse


# Replace original with extension
for k, v in locals().items():
    if not inspect.isclass(v):
        continue
    if issubclass(v, library.Interface):
        setattr(library, k, v)

