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


from ._library import __doc__
from ._ext import (VirtualBox, Session, Keyboard,
                   GuestSession, Guest, Host, Progress,
                   Console, EventSource, Mouse, Process,
                   GuestProcess, Appliance, VirtualSystemDescription)
from ._vboxapi import Manager, WebServiceManager

__all__ = ['VirtualBox', 'Session', 'Keyboard', 'GuestSession', 'EventSource',
           'Appliance', 'VirtualSystemDescription', 'Manager', 'WebServiceManager']
