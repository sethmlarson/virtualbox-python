"""
"""

from multiprocessing import Process
from threading import Thread
import time

import begin
import funconf
from virtualbox import pool

config = funconf.Config('tests/test_vm.conf', 'test_vm.conf')

@begin.subcommand
@config
def seed(machine_name, machine_username, machine_password, seed_count):
    "Test seeding vms"
    mp = pool.MachinePool(machine_name)
    sessions = []
    for i in range(seed_count):
        s = mp.acquire(machine_username, machine_password)
        print("Acquired %s" % s.machine.name)
        sessions.append(s)
    time.sleep(4)
    for s in sessions:
        s.unlock_machine()
        print("Released %s" % s.machine.name)

@begin.subcommand
@config
def seed_multiproc(machine_name, 
                   machine_username, 
                   machine_password, 
                   seed_count):
    "Test seeding vms from multiple processes"
    procs = []
    args=(machine_name, machine_username, machine_password, seed_count)
    for i in range(int(count)):
        p = Process(target=seed, args=args)
        p.start()
        procs.append(p)
    for p in procs:
        p.join()

@begin.subcommand
@config
def seed_multithread(machine, count, username, password):
    "Test seeding vms from multiple threads"
    threads = []
    args=(machine_name, machine_username, machine_password, seed_count)
    for i in range(int(count)):
        t = Process(target=seed, args=args)
        t.start()
        threads.append(t)
    for t in procs:
        t.join()

@begin.start
def main():
    pass


