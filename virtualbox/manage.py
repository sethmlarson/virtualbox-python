from __future__ import print_function
import os
import shutil
import tempfile
import sys
import contextlib
import atexit

import virtualbox
from virtualbox import library
from virtualbox.library import CloneMode
from virtualbox.library import CloneOptions
from virtualbox.library import CleanupMode 
from virtualbox.library import IMachine

"""
 Provide some convenience functions which pull in some of the beauty of
 vboxmanage.
"""


vbox = virtualbox.VirtualBox()


def show_progress(progress, ofile=sys.stderr):
    """Print the current progress out to file"""
    try:
        while not progress.completed:
            print(progress, file=ofile)
            progress.wait_for_completion(100)
    except KeyboardInterrupt:
        if progress.cancelable:
            progress.cancel()

    print(progress, file=ofile)
    print("Progress state: %s" % progress.result_code, file=ofile)
    if progress.error_info:
        print(progress.error_info.text, file=ofile)


def remove(machine_or_name_or_id, delete=True):
    """Unregister and optionally delete associated config
    Required:
        machine_or_name_or_id - value can be either IMachine, name, or id   
    Options:
        delete - remove all elements of this VM from the system

    Return the (vm, media) 
    """
    # TODO: clean up any open sessions to this vm before 
    if type(machine_or_name_or_id) in [str, unicode]:
        vm = vbox.find_machine(machine_or_name_or_id)
    else:
        vm = machine_or_name_or_id

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


def start(machine_or_name_or_id, session_type='gui', environment=''):
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
        vm = vbox.find_machine(machine_or_name_or_id)
    else:
        vm = machine_or_name_or_id

    session = virtualbox.Session()
    progress = vm.launch_vm_process(session, session_type, environment)
    show_progress(progress)
    sesson.unlock_machine()
    return vm


def clone(machine_or_name_or_id, snapshot_name_or_id=None,
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
        settings_file = vbox.compose_machine_filename(test_name, primary_group,
                                                  create_flags, basefolder)
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


def temp_clone_create(machine_or_name_or_id, snapshot_name_or_id=None,
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
            remove(vm_clone)
        except Exception as exc:
            print("Failed to remove %s - %s" % (vm_clone.name, exc))

    vm_clone = clone(machine_or_name_or_id,
                     snapshot_name_or_id=snapshot_name_or_id,
                     basefolder=tempfile.gettempdir())
    if not daemon:
        atexit.register(lambda : atexit_cleanup(vm_clone))
    return vm_clone


@contextlib.contextmanager
def temp_clone(machine_or_name_or_id, snapshot_name_or_id=None):
    """Load a temp clone in a managed context to ensure it is removed after use

    Required:
        machine_or_name_or_id - value can be either IMachine, name, or id
    Options:
        snapshot_name_or_id - value can be either ISnapshot, name, or id 

    Example:
    > with temp_clone('test_vm') as vm:
    >    # do stuff with the vm
    >
    > # automatically cleaned up after use... 

    """
    vm = temp_clone_create(machine_or_name_or_id,
                           snapshot_name_or_id=snapshot_name_or_id,
                           daemon=True)
    try:
        yield vm
    finally:
        remove(vm)



