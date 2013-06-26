from virtualbox import library 

"""
 This module contains the extension implementation for the IGuestSession object
"""

class Path(object):
    def __init__(self, os):
        self.os = os

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
    def __init__(self, os):
        self.os = os

    def ifconfig(self):
        """get the networking interface configuration"""
        raise NotImplementedError()

    def netstat(self):
        """return the network status"""
        raise NotImplementedError()


class OperatingSystem(object):
    def __init__(self, machine):
        self._m = machine
        self._s = None
        self.path = Path(self)
        self.network = Network(self)

    def walk(self, top, topdown=True):
        """walk the guest directory tree"""
        raise NotImplementedError()

    @property
    def session(self):
        return None

    @property
    def name(self):
        """return the name of the os. nt or possix"""
        self.session.console.guest.os_type_id
        raise NotImplementedError()

    def execute(self, *a, **k):
        """execute a command"""
        raise NotImplementedError()

    def copyfrom(self, src_host_path, dst_guest_path, recurse=False):
        """copy file(s) to host path from guest path"""
        raise NotImplementedError()

    def copyto(self, src_guest_path, dst_host_path, recurse=False):
        """copy file(s) from host path to guest path"""
        raise NotImplementedError()

    def makedirs(self, guest_path):
        """make the dirs for the given path"""
        raise NotImplementedError()

    def kill(self, guest_pid):
        """kill the process for pid"""
        raise NotImplementedError()

    def ps(self):
        """return a process listing"""
        raise NotImplementedError()

    def stat(self, guest_path):
        """perform a stat system call on the given path"""
        raise NotImplementedError()


class IGuestSession(library.IGuestSession):
    __doc__ = library.IGuestSession.__doc__
    def __init__(self, interface=None):
        self._i = interface 
        self.os = OperatingSystem(self)



