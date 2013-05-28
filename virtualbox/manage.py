import os
import shutil

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

def unregister(vm, delete=True):
    """Unregister and optionally delete associated config"""
    if delete:
        options = CleanupMode.detach_all_return_hard_disk_only
    else:
        options = CleanupMode.detach_all_return_none
    media = vm.unregister(options)
    if delete:
        progress = machine.delete_config(media)
        progress.wait_for_completion(-1)


def startvm(vm, session_type='gui', environment=''):
    """Start a VM

    Return a session to the newly spawned VM
    """
    session = virtualbox.Session()
    progress = vm.launch_vm_process(session, session_type, environment)
    progress.wait_for_completion(-1)
    return session


def clonevm(vm, mode=CloneMode.machine_state, options=[CloneOptions.link],
        name=None, uuid=None, groups=[], basefolder='', register=False):
    """Clone a Machine 
    Args
        vm - machine to be cloned (i.e vm or vm.current_snapshot.machine)
        mode - 
        options - 
        name - 
        uuid -
        groups -
        basefolder - 
        register - 

    Return a clone of vm 
    """
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
    progress.wait_for_completion(100000)

    if register:
        vbox.register_machine(vm_clone)

    return vm_clone





