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
from __future__ import absolute_import
from contextlib import contextmanager
import os
import sys
import platform
import copy
import atexit
from multiprocessing import current_process

from virtualbox.library_ext import library
from .__about__ import (
    __title__,  # noqa: F401
    __version__,
    __author__,
    __author_email__,
    __maintainer__,
    __maintainer_email__,
    __license__,
    __url__,
)


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
        py_major = sys.version_info[0]
        packages = ["vboxapi"]

        if system == "Windows":
            packages.extend(
                ["win32com", "win32", "win32api", "pywintypes", "win32comext"]
            )
            search = [
                "C:\\Python%s%s\\Lib\\site-packages" % py_mm_ver,
                "C:\\Python%s%s\\Lib\\site-packages\\win32" % py_mm_ver,
                "C:\\Python%s%s\\Lib\\site-packages\\win32\\lib" % py_mm_ver,
                "C:\\Program Files\\Oracle\\VirtualBox\\sdk\\install",
                "C:\\Program Files (x86)\\Oracle\\VirtualBox\\sdk\\install",
            ]

            for x in ["", py_major]:
                search.extend(
                    [
                        "C:\\Anaconda%s\\Lib\\site-packages" % x,
                        "C:\\Anaconda%s\\Lib\\site-packages\\win32" % x,
                        "C:\\Anaconda%s\\Lib\\site-packages\\win32\\lib" % x,
                    ]
                )

        elif system == "Linux":
            search = [
                "/usr/lib/python%s.%s/dist-packages" % py_mm_ver,
                "/usr/lib/python%s.%s/site-packages" % py_mm_ver,
                "/usr/share/pyshared",
            ]

        elif system == "Darwin":
            search = ["/Library/Python/%s.%s/site-packages" % py_mm_ver]
        else:
            # No idea where to look...
            search = []

        # Generates a common prefix from sys.executable in the
        # case that vboxapi is installed in a virtualenv.
        # This will also help with when we don't know where
        # to search because of an unknown platform.
        # These paths also help if the system Python is installed
        # in a non-standard location.
        #
        # NOTE: We don't have to worry if these directories don't
        # exist as they're checked below.
        prefix = os.path.dirname(os.path.dirname(sys.executable))
        search.extend(
            [
                os.path.join(prefix, "Lib", "site-packages"),
                os.path.join(prefix, "Lib", "site-packages", "win32"),
                os.path.join(prefix, "Lib", "site-packages", "win32", "lib"),
                os.path.join(prefix, "lib", "site-packages"),
                os.path.join(prefix, "lib", "dist-packages"),
            ]
        )

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


_managers = {}


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
        if _managers is None:
            raise RuntimeError("Can not create a new manager following a system exit.")
        if pid not in _managers:
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
        if _managers is None:
            raise RuntimeError("Can not get the manager following a system exit.")
        return _managers[current_process().ident]

    @manager.setter
    def manager(self, value):
        "Set the manager object in the global _managers dict."
        pid = current_process().ident
        if _managers is None:
            raise RuntimeError("Can not set the manager following a system exit.")
        if pid not in _managers:
            _managers[pid] = value
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
        if hasattr(self.manager, "mgr"):
            manager = getattr(self.manager, "mgr")
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


# Attempt to close left over manager objects cleanly.
def _cleanup_managers():
    global _managers
    managers = _managers
    _managers = None
    for manager in managers.values():
        try:
            del manager
        except Exception:
            pass
    managers.clear()


atexit.register(_cleanup_managers)


class WebServiceManager(Manager):
    """The WebServiceManager extends the base Manager to include the ability
    to build a WEBSERVICE type vboxapi interface.
    """

    def __init__(self, url="http://localhost/", user="", password=""):
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
        params = {"url": url, "user": user, "password": password}
        super(WebServiceManager, self).__init__("WEBSERVICE", params)


# Lazy include...
from . import pool  # noqa: F401
from . import events  # noqa: F401
from . import library as lib  # noqa: F401
