from __future__ import print_function
import os
import shutil
import tempfile
import sys
import contextlib
import time
import atexit
from threading import Lock

import virtualbox
from virtualbox import library
from virtualbox.library import CloneMode
from virtualbox.library import CloneOptions
from virtualbox.library import CleanupMode 
from virtualbox.library import IMachine
from virtualbox.library import ProcessCreateFlag
from virtualbox.library import ProcessInputFlag
from virtualbox.library import LockType 
from virtualbox.library import MachineState 

"""
 Provide some convenience functions which pull in some of the beauty of
 vboxmanage.
"""


def show_progress(progress, ofile=sys.stderr):
    """Print the current progress out to file"""
    try:
        while not progress.completed:
            print(progress, file=ofile)
            progress.wait_for_completion(1000)
    except KeyboardInterrupt:
        if progress.cancelable:
            progress.cancel()

    print(progress, file=ofile)
    print("Progress state: %s" % progress.result_code, file=ofile)
    if progress.error_info:
        print(progress.error_info.text, file=ofile)


def removevm(machine_or_name_or_id, delete=True):
    """Unregister and optionally delete associated config
    Required:
        machine_or_name_or_id - value can be either IMachine, name, or id   
    Options:
        delete - remove all elements of this VM from the system

    Return the (vm, media) 
    """
    if type(machine_or_name_or_id) in [str, unicode]:
        vbox = virtualbox.VirtualBox()
        vm = vbox.find_machine(machine_or_name_or_id)
    else:
        vm = machine_or_name_or_id

    if vm.state >= MachineState.running:
        session = virtualbox.Session()
        vm.lock_machine(session, LockType.shared)
        try:
            progress = session.console.power_down()
            show_progress(progress)
        except Exception as exc:
            print("Error powering off machine %s" % progress)
            pass
        session.unlock_machine()
        time.sleep(1)

    if delete:
        options = CleanupMode.detach_all_return_hard_disks_only
    else:
        options = CleanupMode.detach_all_return_none
    media = vm.unregister(options)
    if delete:
        progress = vm.delete_config(media)
        show_progress(progress)
        media = []
    return (vm, media)


def startvm(machine_or_name_or_id, session_type='gui', environment=''):
    """Start a VM
    Required:
        machine_or_name_or_id - value can be either IMachine, name, or id
    Options: 
        session_type - 'gui', 'headless', 'sdl', 'emergencystop'
        environment - specify the env for the VM 
            ie.
                NAME[=VALUE]    
                NAME[=VALUE]
                ...

    Return the vm which was just started 
    """
    if type(machine_or_name_or_id) in [str, unicode]:
        vbox = virtualbox.VirtualBox()
        vm = vbox.find_machine(machine_or_name_or_id)
    else:
        vm = machine_or_name_or_id

    session = virtualbox.Session()
    progress = vm.launch_vm_process(session, session_type, environment)
    show_progress(progress)
    session.unlock_machine()
    return vm


_clone_lock = Lock()
def clonevm(machine_or_name_or_id, snapshot_name_or_id=None,
        mode=CloneMode.machine_state, options=[CloneOptions.link],
        name=None, uuid=None, groups=[], basefolder='', register=True):
    """Clone a Machine 

    Required:
        machine_or_name_or_id - value can be either IMachine, name, or id
    Options: 
        snapshot_name_or_id - value can be either ISnapshot, name, or id
        mode - set the CloneMode value
        options - define the CloneOptions options 
        name - define a name of the new VM
        uuid - set the uuid of the new VM
        groups - specify which groups the new VM will exist under
        basefolder - specify which folder to set the VM up under
        register - register this VM with the server
    
    Note: Default values create a linked clone from the current machine state

    Return a IMachine object for the vm 
    """
    with _clone_lock:
        vbox = virtualbox.VirtualBox()
        if type(machine_or_name_or_id) in [str, unicode]:
            vm = vbox.find_machine(machine_or_name_or_id)
        else:
            vm = machine_or_name_or_id

        if snapshot_name_or_id is not None:
            if snapshot_name_or_id in [str, unicode]:
                snapshot = vm.find_snapshot(snapshot_name_or_id)
            else:
                snapshot = snapshot_name_or_id
            vm = snapshot.machine

        if name is None:
            name = "%s Clone" % vm.name

        # Build the settings file 
        create_flags = ''
        if uuid is not None:
            create_flags = "UUID=%s" % uuid
        primary_group = ''
        if groups:
            primary_group = groups[0]
        
        # Make sure this settings file does not already exist
        test_name = name
        for i in range(1, 1000):
            settings_file = vbox.compose_machine_filename(test_name,
                                    primary_group, create_flags, basefolder)
            if not os.path.exists(settings_file):
                break
            test_name = "%s (%s)" % (name, i)
        name = test_name

        # Create the new machine and clone it!
        vm_clone = vbox.create_machine(settings_file, name, groups, '', 
                                        create_flags)
        progress = vm.clone_to(vm_clone, mode, options)
        show_progress(progress)

        if register:
            vbox.register_machine(vm_clone)

    return vm_clone


