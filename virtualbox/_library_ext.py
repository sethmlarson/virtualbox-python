import inspect
import time

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

    def execute(self, command, arguments=[], stdin="", environment=[],
                 flags=[library.ProcessCreateFlag.wait_for_std_err,
                        library.ProcessCreateFlag.wait_for_std_out,
                        library.ProcessCreateFlag.ignore_orphaned_processes],
                 priority=library.ProcessPriority.default,
                 affinity=[], timeout_ms=0):
        """Execute a command in the Guest

            Arguments:
                command - Command to execute.
                arguments - List of arguments for the command
                stdin - A buffer to write to the stdin of the command.
                environment - See IGuestSession.create_process?
                flags - List of ProcessCreateFlag objects.  
                    Default value set to [wait_for_std_err, 
                                          wait_for_stdout,
                                          ignore_orphaned_processes]
                timeout_ms - ms to wait for the process to complete.  
                    If 0, wait for ever... 
                priority - Set the ProcessPriority priority to be used for
                    execution.
                affinity - Process affinity to use for execution. 

            Return IProcess, stdout, stderr 
        """
        def read_out(process, flags, stdout, stderr):
            if library.ProcessCreateFlag.wait_for_std_err in flags:
                e = process.read(2, 65000, 0)
                stderr.append(e)
            if library.ProcessCreateFlag.wait_for_std_out in flags:
                o = process.read(1, 65000, 0)
                stdout.append(o)

        process = self.process_create_ex(command, arguments, environment,
                            flags, timeout_ms, priority, affinity)
        process.wait_for(int(library.ProcessWaitResult.start), 0)

        # write stdin to the process 
        if stdin:
            index = 0
            while index < len(stdin):
                index += process.write(0, [library.ProcessInputFlag.none], 
                                        stdin[index:], 0)
            process.write(0, [library.ProcessInputFlag.end_of_file], 0)

        # read the process output and wait for 
        stdout = []
        stderr = []
        while process.status == library.ProcessStatus.started:
            read_out(process, flags, stdout, stderr)
            time.sleep(0.2)
        # make sure we have read the remainder of the out
        read_out(process, flags, stdout, stderr)
        return process, "".join(stdout), "".join(stderr)


# Define some default params for create session 
class IGuest(library.IGuest):
    __doc__ = library.IGuest.__doc__
    def create_session(self, user, password, domain='', session_name='pyvbox',
                        timeout_ms=0):
        session = super(IGuest, self).create_session(user, password, domain,
                                                    session_name)
        if timeout_ms != 0:
            # There is probably a better way to to this?
            if 'win' in self.os_type_id.lower():
                test_file = 'C:\\autoexec.bat'
            else:
                test_file = '/bin/sh'
            while True:
                try:
                    session.file_query_info(test_file)
                except library.VBoxError as err:
                    time.sleep(0.5)
                    timeout_ms -= 500
                    if timeout_ms <= 0:
                        raise
                    continue
                break
        return session
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

