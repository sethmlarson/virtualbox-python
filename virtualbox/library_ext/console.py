from __future__ import print_function

import virtualbox
from virtualbox import library

"""
Add helper code to the default IConsole class.
"""

class IConsole(library.IConsole):
    __doc__ = library.IConsole.__doc__

    #if no snapshot has been supplied, try using the current_snapshot
    def restore_snapshot(self, snapshot=None):
        if snapshot is None:
            if self.machine.current_snapshot:
                snapshot = self.machine.current_snapshot
            else:
                raise Exception("Machine has no snapshots")
        return super(IConsole, self).restore_snapshot(snapshot)
    restore_snapshot.__doc__ = library.IConsole.restore_snapshot.__doc__

    def register_on_network_adapter_changed(self, callback):
        """Set the callback function to consume on network adapter changed
        events.

        Callback receives a INetworkAdapterChangedEvent object.

        Returns the callback_id 
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_network_adapter_changed)

    def register_on_serial_port_changed(self, callback):
        """Set the callback function to consume on serial port changed events.

        Callback receives a ISerialPortChangedEvent object.

        Returns the callback_id 
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_serial_port_changed)

    def register_on_parallel_port_changed(self, callback):
        """Set the callback function to consume on serial port changed events.

        Callback receives a IParallelPortChangedEvent object.

        Returns the callback_id 
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_parallel_port_changed)

    def register_on_medium_changed(self, callback):
        """Set the callback function to consume on medium changed events.

        Callback receives a IMediumChangedEvent object.

        Returns the callback_id 
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_medium_changed)

    def register_on_clipboard_mode_changed(self, callback):
        """Set the callback function to consume on clipboard mode changed
        events.

        Callback receives a IClipboardModeChangedEvent object.

        Returns the callback_id 
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_clipboard_mode_changed)

    def register_on_drag_and_drop_mode_changed(self, callback):
        """Set the callback function to consume on drag and drop mode changed
        events.

        Callback receives a IDragAndDropModeChangedEvent object.

        Returns the callback_id 
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_drag_and_drop_mode_changed)

    def register_on_vrde_server_changed(self, callback):
        """Set the callback function to consume on VirtualBox Remote Desktop
        Extension (VRDE) changed events.

        Callback receives a IVRDEServerChangedEvent object.

        Returns the callback_id 
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_vrde_server_changed)

    def register_on_shared_folder_changed(self, callback):
        """Set the callback function to consume on shared folder changed events.

        Callback receives a ISharedFolderChangedEvent object.

        Returns the callback_id 
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_shared_folder_changed)

    def register_on_additions_state_changed(self, callback):
        """Set the callback function to consume on additions state changed
        events.

        Callback receives a IAdditionsStateChangedEvent object.

        Note: Interested callees should query IGuest attributes to find out
              what has changed.

        Returns the callback_id 
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_additions_state_change)

    def register_on_state_changed(self, callback):
        """Set the callback function to consume on state changed events
        which are generated when the state of the machine changes.

        Callback receives a IStateChangeEvent object.

        Returns the callback_id 
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_state_changed)


    def register_on_event_source_changed(self, callback):
        """Set the callback function to consume on event source changed
        events.  This occurs when a listener is added or removed.

        Callback receives a IEventStateChangedEvent object.
        
        Returns the callback_id 
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_event_source_changed)

    def register_on_can_show_window(self, callback):
        """Set the callback function to consume on can show window events.  
        This occurs when the console window is to be activated and brought to
        the foreground of the desktop of the host PC.  If this behaviour is
        not desired a call to event.add_veto will stop this from happening. 

        Callback receives a ICanShowWindowEvent object.
        
        Returns the callback_id 
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_can_show_window)

    def register_on_show_window(self, callback):
        """Set the callback function to consume on show window events.  
        This occurs when the console window is to be activated and brought to
        the foreground of the desktop of the host PC.

        Callback receives a IShowWindowEvent object.
        
        Returns the callback_id 
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_show_window)