def temp_clonevm(machine_or_name_or_id, snapshot_name_or_id=None,
                        daemon=False):
    """Create a linked clone 

    Required:
        machine_or_name_or_id - value can be either IMachine, name, or id
    Options:
        snapshot_name_or_id - value can be either ISnapshot, name, or id 
        daemon - if daemon is True, the cleanup of the cloned machine is now
                 the responsibility of the calling function

    Return a IMachine object for the new cloned vm 
    """
    def atexit_cleanup(vm_clone):
        try:
            removevm(vm_clone)
        except Exception as exc:
            print("Failed to remove %s - %s" % (vm_clone.name, exc))

    if type(machine_or_name_or_id) in [str, unicode]:
        vbox = virtualbox.VirtualBox()
        vm = vbox.find_machine(machine_or_name_or_id)
    else:
        vm = machine_or_name_or_id

    if snapshot_name_or_id is None:
        snapshot_name_or_id = vm.current_snapshot

    vm_clone = clonevm(vm,
                     snapshot_name_or_id=snapshot_name_or_id,
                     basefolder=tempfile.gettempdir())
    if not daemon:
        atexit.register(lambda : atexit_cleanup(vm_clone))
    return vm_clone


@contextlib.contextmanager
def temp_clonevm_context(machine_or_name_or_id, snapshot_name_or_id=None):
    """Load a temp clone in a managed context to ensure it is removed after use

    Required:
        machine_or_name_or_id - value can be either IMachine, name, or id
    Options:
        snapshot_name_or_id - value can be either ISnapshot, name, or id 

    Example:
    > with temp_clonevm_context('test_vm') as vm:
    >    # do stuff with the vm
    >
    > # automatically cleaned up after use... 

    """
    vm = temp_clonevm(machine_or_name_or_id,
                           snapshot_name_or_id=snapshot_name_or_id,
                           daemon=True)
    try:
        yield vm
    finally:
        removevm(vm)


def snapshot_take(machine_or_name_or_id, name, description=''):
    """Take a snapshot of the machine
    
    Required:
        machine_or_name_or_id - value can be either IMachine, name, or id
        name - short name for the snapshot
    Options:
        description - description of the snapshot
    """
    if type(machine_or_name_or_id) in [str, unicode]:
        vbox = virtualbox.VirtualBox()
        vm = vbox.find_machine(machine_or_name_or_id)
    else:
        vm = machine_or_name_or_id

    # take snapshot
    session = virtualbox.Session()
    vm.lock_machine(session, LockType.shared)
    progress = session.console.take_snapshot(snapshot, name, description)
    show_progress(progress)
    session.unlock_machine()
    return vm


def snapshot_restore(machine_or_name_or_id, snapshot_name_or_id=None):
    """Restore to a snapshot
    
    Required:
        machine_or_name_or_id - value can be either IMachine, name, or id
    Options:
        snapshot_name_or_id - value can be either ISnapshot, name, or id 

    return IMachine object    
    """
    if type(machine_or_name_or_id) in [str, unicode]:
        vbox = virtualbox.VirtualBox()
        vm = vbox.find_machine(machine_or_name_or_id)
    else:
        vm = machine_or_name_or_id

    if snapshot_name_or_id is not None:
        snapshot = vm.find_snapshot(snapshot_name_or_id)
    else:
        snapshot = vm.current_snapshot

    # restore snapshot
    session = virtualbox.Session()
    vm.lock_machine(session, LockType.shared)
    progress = session.console.restore_snapshot(snapshot)
    show_progress(progress)
    session.unlock_machine()
    return vm

    
