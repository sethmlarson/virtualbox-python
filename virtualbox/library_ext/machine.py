from __future__ import print_function
import time
import sys

import virtualbox
from virtualbox import library

"""
Add helper code to the default IMachine class.
"""


# Extend and fix IMachine :) 
class IMachine(library.IMachine):
    __doc__ = library.IMachine.__doc__

    def __str__(self):
        return self.name

    def remove(self, delete=True):
        """Unregister and optionally delete associated config

        Options:
            delete - remove all elements of this VM from the system

        Return the IMedia from unregistered VM 
        """
        if self.state >= library.MachineState.running:
            session = virtualbox.Session()
            self.lock_machine(session, LockType.shared)
            try:
                progress = session.console.power_down()
                progress.wait_for_completion(-1)
            except Exception as exc:
                print("Error powering off machine %s" % progress, 
                                            file=sys.stderr)
                pass
            session.unlock_machine()
            time.sleep(0.5) # TODO figure out how to ensure session is 
                            # really unlocked...
        if delete:
            option = library.CleanupMode.detach_all_return_hard_disks_only
        else:
            option = library.CleanupMode.detach_all_return_none
        media = self.unregister(option)
        if delete:
            progress = self.delete_config(media)
            progress.wait_for_completion(-1)
            media = []
        return media

    # Fix a what seems to be a buggy definition for deleting machine config
    # Testing showed that deleteConfig was just 'delete'
    def delete_config(self, media):
        if not isinstance(media, list):
            raise TypeError("media can only be an instance of type list")
        for a in media[:10]:
            if not isinstance(a, IMedium):
                raise TypeError(\
                        "array can only contain objects of type IMedium")
        progress = self._call("delete", in_p=[media])
        progress = IProgress(progress)
        return progress
    delete_config.__doc__ = library.IMachine.delete_config.__doc__

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

    # Simplify the launch_vm_process. Build a ISession if it has not been 
    # defined... 
    def launch_vm_process(self, session=None, type_p='gui', environment=''):
        if session is None:
            local_session = library.ISession()
        else:
            local_session = session
        p = super(IMachine, self).launch_vm_process(local_session, 
                                                    type_p, environment)
        if session is None:
            p.wait_for_completion(-1)
            local_session.unlock_machine()
        return p
    launch_vm_process.__doc__ = library.IMachine.launch_vm_process.__doc__



