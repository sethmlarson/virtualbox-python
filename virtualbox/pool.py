"""Virtual Machine pool
=======================

The :py:class:`MachinePool` manages a pool of linked clones against a defined
"root machine".  This module works with multiple processes running on the
host machine at a time.  It manages a resource lock over the root virtual
machine to ensure consistency.

In this example the machine *win7* has a current version of guest editions
installed and is in a powered off state.


Create multiple clones::

    pool = MachinePool('win7')
    sessions = []
    for i in range(3):
        sessions.append(pool.acquire("Mick", "password"))

    # You now have three running machines.
    for session in sessions:
        with session.guest.create_session("Mick", "password") as gs:
            _, out, _ = gs.execute("ipconfig")
            print(out)

    for session in sessions:
        pool.release(session)


A reliable version of the above code would look like this::

    pool = MachinePool('win7')
    sessions = []
    try:
        for i in range(3):
            sessions.append(pool.acquire("Mick", "password"))

        # You now have three running machines.
        for session in sessions:
            with session.guest.create_session("Mick", "password") as gs:
                _, out, _ = gs.execute("ipconfig")
                print(out)

    finally:
        for session in sessions:
            try:
                pool.release(session)
            except Exception as err:
                print("Error raised on release: %s" % err)

"""

from __future__ import absolute_import
from contextlib import contextmanager
import time

from virtualbox import VirtualBox
from virtualbox import Session
from virtualbox.library import LockType
from virtualbox.library import SessionState
from virtualbox.library import DeviceType
from virtualbox.library import DeviceActivity
from virtualbox.library import OleErrorUnexpected


class MachinePool(object):
    """MachinePool manages a pool of resources and enable cross process
    coordination of a linked machine clone."""

    def __init__(self, machine_name):
        """Create a MachinePool instance.

        :param machine_name: Name of the root virtual machine.
        :type machine_name: str
        """
        self.machine_name = machine_name
        with self._lock() as session:
            machine = session.machine
            if not machine.current_snapshot:
                p, id_p = machine.take_snapshot("initialised", "root machine", False)
                p.wait_for_completion(60 * 1000)

    @contextmanager
    def _lock(self, timeout_ms=-1):
        """Exclusive lock over root machine"""
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
        """Yield all machines under this pool"""
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
            p.wait_for_completion(60 * 1000)
            try:
                session.unlock_machine()
            except OleErrorUnexpected:
                # session seems to become unlocked automatically after
                # wait_for_completion is called after the power_down?
                pass
            session = clone.create_session()
            p = session.machine.restore_snapshot()
            p.wait_for_completion(60 * 1000)
            return clone
        finally:
            if session.state == SessionState.locked:
                session.unlock_machine()

    def acquire(self, username, password, frontend="headless"):
        """Acquire a Machine resource."""
        with self._lock() as root_session:
            for clone in self._clones:
                # Search for a free clone
                session = Session()
                try:
                    clone.lock_machine(session, LockType.write)
                except Exception:
                    continue
                else:
                    try:
                        p = session.machine.restore_snapshot()
                        p.wait_for_completion(60 * 1000)
                    except Exception:
                        pass
                    session.unlock_machine()
                    break
            else:
                # Build a new clone
                machine = root_session.machine
                clone = machine.clone(name="%s Pool" % self.machine_name)
                p = clone.launch_vm_process(type_p=frontend)
                p.wait_for_completion(60 * 1000)
                session = clone.create_session()
                console = session.console
                guest = console.guest
                try:
                    guest_session = guest.create_session(
                        username, password, timeout_ms=300 * 1000
                    )
                    idle_count = 0
                    timeout = 60
                    while idle_count < 5 and timeout > 0:
                        act = console.get_device_activity([DeviceType.hard_disk])
                        if act[0] == DeviceActivity.idle:
                            idle_count += 1
                        time.sleep(0.5)
                        timeout -= 0.5
                    guest_session.close()
                    console.pause()
                    p, id_p = console.machine.take_snapshot(
                        "initialised", "machine pool", True
                    )
                    p.wait_for_completion(60 * 1000)
                    self._power_down(session)
                finally:
                    if session.state == SessionState.locked:
                        session.unlock_machine()

            # Launch our clone
            p = clone.launch_vm_process(type_p=frontend)
            p.wait_for_completion(60 * 1000)
            session = clone.create_session()
            return session

    def release(self, session):
        """Release a machine session resource."""
        if session.state != SessionState.locked:
            return
        with self._lock():
            return self._power_down(session)
