import unittest 
import os
import time
import contextlib

import virtualbox
from virtualbox import library


# Read creds from the file called test_vm.creds
#  USERNAME PASSWORD
if os.path.exists('test_vm.creds'):
    with open('test_vm.creds', 'wb') as f:
        d = f.read()
        username, password = d.split()
else:
    username, password = ['Michael Dorman', 'password']


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

    def atest_power_up_down_via_console(self):
        """power up than down the test_vm via console"""
        vbox = virtualbox.VirtualBox()
        vm = vbox.find_machine('test_vm')
        s = virtualbox.Session()
        vm.lock_machine(s, virtualbox.library.LockType.vm)
        try:
            progress = s.console.power_up()
            progress.wait_for_completion(5000)
            s.console.power_down()
        finally:
            s.unlock_machine()

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
        self.session = virtualbox.Session()
        self.vm = self.vbox.find_machine('test_vm')
        if self.vm.state < virtualbox.library.MachineState.running:
            p = self.vm.launch_vm_process(self.session, "gui", "")
            p.wait_for_completion(5000)
        else:
            self.vm.lock_machine(self.session,
                    virtualbox.library.LockType.shared)

    def tearDown(self):
        self.session.console.power_down()
        while self.vm.state >= virtualbox.library.MachineState.running:
            time.sleep(1)

    @contextlib.contextmanager
    def guest_session(self):
        guest_session = self.session.console.guest.create_session(\
                username, password, '', 'TestGuestSession')
        # Wait until the guest service comes online
        while True:
            try:
                guest_session.file_query_info(CMD_EXE)
            except virtualbox.library.VBoxError:
                time.sleep(0.5)
                continue
            else:
                break
        try:
            yield guest_session
        finally:
            print ("close guest session")
            guest_session.close()


    def test_execute(self):
        """test execute ping localhost"""

        # TODO This technique is unstable
        def execute(guest_session, cmd, args):
            # Now to run a process
            print "Execute %s " % cmd
            process = guest_session.process_create(cmd, args, [],
                    [virtualbox.library.ProcessCreateFlag.wait_for_std_err,
                     virtualbox.library.ProcessCreateFlag.wait_for_std_out],
                    10000)

            # wait until the process has started
            process.wait_for(int(virtualbox.library.ProcessWaitResult.start),
                            5000)

            # NOTE : XP guest svc doesn't support StdOut or StdErr wait flags
            stdout = []
            stderr = []
            # TODO Seems that reading data from stderr sometimes causes a 
            #      VBoxErrorIptrError - which tends to break the guest service
            while process.status == virtualbox.library.ProcessStatus.started:
                #try:
                o = process.read(1, 65000, 1000)
                stdout.append(o)
                e = process.read(2, 65000, 1000)
                stderr.append(e)
                #except virtualbox.library.VBoxErrorIprtError:
                #    pass
                time.sleep(0.2)

            #
            o = process.read(1, 65000, 1000)
            stdout.append(o)
            e = process.read(2, 65000, 1000)
            stderr.append(e)
    
            self.assertEqual(process.status,
                    virtualbox.library.ProcessStatus.terminated_normally)
            
            stdout = "".join(stdout)
            stderr = "".join(stderr)
            return process.exit_code, stdout, stderr

        with self.guest_session() as guest_session:
            _, stdout, _ = execute(guest_session, CMD_EXE, 
                    [r'/C', 'ping', '127.0.0.1'])
            self.assertTrue('Pinging' in stdout)

            # failing...  need to figure out whats going on
            for i in xrange(1000):
                print "Test %s " % (i + 1)
                _, stdout, _ = execute(guest_session, CMD_EXE, 
                        [r'/C', 'netstat', '-nao'])
                print stdout

 

