from virtualbox import library

"""
Add helper code to the default IMachine class.
"""


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


