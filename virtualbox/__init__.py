"""Virtualbox API wrapper and Reference

By Michael Dorman
[mjdorma+pyvbox@gmail.com]
"""
from __future__ import absolute_import
from contextlib import contextmanager
import os
import sys
import platform
import copy
from multiprocessing import current_process
from threading import current_thread

from virtualbox.library_ext import library


# Adopt on the library API root documentation
__doc__ = library.__doc__


VirtualBox = library.IVirtualBox
Session = library.ISession

@contextmanager
def import_vboxapi():
    """This import is designed to help when loading vboxapi inside of
    alternative Python environments (virtualenvs etc).

    :rtype: vboxapi module
    """
    try:
        import vboxapi
    except ImportError:
        system = platform.system()
        py_mm_ver = sys.version_info[:2]
        packages = ['vboxapi']
        if system == 'Windows':
            packages.extend(['win32com', 'win32', 'win32api', 'pywintypes', 'win32comext'])
            search = [
                        'C:\\Python%s%s\\Lib\\site-packages' % py_mm_ver,
                        'C:\\Python%s%s\\Lib\\site-packages\\win32' % py_mm_ver,
                        'C:\\Python%s%s\\Lib\\site-packages\\win32\\lib' % py_mm_ver,
                        'C:\\Program Files\\Oracle\\VirtualBox\\sdk\\install',
                        'C:\\Program Files (x86)\\Oracle\\VirtualBox\\sdk\\install',
                     ]
        elif system == 'Linux':
            search = [
                        '/usr/lib/python%s.%s/dist-packages' % py_mm_ver,
                        '/usr/lib/python%s.%s/site-packages' % py_mm_ver,
                        '/usr/share/pyshared',
                     ]
        elif system == 'Darwin':
            search = [
                        '/Library/Python/%s.%s/site-packages' % py_mm_ver,
                     ]
        else:
            # No idea where to look...
            raise
        packages = set(packages)
        original_path = copy.copy(sys.path)
        for path in search:
            if not os.path.isdir(path):
                continue
            listing = set([os.path.splitext(f)[0] for f in os.listdir(path)])
            if packages.intersection(listing):
                sys.path.append(path)
            packages -= listing
            if not packages:
                break
        else:
            # After search each path we still failed to find 
            # the required set of packages.
            raise
        import vboxapi
        try:
            yield vboxapi
        finally:
            sys.path = original_path
    else:
        yield vboxapi


_manager = {} 
class Manager(object):
    """The Manager maintains a single point of entry into vboxapi.
    
    This object is responsible for the construction of
    :py:class:`virtualbox.library_ext.ISession` and
    :py:class:`virtualbox.library_ext.IVirtualBox`.  

    :param mtype: Type of manager i.e. WEBSERVICE.
    :type mtype: str (Default None)
    :param mparams: The params that the mtype manager object accepts.
    :type mparams: tuple|list (Default None)
    """
    def __init__(self, mtype=None, mparams=None):
        pid = current_process().ident
        if pid not in _manager:
            with import_vboxapi() as vboxapi:
                self.manager = vboxapi.VirtualBoxManager(mtype, mparams)

    @property
    def manager(self):
        """Create a default Manager object
        
        Builds a singleton VirtualBoxManager object.

        Note: It is not necessary to build this object when defining a
        Session or VirtualBox object as both of these classes will default
        to this object's global singleton during construction. 
        """
        return _manager[current_process().ident]

    @manager.setter
    def manager(self, value):
        "Set the manager object in the global _manager dict."
        pid = current_process().ident
        if pid not in _manager:
            _manager[pid] = value 
        else:
            raise Exception("Manager already set for pid %s" % pid)

    def get_virtualbox(self):
        """Return a VirtualBox interface
        
        :rtype: library.IVirtualBox
        """
        return VirtualBox(interface=self.manager.getVirtualBox())

    def get_session(self):
        """Return a Session interface
        
        :rtype: library.ISession
        """
        # The inconsistent vboxapi implementation makes this annoying...
        if hasattr(self.manager, 'mgr'):
            manager = getattr(self.manager, 'mgr')
        else:
            manager = self.manager
        return Session(interface=manager.getSessionObject(None))

    def cast_object(self, interface_object, interface_class):
        """Cast the obj to the interface class
        
        :rtype: interface_class(interface_object)
        """
        name = interface_class.__name__
        i = self.manager.queryInterface(interface_object._i, name)
        return interface_class(interface=i)

    @property
    def bin_path(self):
        """return the virtualbox install directory
        
        :rtype: str
        """
        return self.manager.getBinDir()


class WebServiceManager(Manager):
    """The WebServiceManager extends the base Manager to include the ability
    to build a WEBSERVICE type vboxapi interface.
    """
    def __init__(self, url='http://localhost/', user='', password=''):
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
        params = (url, user, password)
        super(WebServiceManager, self).__init__("WEBSERVICE", params)


# Lazy include...
from virtualbox import pool
from virtualbox import events
from virtualbox import version
