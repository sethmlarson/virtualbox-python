"""

"""
from contextlib import contextmanager
import time

from virtualbox import VirtualBox
from virtualbox import Session 
from virtualbox.library import LockType
from virtualbox.library import SessionState 
from virtualbox.library import MachineState 
from virtualbox.library import DeviceType 
from virtualbox.library import DeviceActivity 

class MachinePool(object):
    """
    """
    def __init__(self, machine_name):
        self.machine_name = machine_name
        with self._lock() as session:
            if not session.machine.current_snapshot:
                console = session.console
                p = console.take_snapshot('initialised', 'root machine')
                p.wait_for_completion(60*1000)

    @contextmanager
    def _lock(self, timeout_ms=-1):
        "Exclusive lock over root machine"
        vbox = VirtualBox()
        machine = vbox.find_machine(self.machine_name)
        wait_time = 0
        while True:
            session = Session()
            try:
                machine.lock_machine(session, LockType.write)
            except Exception as exc:
                if timeout_ms != -1 and wait_time > timeout_ms:
                    raise ValueError("Failed to acquire lock - %s" % exc)
                time.sleep(1)
                wait_time += 1000
            else:
                try:
                    yield session
                finally: 
                    session.unlock_machine()
                break

    @property
    def _clones(self):
        "Yield all machines under this pool"
        vbox = VirtualBox()
        machines = []
        for machine in vbox.machines:
            if machine.name == self.machine_name:
                continue
            if machine.name.startswith(self.machine_name):
                machines.append(machine)
        return machines

    def _power_down(self, session):
        vbox = VirtualBox()
        clone = vbox.find_machine(session.machine.name)
        try:
            p = session.console.power_down()
            p.wait_for_completion(60*1000)
            session.unlock_machine()
            session = clone.create_session()
            console = session.console
            p = console.restore_snapshot()
            p.wait_for_completion(60*1000)
            return clone
        finally:
            if session.state == SessionState.locked:
                session.unlock_machine()

    def acquire(self, username, password):
        "Acquire a Machine resource"
        with self._lock() as root_session:
            for clone in self._clones:
                # Search for a free clone 
                session = Session()
                try:
                    clone.lock_machine(session, LockType.write)
                except:
                    continue
                else:
                    session.unlock_machine()
                    break
            else:
                # Build a new clone
                machine = root_session.machine
                clone = machine.clone(name="%s Pool" % self.machine_name)
                p = clone.launch_vm_process(type_p='headless')
                p.wait_for_completion(60*1000)
                session = clone.create_session()
                console = session.console
                guest = console.guest
                try:
                    guest_session = guest.create_session(username, password,
                                                         timeout_ms=5*60*1000)
                    idle_count = 0
                    timeout = 60
                    while idle_count < 5 and timeout > 0:
                        act = console.get_device_activity(DeviceType.hard_disk)
                        if act == DeviceActivity.idle:
                            idle_count += 1
                        time.sleep(0.5)
                        timeout -= 0.5
                    guest_session.close()
                    console.pause()
                    p = console.take_snapshot('initialised', 'machine pool')
                    p.wait_for_completion(60*1000)
                    self._power_down(session)
                finally:
                    if session.state == SessionState.locked:
                        session.unlock_machine()

            # Launch our clone
            p = clone.launch_vm_process(type_p='headless')
            p.wait_for_completion(60*1000)
            session = clone.create_session()
            return session
    
    def release(self, session):
        "Release a machine session resource"
        if session.state != SessionState.locked:
            return 
        with self._lock():
            return self._power_down(session)



