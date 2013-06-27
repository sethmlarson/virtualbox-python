import inspect

from virtualbox import library

import vboxapi
manager = vboxapi.VirtualBoxManager(None, None)

"""
 This module is responsible for bootstrapping the COM interfaces into the 
 VirthalBox and Session class interfaces.

 It is also the place to fix up or improve on default COM API behaviour
 when interacting through an Interface to the Main library API.
"""


# Import the IKeyboard extension class object
from virtualbox._keyboard_ext import IKeyboard


# Add context management to IGuestSession
class IGuestSession(library.IGuestSession):
    __doc__ = library.IGuestSession.__doc__
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.close()
        

# Define some default params for create session 
class IGuest(library.IGuest):
    __doc__ = library.IGuest.__doc__
    def create_session(self, user, password, domain='', session_name='pyvbox'):
        return super(IGuest, self).create_session(user, password, domain,
                                                    session_name)
    create_session.__doc__ = library.IGuest.create_session.__doc__


# Configure ISession bootstrap to build from vboxapi getSessionObject
class ISession(library.ISession):
    __doc__ = library.ISession.__doc__
    def __init__(self, interface=None):
        if interface is None:
            self._i = manager.platform.getSessionObject(None)
        else:
            self._i = interface
    
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.unlock_machine()


# Configure IVirtualBox bootstrap to build from vboxapi getVirtualBox
class IVirtualBox(library.IVirtualBox):
    __doc__ = library.IVirtualBox.__doc__
    def __init__(self, interface=None):
        if interface is None:
            self._i = manager.getVirtualBox()
        else:
            self._i = interface


# Extend and fix IMachine :) 
class IMachine(library.IMachine):
    __doc__ = library.IMachine.__doc__

    # Fix a what seems to be a buggy definition for deleting machine config
    # Testing showed that deleteConfig was just 'delete'
    _delete_config = 'delete'

    # Add a helper to make locking and building a session simple
    def create_session(self, lock_type=library.LockType.shared,
                   session=None):
        """Lock this machine
        
        Arguments:
            lock_type - see IMachine.lock_machine for details
            session - optionally define a session object to lock this machine 
                      against.  If not defined, a new ISession object is 
                      created to lock against
        
        return an ISession object
        """ 
        if session is None:
            session = library.ISession()
        self.lock_machine(session, lock_type)
        return session


# Helper function for IProgress to print out a current progress state
# in __str__ 
_progress_template = """\
(%(o)s/%(oc)s) %(od)s %(p)-3s%% (%(tr)s s remaining)"""
class IProgress(library.IProgress):
    __doct__ = library.IProgress.__doc__

    def __str__(self):
       return _progress_template % dict(o=self.operation, p=self.percent,
               oc=self.operation_count, od=self.operation_description, 
               tr=self.time_remaining)


# Replace original with extension
for k, v in locals().items():
    if not inspect.isclass(v):
        continue
    if issubclass(v, library.Interface):
        setattr(library, k, v)

