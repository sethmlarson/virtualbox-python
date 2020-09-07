"""
"""

from multiprocessing import Process
from threading import Thread
import time

import begin
import funconf
from virtualbox import pool


config = funconf.Config(["tests/test_vm.conf", "test_vm.conf"])


def on_machine_state_changed(event):
    vbox = pool.VirtualBox()
    machine = vbox.find_machine(event.machine_id)
    print("Machine '%s' state has changed to %s" % (machine.name, event.state))


# TODO :  BUG found in vboxapi ...
#         If a call to vboxapi.VirtualBoxManager is made in the main process
#         followed by another call in a forked multiprocess Process, the call
#         in the subprocess freezes and will not return...  Bug in one of the
#         lower level APIs
# if __name__ == '__main__':
#    vbox = pool.VirtualBox()
#    vbox.register_on_machine_state_changed(on_machine_state_changed)

# Note: python3.x this maybe solved using set_start_method


@begin.subcommand
@config
def seed(machine_name, machine_username, machine_password, seed_count):
    "Test seeding vms"
    # register here - can't do it in scope of module due to bug in
    # low level API.
    vbox = pool.VirtualBox()
    vbox.register_on_machine_state_changed(on_machine_state_changed)

    mp = pool.MachinePool(machine_name)
    sessions = []
    for i in range(seed_count):
        s = mp.acquire(machine_username, machine_password)
        sessions.append(s)
    time.sleep(4)
    for s in sessions:
        machine = mp.release(s)


@begin.subcommand
@config
def seed_multiproc(machine_name, machine_username, machine_password, seed_count):
    "Test seeding vms from multiple processes"
    procs = []
    args = (machine_name, machine_username, machine_password, 1)
    for i in range(seed_count):
        p = Process(target=seed, args=args)
        p.start()
        procs.append(p)
    for p in procs:
        p.join()


@begin.subcommand
@config
def seed_multithread(machine_name, machine_username, machine_password, seed_count):
    "Test seeding vms from multiple threads"
    threads = []
    args = (machine_name, machine_username, machine_password, 1)
    for i in range(seed_count):
        t = Thread(target=seed, args=args)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


@begin.start
def main():
    pass
