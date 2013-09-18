import unittest 
import os
import time
import contextlib
import shlex
import os

import funconf

import virtualbox
from virtualbox import library

config = funconf.Config(['tests/test_vm.conf', 'test_vm.conf'])
username = config.machine.username
password = config.machine.password

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

    def test_power_up_down_vm(self):
        """power up than down the test_vm via launch"""
        vbox = virtualbox.VirtualBox()
        vm = vbox.find_machine('test_vm')
        s = virtualbox.Session()
        p = vm.launch_vm_process(s, "headless", "")
        p.wait_for_completion(5000)
        s.console.power_down()
        s.unlock_machine()


CMD_EXE = r"C:\Windows\System32\cmd.exe"
class TestGuestSession(unittest.TestCase):
    def setUp(self):
        self.vbox = virtualbox.VirtualBox()
        self.vm = self.vbox.find_machine('test_vm')
        self._powered_up = False
        if self.vm.state < virtualbox.library.MachineState.running:
            self._powered_up = True
            p = self.vm.launch_vm_process()
            p.wait_for_completion()
        self.session = self.vm.create_session()

    def tearDown(self):
        if self._powered_up:
            self.session.console.power_down()
            while self.vm.state >= virtualbox.library.MachineState.running:
                time.sleep(1)

    def test_execute(self):
        guest = self.session.console.guest.create_session(username, password,
                                timeout_ms=60*2000)
        p, o, e = guest.execute(CMD_EXE, [r'/C', 'ping', '127.0.0.1'])
        self.assertTrue('Pinging' in o)
        
        p, o, e = guest.execute(CMD_EXE, [r'/C', 'netstat', '-nao'])
        self.assertTrue('Active Connections' in o)

 

