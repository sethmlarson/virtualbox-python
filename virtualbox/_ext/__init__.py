"""
 This module is responsible for shimming out the auto generated libraries found
 under library.py.  The intension for the extension classes is to fix up or
 improve on the default COM API behaviour and auto generated Python library
 file when interacting through an Interface to the Main library API.
"""

from .vbox import IVirtualBox  # noqa: F401
from .session import ISession  # noqa: F401
from .keyboard import IKeyboard  # noqa: F401
from .guest_session import IGuestSession  # noqa: F401
from .guest import IGuest  # noqa: F401
from .host import IHost  # noqa: F401
from .machine import IMachine  # noqa: F401
from .progress import IProgress  # noqa: F401
from .console import IConsole  # noqa: F401
from .event_source import IEventSource  # noqa: F401
from .mouse import IMouse  # noqa: F401
from .process import IProcess  # noqa: F401
from .guest_process import IGuestProcess  # noqa: F401
from .appliance import IAppliance  # noqa: F401
from .virtual_system_description import IVirtualSystemDescription  # noqa: F401
