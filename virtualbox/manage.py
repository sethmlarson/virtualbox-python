from __future__ import print_function
import os
import sys
import time
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


