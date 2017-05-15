"""
Add helper code to the default IMouse class.
"""

from virtualbox import library


class IMouse(library.IMouse):
    __doc__ = library.IMouse.__doc__

    def register_on_guest_mouse(self, callback):
        """Set the callback function to consume on guest mouse events.

        Callback receives a IGuestMouseEvent object.

        Example:
            def callback(event):
                print(("%s %s %s" % (event.x, event.y, event.z))
        """
        event_type = library.VBoxEventType.on_guest_mouse
        return self.event_source.register_callback(callback, event_type)
