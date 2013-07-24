import virtualbox
from virtualbox import library

"""
Add helper code to the default ISession class.
"""

# Configure ISession bootstrap to build from vboxapi getSessionObject
class ISession(library.ISession):
    __doc__ = library.ISession.__doc__
    def __init__(self, interface=None, manager=None):
        if interface is not None:
            super(ISession, self).__init__(interface)
        elif manager is not None:
            self._i = manager.get_session()._i
        else:
            manager = virtualbox.Manager()
            self._i = manager.get_session()._i
    
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.unlock_machine()
