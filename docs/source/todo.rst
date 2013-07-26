Outstanding TODOs
=================

Link remaining event types to event sources.
--------------------------------------------
Need to figure out which event sources each of these events types belong to::

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


VirtualBox.nat_networks fails.
------------------------------

Attempting to get the NATNetworks from the VirtualBox object is failing.
Need to debug this to figure out if the wrong COM name has been documented,
or if there is a genuine bug in the API...




