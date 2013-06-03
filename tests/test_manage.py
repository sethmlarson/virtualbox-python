import unittest 
import os
import time
import threading

import virtualbox
from virtualbox import library
from virtualbox import manage 


# Read creds from the file called test_vm.creds
#  USERNAME PASSWORD
if os.path.exists('test_vm.creds'):
    with open('test_vm.creds', 'wb') as f:
        d = f.read()
        username, password = d.split()
else:
    username, password = ['Michael Dorman', 'password']



CMD_EXE = r"C:\Windows\System32\cmd.exe"
NETSTAT = [r'/C', 'netstat', '-nao']
class TestManage(unittest.TestCase):

    def do_bake_test(self, gs, z=0):
        def test_execute_thread(i, gs):
            _, stdout, _ = manage.guest_execute(gs, CMD_EXE, NETSTAT)
            print "Test %s \n%s" % ((i + 1), stdout)

            _, stdout, _ = manage.guest_execute(gs, CMD_EXE, 
                    [r'/C', 'ping', '127.0.0.1'])
            self.assertTrue('Pinging' in stdout)

        # failing...  need to figure out whats going on
        for i in range(10):
            threads = []
            for x in range(10):
                t = threading.Thread(target=test_execute_thread, 
                                     args=(z*100 + (i * 10) + x, gs))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()


    def test_execute(self):
        """test managed guest execute ping localhost"""
        vm = manage.startvm("test_vm")
        with manage.guest_session_context(vm, username, password) as gs:
            self.do_bake_test(gs)


    def test_forked_vm_execute(self):
        """test forked vm execute"""
        def test_fork_thread(z):
            with manage.temp_clonevm_context("test_vm") as vm:
                manage.startvm(vm)
                with manage.guest_session_context(vm, username, password) as gs:
                    self.do_bake_test(gs, z=z)

        threads = []
        for z in range(10):
            t = threading.Thread(target=test_fork_thread, 
                                 args=(z,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()



