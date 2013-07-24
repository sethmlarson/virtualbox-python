from __future__ import print_function

import virtualbox
from virtualbox import library
from virtualbox import events

"""
Add helper code to the default IEventSource class.
"""

class IEventSource(library.IEventSource):
    __doc__ = library.IEventSource.__doc__

    def register_callback(self, callback, event_type):
        """register a callback function for the provided given event_type"""
        return events.register_callback(callback, self, event_type)