def updatevm(self, machine_or_name_or_id):
    """Update a VM with to the latest [VMNAME].[VERSION] release"""
    pass


CMD_EXE = r"C:\Windows\System32\cmd.exe"
def guest_session(machine_or_name_or_id, username, password, domain='',
                          alive_file=CMD_EXE, timeout_ms=None):
    """Create and yield a guest session object

    Required:
        machine_or_name_or_id - value can be either IMachine, name, or id
        username - a valid username for the guest session to log into to
    Options:
        password - user account password
        domain - domain name of the user account 
        alive_file - if not None the session is not yield until the file can be
                     queried
        timeout_ms - set to None for an infinite wait 

    returns a valid IGuestSession
    """
    if type(machine_or_name_or_id) in [str, unicode]:
        vbox = virtualbox.VirtualBox()
        vm = vbox.find_machine(machine_or_name_or_id)
    else:
        vm = machine_or_name_or_id

    session = virtualbox.Session()
    vm.lock_machine(session, LockType.shared)

    guest_session = session.console.guest.create_session(username, password,
                            domain, 'virtualbox.manage.guest_session_context')

    # Wait until the guest service is alive
    if alive_file is not None:
        while True:
            try:
                guest_session.file_query_info(CMD_EXE)
            except virtualbox.library.VBoxError:
                time.sleep(0.5)
                if timeout_ms is not None:
                    ttl -= 500
                    if ttl < 0:
                        raise 
                continue
            else:
                break
    return guest_session


@contextlib.contextmanager
def guest_session_context(*a, **k):
    # yield our guest session
    gs = guest_session(*a, **k)
    try:
        yield gs
    finally:
        gs.close()
guest_session_context.__doc__ = guest_session.__doc__


def guest_execute(guest_session, cmd, args=[], stdin=[],
        process_create_flags=[ProcessCreateFlag.wait_for_std_err,
                              ProcessCreateFlag.wait_for_std_out,
                              ProcessCreateFlag.hidden,
                              ProcessCreateFlag.ignore_orphaned_processes],
        environment=[], timeout_ms=None):
    """Execute a cmd on the guest
    
    Required:
        guest_session - an connected and established IGuestSession
        cmd - cmd to execute in the guest

    Options:
        args - arguments for the 'cmd'
        stdin - 
        process_create_flags - refer to virtualbox.library.ProcessCreateFlag
        environment - specify the env for the VM 
            ie.
                NAME[=VALUE]           
                NAME[=VALUE] 
                ...
        timeout_ms - limit the guest process' running time.

    For more details refer to virtualbox.library.IGuestSession.process_create 

    return IGuestProcess object
    """
    def read_out(process, process_create_flags, stdout, stderr):
        if ProcessCreateFlag.wait_for_std_err in process_create_flags:
            e = process.read(2, 65000, 0)
            stderr.append(e)
        if ProcessCreateFlag.wait_for_std_out in process_create_flags:
            o = process.read(1, 65000, 0)
            stdout.append(o)

    # set timeout to infinite if None
    if timeout_ms is None:
        timeout_ms = 0  

    # create the new guest process
    process = guest_session.process_create(cmd, args, environment,
                                            process_create_flags, timeout_ms)

    # wait for process session to start
    process.wait_for(int(virtualbox.library.ProcessWaitResult.start), 0)

    # write stdin to the process 
    if stdin:
        index = 0
        while index < len(stdin):
            index += process.write(0, [ProcessInputFlag.none], 
                                    stdin[index:], 0)
        process.write(0, [ProcessInputFlag.end_of_file], 0)

    # read the process output and wait for 
    stdout = []
    stderr = []
    while process.status == virtualbox.library.ProcessStatus.started:
        read_out(process, process_create_flags, stdout, stderr)
        time.sleep(0.2)
    # make sure we have read the remainder of the out
    read_out(process, process_create_flags, stdout, stderr)

    return process, "".join(stdout), "".join(stderr)

