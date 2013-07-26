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

    def register_on_snapshot_deleted(self, callback):
        """Set the callback function to consume on snapshot deleted events.

        Callback receives a ISnapshotDeletedEvent object.

        Returns the callback_id 
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_snapshot_deleted)

    def register_on_snapshot_taken(self, callback):
        """Set the callback function to consume on snapshot taken events.

        Callback receives a ISnapshotTakenEvent object.
        
        Returns the callback_id 
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_snapshot_taken)

    def register_on_snapshot_changed(self, callback):
        """Set the callback function to consume on snapshot changed events
        which occur when snapshot properties have been changed.

        Callback receives a ISnapshotChangedEvent object.
        
        Returns the callback_id 
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_snapshot_changed)

    def register_on_guest_property_changed(self, callback):
        """Set the callback function to consume on guest property changed 
        events.

        Callback receives a IGuestPropertyChangedEvent object.
        
        Returns the callback_id 
        """
        return self.event_source.register_callback(callback,
                            library.VBoxEventType.on_guest_property_changed)


