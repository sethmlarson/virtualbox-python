"""Virtualbox API wrapper and Reference

Copyright (c) 2013 Michael Dorman (mjdorma@gmail.com). All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from .__about__ import (__name__,  # noqa: F401
                        __version__,
                        __author__,
                        __email__,
                        __license__,
                        __url__)


from ._library import __doc__  # noqa F401
from ._vboxapi import Manager, WebServiceManager  # noqa: F401
from ._library import (AccessMode, AdditionsFacility, AdditionsFacilityClass, AdditionsFacilityStatus,  # noqa: F401
                       AdditionsFacilityType, AdditionsRunLevelType, AdditionsStateChangedEvent,
                       AdditionsUpdateFlag, APICMode, AudioAdapter, AudioCodecType, AudioControllerType,
                       AudioDriverType, AuthType, AutostopType, BandwidthControl, BandwidthGroup,
                       BandwidthGroupChangedEvent, BandwidthGroupType, BIOSBootMenuMode, BIOSSettings,
                       BitmapFormat, ClipboardMode, CleanupMode, CanShowWindowEvent, Certificate,
                       CertificateVersion, ChipsetType, ClipboardModeChangedEvent, CloneMode, CloneOptions,
                       CPUChangedEvent, CPUExecutionCapChangedEvent, CPUPropertyType, DataFlags, DataType,
                       DeviceActivity, DeviceType, DhcpOpt, DhcpOptEncoding, DHCPServer, Directory,
                       DirectoryCopyFlags, DirectoryCreateFlag, DirectoryOpenFlag, DirectoryRemoveRecFlag,
                       Display, DisplaySourceBitmap, DragAndDropAction, DragAndDropBase, DragAndDropMode,
                       DragAndDropModeChangedEvent, DragAndDropSource, DragAndDropTarget, EmulatedUSB,
                       Event, EventListener, EventSourceChangedEvent, ExportOptions, ExtPack, ExtPackBase,
                       ExtPackFile, ExtPackManager, ExtPackPlugIn, ExtraDataCanChangeEvent, ExtraDataChangedEvent,
                       FaultToleranceState, File, FileAccessMode, FileCopyFlag, FileOpenAction, FileOpenExFlags,
                       FileSeekOrigin, FileSharingMode, FileStatus, FirmwareType, Framebuffer,
                       FramebufferCapabilities, FramebufferOverlay, FsObjInfo, FsObjMoveFlags, FsObjRenameFlag,
                       FsObjType, GraphicsControllerType, GuestDirectory, GuestDragAndDropSource,
                       GuestDragAndDropTarget, GuestFile, GuestFileEvent, GuestFileIOEvent, GuestFileOffsetChangedEvent,
                       GuestFileReadEvent, GuestFileRegisteredEvent, GuestFileStateChangedEvent, GuestFileWriteEvent,
                       GuestFsObjInfo, GuestKeyboardEvent, GuestMonitorChangedEvent, GuestMonitorChangedEventType,
                       GuestMonitorStatus, GuestMouseEvent, GuestMouseEventMode, GuestMultiTouchEvent,
                       GuestOSType, GuestProcessEvent, GuestProcessInputNotifyEvent, GuestProcessIOEvent,
                       GuestProcessOutputEvent, GuestProcessRegisteredEvent, GuestProcessStateChangedEvent,
                       GuestPropertyChangedEvent, GuestScreenInfo, GuestSessionEvent, GuestSessionRegisteredEvent,
                       GuestSessionStateChangedEvent, GuestSessionStatus, GuestSessionWaitForFlag,
                       GuestSessionWaitResult, GuestUserState, GuestUserStateChangedEvent,
                       HostNameResolutionConfigurationChangeEvent, HostNetworkInterface, HostNetworkInterfaceMediumType,
                       HostNetworkInterfaceStatus, HostNetworkInterfaceType, HostPCIDevicePlugEvent,
                       HostUSBDevice, HostUSBDeviceFilter, HostVideoInputDevice, HardwareVirtExPropertyType,
                       ImportOptions, InternalMachineControl, InternalSessionControl, KeyboardHIDType,
                       KeyboardLED, KeyboardLedsChangedEvent, LockType, MachineDataChangedEvent, MachineDebugger,
                       MachineEvent, MachineRegisteredEvent, MachineState, MachineStateChangedEvent, Medium,
                       MediumAttachment, MediumChangedEvent, MediumConfigChangedEvent, MediumFormat,
                       MediumFormatCapabilities, MediumRegisteredEvent, MediumState, MediumType, MediumVariant,
                       MouseButtonState, MouseCapabilityChangedEvent, MousePointerShape, MousePointerShapeChangedEvent,
                       NetworkAdapterType, NetworkAttachmentType, NATAliasMode, NATEngine, NATNetwork,
                       NATNetworkAlterEvent, NATNetworkChangedEvent, NATNetworkCreationDeletionEvent,
                       NATNetworkPortForwardEvent, NATNetworkSettingEvent, NATNetworkStartStopEvent, NATProtocol,
                       NATRedirectEvent, NetworkAdapter, NetworkAdapterChangedEvent, NetworkAdapterPromiscModePolicy,
                       OleErrorAccessdenied, OleErrorFail, OleErrorInvalidarg, OleErrorNointerface, OleErrorNotimpl,
                       OleErrorUnexpected, ProcessCreateFlag, ProcessStatus, ProcessWaitResult, ProcessPriority,
                       ProcessWaitForFlag, ParallelPort, ParallelPortChangedEvent, ParavirtProvider, PathStyle,
                       PCIAddress, PCIDeviceAttachment, PerformanceCollector, PerformanceMetric, PointingHIDType,
                       PortMode, ProcessInputFlag, ProcessInputStatus, ProcessorFeature, ProcessOutputFlag,
                       Reason, ReusableEvent, RuntimeErrorEvent, SessionState, Scope, ScreenLayoutMode, SerialPort,
                       SerialPortChangedEvent, SessionStateChangedEvent, SessionType, SettingsVersion, SharedFolder,
                       SharedFolderChangedEvent, ShowWindowEvent, Snapshot, SnapshotChangedEvent, SnapshotDeletedEvent,
                       SnapshotEvent, SnapshotRestoredEvent, SnapshotTakenEvent, StateChangedEvent, StorageBus,
                       StorageController, StorageControllerChangedEvent, StorageControllerType,
                       StorageDeviceChangedEvent, SymlinkReadFlag, SymlinkType, SystemProperties, Token,
                       TouchContactState, Unattended, USBConnectionSpeed, USBController, USBControllerChangedEvent,
                       USBControllerType, USBDevice, USBDeviceFilter, USBDeviceFilterAction, USBDeviceFilters,
                       USBDeviceState, USBDeviceStateChangedEvent, USBProxyBackend, VirtualSystemDescription,
                       VBoxError, VBoxErrorFileError, VBoxErrorHostError, VBoxErrorInvalidObjectState,
                       VBoxErrorInvalidSessionState, VBoxErrorInvalidVmState, VBoxErrorIprtError, VBoxErrorNotSupported,
                       VBoxErrorObjectInUse, VBoxErrorObjectNotFound, VBoxErrorPasswordIncorrect, VBoxErrorPdmError,
                       VBoxErrorVmError, VBoxErrorXmlError, VBoxEventType, VBoxSVCAvailabilityChangedEvent, VetoEvent,
                       VFSExplorer, VFSType, VideoCaptureChangedEvent, VirtualBoxClient, VirtualBoxErrorInfo,
                       VirtualSystemDescriptionType, VirtualSystemDescriptionValueType, VRDEServer,
                       VRDEServerChangedEvent, VRDEServerInfo, VRDEServerInfoChangedEvent)
