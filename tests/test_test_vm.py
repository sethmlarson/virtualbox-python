import unittest 

import virtualbox
from virtualbox import library


class TestTestVM(unittest.TestCase):
    
    def test_lock_vm(self):
        """create a locked session for the test_vm machine"""
        vbox = virtualbox.VirtualBox()
        
        # Assert that we can create a lock over a machine 
        vm = vbox.find_machine('test_vm')
        s = virtualbox.Session()
        vm.lock_machine(s, virtualbox.library.LockType.shared)
        self.assertTrue(s.state == virtualbox.library.SessionState.locked)

        # Assert we can only lock a session object once 
        self.assertRaises(library.VBoxErrorInvalidObjectState,
                        vm.lock_machine,
                        s, 
                        virtualbox.library.LockType.shared)

        # Assert we can open a second session and can now apply a write lock
        # to the resource machine as it already has a shared lock acquired
        s2 = virtualbox.Session()
        self.assertRaises(library.VBoxErrorInvalidObjectState,
                        vm.lock_machine,
                        s2, 
                        virtualbox.library.LockType.write)

        # Assert that we can open a shared lock to the vm which already has
        # a session with a shared lock over it
        vm.lock_machine(s2, virtualbox.library.LockType.shared)
        self.assertTrue(s2.state == virtualbox.library.SessionState.locked)

        # Assert that unlocking the machine through s or s2 will change
        # the lock state of s2 back to unlocked
        s.unlock_machine()
        self.assertTrue(s.state == virtualbox.library.SessionState.unlocked)
        self.assertTrue(s2.state == virtualbox.library.SessionState.unlocked)

        # Finally, build a write lock and assert we can not open a shared lock
        vm.lock_machine(s, virtualbox.library.LockType.write)
        self.assertRaises(library.VBoxErrorInvalidObjectState,
                        vm.lock_machine,
                        s2, 
                        virtualbox.library.LockType.write)
        s.unlock_machine()
        self.assertRaises(library.VBoxError, s.unlock_machine)

    def test_power_up_down_via_console(self):
        """power up than down the test_vm via console"""
        vbox = virtualbox.VirtualBox()
        vm = vbox.find_machine('test_vm')
        s = virtualbox.Session()
        vm.lock_machine(s, virtualbox.library.LockType.write)
        try:
            #progress = s.console.power_up()
            pass

        finally:
            s.unlock_machine()

    def test_power_up_down_vm(self):
        """power up than down the test_vm via launch"""
        #vm.launch_vm_process
        vbox = virtualbox.VirtualBox()
        vm = vbox.find_machine('test_vm')
        s = virtualbox.Session()
        p = vm.launch_vm_process(s, "headless", "")
        p.wait_for_completion(5000)
        s.console.power_down()
        s.unlock_machine()
        

#s.console.guest.create_session('mick', 'XXXXXX', 'workgroup', '',)
#iguest.process_create('notepad.exe', '', '', [virtualbox.library.ProcessCreateFlag.wait_for_process_start_only], 1000)

