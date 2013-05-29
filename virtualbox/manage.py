from __future__ import print_function
import os
import shutil
import sys

import virtualbox
from virtualbox import library
from virtualbox.library import CloneMode
from virtualbox.library import CloneOptions
from virtualbox.library import CleanupMode 


"""
 Provide some convenience functions which pull in some of the beauty of
 vboxmanage.
"""


vbox = virtualbox.VirtualBox()


def show_progress(progress, file=sys.stderr):
    """Print the current progress out to file"""
    try:
        print(progress, file=file)
        sys.stderr
        while not progress.completed:
            print(progress, file=file)
            progress.wait_for_completion(100)
    except KeyboardInterrupt:
        if progress.cancelable:
            progress.cancel()

    print(progress, file=file)
    print("Progress state: %s" % progress.result_code, file=file)
    if progress.error_info:
        print(progress.error_info.text)


def unregister(machine_name_or_id, delete=True):
    """Unregister and optionally delete associated config
    Required:
        machine_or_name_or_id - value can be either IMachine, name, or id   
    Options:
        delete - remove all elements of this VM from the system

    Return the (vm, media) 
    """
    if machine_or_name_or_id in [str, unicode]:
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


def startvm(machine_name_or_id, session_type='gui', environment=''):
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
    if machine_or_name_or_id in [str, unicode]:
        vm = vbox.find_machine(machine_or_name_or_id)
    else:
        vm = machine_or_name_or_id

    session = virtualbox.Session()
    progress = vm.launch_vm_process(session, session_type, environment)
    show_progress(progress)
    sesson.unlock_machine()
    return vm


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

    Return a IMachine object for the vm 
    """
    if machine_or_name_or_id in [str, unicode]:
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





