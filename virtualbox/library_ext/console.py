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

    def set_on_network_adapter_changed(self, callback):
        """Set the callback function to consume on network adapter changed
        events.

        Callback receives a INetworkAdapterChangedEvent object.

        Example:
            def callback(event):
                adapter = event.network_adapter
                print("Enabled = %s, connected = %s" % (adapter.enabled,
                                    adapter.cable_connected))
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_network_adapter_changed)


    def set_on_additions_state_changed(self, callback):
        """Set the callback function to consume on additions state changed
        events.

        Callback receives a IAdditionsStateChangedEvent object.

        Note: Interested callees should query IGuest attributes to find out
              what has changed.

        Example:
            def callback(event):
                print("change...")
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_additions_state_change)

    def set_on_state_changed(self, callback):
        """Set the callback function to consume on state changed events
        which are generated when the state of the machine changes.

        Callback receives a IStateChangeEvent object.

        Example:
            def callback(event):
                print("State changed to %s" % event.state)
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_state_changed)



