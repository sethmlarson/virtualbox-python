import os
import sys
import platform
import copy
from multiprocessing import current_process
from threading import current_thread
from library_ext import library

__doc__ = library.__doc__

VirtualBox = library.IVirtualBox
Session = library.ISession


def import_vboxapi():
    """This import is designed to help support when loading vboxapi inside of
    alternative Python environments (virtualenvs etc).

    return vboxapi module
    """
    try:
        import vboxapi
    except ImportError:
        system = platform.system()
        py_mm_ver = sys.version_info[:2]
        packages = ['vboxapi']
        if system == 'Windows':
            packages.append('win32com')
            search = [
                        'C:\\Python%s%s\\Lib\\site-packages' % py_mm_ver,
                        'C:\\Program Files\\Oracle\\VirtualBox\\sdk\\install',
                     ]
        elif system == 'Linux':
            search = [
                        '/usr/lib/python%s.%s/dist-packages' % py_mm_ver,
                        '/usr/share/pyshared',
                     ]
        elif system == 'Darwin':
            search = [
                        '/Library/Python/%s.%s/site-packages' % py_mm_ver,
                     ]
        else:
            # No idea where to look...
            raise
        original_path = copy.copy(sys.path)
        for path in search:
            listing = os.listdir(path)
            for package in packages:
                if package in listing:
                    packages.remove(package)
                    sys.path.append(path)
            if not packages:
                break
        else:
            raise
        import vboxapi
        sys.path = original_path
    return vboxapi


_manager = {} 
class Manager(object):
    @property
    def manager(self):
        """Create a default Manager object
        
        Builds a singleton VirtualBoxManager object.

        Note: It is not necessary to build this object when defining a
        Session or VirtualBox object as both of these classes will default
        to this object's global singleton during construction. 
        """
        global _manager
        pid = current_process().ident
        if pid not in _manager:
            vboxapi = import_vboxapi()
            _manager[pid] = vboxapi.VirtualBoxManager(None, None)
        return _manager[pid]

    def get_virtualbox(self):
        """Return a VirtualBox interface"""
        return VirtualBox(interface=self.manager.getVirtualBox())

    def get_session(self):
        """Return a Session interface"""
        # The inconsistent vboxapi implementation makes this annoying...
        if hasattr(self.manager, 'mgr'):
            manager = getattr(self.manager, 'mgr')
        else:
            manager = self.manager
        return Session(interface=manager.getSessionObject(None))

    def cast_object(self, interface_object, interface_class):
        """Cast the obj to the interface class"""
        name = interface_class.__name__
        i = self.manager.queryInterface(interface_object._i, name)
        return interface_class(interface=i)

    @property
    def bin_path(self):
        """return the virtualbox install directory"""
        return self.manager.getBinDir()


class WebServiceManager(Manager):
    def __init__(url='http://localhost/', user='', password=''):
        """Create a VirtualBoxManager WEBSERVICE manager for IVirtualBox
        
        Options:
            url - url to connect with the VirtualBox server 
            user - username used to auth to the VirtualBox server service
            password - password used to auth to the VirtualBox server service

        Example:
            manager = WebServiceManager(user="mick", password="password")
            vbox = VirtualBox(manager=manager)
            ...
        """
        vboxapi = import_vboxapi()
        params = (url, user, password)
        self.manager = vboxapi.VirtualBoxManager("WEBSERVICE", params)

