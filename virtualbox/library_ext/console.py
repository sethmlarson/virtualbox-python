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



