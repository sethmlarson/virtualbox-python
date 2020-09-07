from virtualbox import library
from virtualbox.library_ext.progress import IProgress


class IHost(library.IHost):
    __doc__ = library.IHost.__doc__

    # Work around a bug where createHostOnlyNetworkInterface returns
    # host_interface and progress in the wrong order
    def create_host_only_network_interface(self):
        progress, host_interface = self._call("createHostOnlyNetworkInterface")
        host_interface = library.IHostNetworkInterface(host_interface)
        progress = IProgress(progress)
        return host_interface, progress

    create_host_only_network_interface.__doc__ = (
        library.IHost.create_host_only_network_interface.__doc__
    )
