"""
 This module is responsible for shimming out the auto generated libraries found
 under library.py.  The intension for the extension classes is to fix up or
 improve on the default COM API behaviour and auto generated Python library
 file when interacting through an Interface to the Main library API.
"""

from .vbox import VirtualBox
from .session import Session
from .keyboard import Keyboard
from .guest_session import GuestSession
from .guest import Guest
from .host import Host
from .machine import Machine
from .progress import Progress
from .console import Console
from .event_source import EventSource
from .mouse import Mouse
from .process import Process
from .guest_process import GuestProcess
from .appliance import Appliance
from .virtual_system_description import VirtualSystemDescription

__all__ = ['VirtualBox', 'Session', 'Keyboard', 'GuestSession', 'Guest',
           'Host', 'Machine', 'Process', 'Progress', 'Console',
           'EventSource', 'Mouse', 'GuestProcess', 'Appliance',
           'VirtualSystemDescription']
