

import virtualbox
from virtualbox import manage
from virtualbox import library


class Path(object):
    def __init__(self):
        self.os = self

    @property
    def sep(self):
        if self.os.name == 'nt':
            return '\\'
        else:
            return '/'

    def join(self, a, *p):
        """Join two or more pathname components, inserting the correct sep
        for the guest operating system"""
        raise NotImplementedError()

    def exists(self, guest_path):
        """test whether a path exists."""
        raise NotImplementedError()


class Network(object):
    def __init__(self):
        self.os = self

    def ifconfig(self):
        """get the networking interface configuration"""
        raise NotImplementedError()

    def netstat(self):
        """return the network status"""
        raise NotImplementedError()


class OperatingSystem(object):
    def __init__(self, session):
        self._s = session
        self.path = Path(self)
        self.network = Network(self)

    def walk(self, top, topdown=True):
        """walk the guest directory tree"""
        raise NotImplementedError()

    @property
    def name(self):
        """return the name of the os. nt or possix"""
        raise NotImplementedError()

    def execute(self, *a, **k):
        """execute a command"""
        raise NotImplementedError()

    def copyfrom(self, to_host_path, from_guest_path, recurse=False):
        """copy file(s) to host path from guest path"""
        raise NotImplementedError()

    def copyto(self, from_host_path, to_guest_path, recurse=False):
        """copy file(s) from host path to guest path"""
        raise NotImplementedError()

    def makedirs(self, guest_path):
        """make the dirs for the given path"""
        raise NotImplementedError()

    def kill(self, pid):
        """kill the process for pid"""
        raise NotImplementedError()

    def ps(self):
        """return a process listing"""
        raise NotImplementedError()

    def stat(self, guest_path):
        """perform a stat system call on the given path"""
        raise NotImplementedError()


class Machine(library.IMachine):
    def __init__(self, machine, session):
        self._i = machine._i
        self._s = session
        self.os = OperatingSystem(session)

    def close(self):
        """close this machine session"""
        self._s.unlock_machine()


class Pool(object):
    def __init__(self, name, 
                vm_image_root=None,         
                
            ):
        self._name = name           
        self._update_pool()

    def _update_pool(self):
        # load configuration for pool
    
    def open(self, block=True):
        """get a Machine resource from the pool"""
        vbox = virtualbox.VirtualBox()
        for vm in vbox.machines:
            if not vm.name.startswtih(self._name):
                continue
            if not '_pool_' in vm.name:
                continue
            # check state, acquire resource
            if vm.machine_state ???
                #

        return Machine(machine, session)

