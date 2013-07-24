import virtualbox
from virtualbox import library

"""
Add helper code to the default ISession class.
"""

# Configure IVirtualBox bootstrap to build from vboxapi getVirtualBox
class IVirtualBox(library.IVirtualBox):
    __doc__ = library.IVirtualBox.__doc__
    def __init__(self, interface=None, manager=None):
        if interface is not None:
            super(IVirtualBox, self).__init__(interface)
        elif manager is not None:
            self._i = manager.get_virtualbox()._i
        else:
            manager = virtualbox.Manager()
            self._i = manager.get_virtualbox()._i

    def set_on_snapshot_deleted(self, callback):
        """Set the callback function to consume on snapshot deleted events.

        Callback receives a ISnapshotDeletedEvent object.

        Example:
            def callback(event):
                print(event.snapshot_id)
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_snapshot_deleted)

    def set_on_snapshot_taken(self, callback):
        """Set the callback function to consume on snapshot taken events.

        Callback receives a ISnapshotTakenEvent object.

        Example:
            def callback(event):
                print(event.snapshot_id)
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_snapshot_taken)

    def set_on_snapshot_changed(self, callback):
        """Set the callback function to consume on snapshot changed events
        which occur when snapshot properties have been changed.

        Callback receives a ISnapshotDeleteEvent object.

        Example:
            def callback(event):
                print(event.snapshot_id)
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_snapshot_changed)


