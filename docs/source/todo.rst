Outstanding TODOs
=================

Events
------

Need to figure out which sources each of these events belong to::

    IStorageControllerChangedEvent
    ICPUChangedEvent
    ICPUExecutionCapChangedEvent

    IGuestSessionStateChangedEvent
    IGuestSessionRegisteredEvent
    IGuestProcessRegisteredEvent
    IGuestProcessStateChangedEvent
    IGuestProcessInputNotifyEvent
    IGuestProcessOutputEvent
    IGuestFileRegisteredEvent
    IGuestFileStateChangedEvent
    IGuestFileOffsetChangedEvent
    IGuestFileWriteEvent

    IVRDEServerInfoChangedEvent
    ICanShowWindowEvent

    IMediumRegisteredEvent

    IKeyboardLedsChangedEvent
    IMouseCapabilityChangedEvent
    IMousePointerShapeChangedEvent

    IUSBControllerChangedEvent
    IUSBDeviceStateChangedEvent
    IRuntimeErrorEvent  <-- this looks useful!

    INATRedirectEvent
    IHostPCIDevicePlugEvent
    IVBoxSVCAvailabilityChangedEvent
    IBandwidthGroupChangedEvent
    IGuestMonitorChangedEvent
    IStorageDeviceChangedEvent
    INATNetworkChangedEvent
    INATNetworkStartStopEvent
    INATNetworkAlterEvent
    INATNetworkCreationDeletionEvent
    INATNetworkSettingEvent
    INATNetworkPortForwardEvent


NATNetworks
-----------

Attempting to get the NATNetworks from the VirtualBox object is failing...
need to debug this and figure out what the COM name is (or if there is a bug
somewhere in vboxapi's xpcom implementation).




