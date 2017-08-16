"""
Add helper code to the default IConsole class.
"""

from __future__ import print_function
from virtualbox import library


class IConsole(library.IConsole):
    __doc__ = library.IConsole.__doc__

    # TODO: Where do these events exist in 5x ?
    def register_on_network_adapter_changed(self, callback):
        """Set the callback function to consume on network adapter changed
        events.

        Callback receives a INetworkAdapterChangedEvent object.

        Returns the callback_id
        """
        event_type = library.VBoxEventType.on_network_adapter_changed
        return self.event_source.register_callback(callback, event_type)

    def register_on_serial_port_changed(self, callback):
        """Set the callback function to consume on serial port changed events.

        Callback receives a ISerialPortChangedEvent object.

        Returns the callback_id
        """
        event_type = library.VBoxEventType.on_serial_port_changed
        return self.event_source.register_callback(callback, event_type)

    def register_on_parallel_port_changed(self, callback):
        """Set the callback function to consume on serial port changed events.

        Callback receives a IParallelPortChangedEvent object.

        Returns the callback_id
        """
        event_type = library.VBoxEventType.on_parallel_port_changed
        return self.event_source.register_callback(callback, event_type)

    def register_on_medium_changed(self, callback):
        """Set the callback function to consume on medium changed events.

        Callback receives a IMediumChangedEvent object.

        Returns the callback_id
        """
        event_type = library.VBoxEventType.on_medium_changed
        return self.event_source.register_callback(callback, event_type)

    def register_on_clipboard_mode_changed(self, callback):
        """Set the callback function to consume on clipboard mode changed
        events.

        Callback receives a IClipboardModeChangedEvent object.

        Returns the callback_id
        """
        event_type = library.VBoxEventType.on_clipboard_mode_changed
        return self.event_source.register_callback(callback, event_type)

    def register_on_drag_and_drop_mode_changed(self, callback):
        """Set the callback function to consume on drag and drop mode changed
        events.

        Callback receives a IDragAndDropModeChangedEvent object.

        Returns the callback_id
        """
        event_type = library.VBoxEventType.on_drag_and_drop_mode_changed
        return self.event_source.register_callback(callback, event_type)

    def register_on_vrde_server_changed(self, callback):
        """Set the callback function to consume on VirtualBox Remote Desktop
        Extension (VRDE) changed events.

        Callback receives a IVRDEServerChangedEvent object.

        Returns the callback_id
        """
        event_type = library.VBoxEventType.on_vrde_server_changed
        return self.event_source.register_callback(callback, event_type)

    def register_on_shared_folder_changed(self, callback):
        """Set the callback function to consume on shared folder changed events.

        Callback receives a ISharedFolderChangedEvent object.

        Returns the callback_id
        """
        event_type = library.VBoxEventType.on_shared_folder_changed
        return self.event_source.register_callback(callback, event_type)

    def register_on_additions_state_changed(self, callback):
        """Set the callback function to consume on additions state changed
        events.

        Callback receives a IAdditionsStateChangedEvent object.

        Note: Interested callees should query IGuest attributes to find out
              what has changed.

        Returns the callback_id
        """
        event_type = library.VBoxEventType.on_additions_state_change
        return self.event_source.register_callback(callback, event_type)

    def register_on_state_changed(self, callback):
        """Set the callback function to consume on state changed events
        which are generated when the state of the machine changes.

        Callback receives a IStateChangeEvent object.

        Returns the callback_id
        """
        event_type = library.VBoxEventType.on_state_changed
        return self.event_source.register_callback(callback, event_type)

    def register_on_event_source_changed(self, callback):
        """Set the callback function to consume on event source changed
        events.  This occurs when a listener is added or removed.

        Callback receives a IEventStateChangedEvent object.

        Returns the callback_id
        """
        event_type = library.VBoxEventType.on_event_source_changed
        return self.event_source.register_callback(callback, event_type)

    def register_on_can_show_window(self, callback):
        """Set the callback function to consume on can show window events.
        This occurs when the console window is to be activated and brought to
        the foreground of the desktop of the host PC.  If this behaviour is
        not desired a call to event.add_veto will stop this from happening.

        Callback receives a ICanShowWindowEvent object.

        Returns the callback_id
        """
        event_type = library.VBoxEventType.on_can_show_window
        return self.event_source.register_callback(callback, event_type)

    def register_on_show_window(self, callback):
        """Set the callback function to consume on show window events.
        This occurs when the console window is to be activated and brought to
        the foreground of the desktop of the host PC.

        Callback receives a IShowWindowEvent object.

        Returns the callback_id
        """
        event_type = library.VBoxEventType.on_show_window
        return self.event_source.register_callback(callback, event_type)
