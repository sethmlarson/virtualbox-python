"""
Add helper code to the default IGuest class.
"""

import time
import os
import virtualbox
from virtualbox import library


# Define some default params for create session
class IGuest(library.IGuest):
    __doc__ = library.IGuest.__doc__

    def create_session(
        self, user, password, domain="", session_name="pyvbox", timeout_ms=0
    ):
        session = super(IGuest, self).create_session(
            user, password, domain, session_name
        )
        for i in range(50):
            if session.status == library.GuestSessionStatus.started:
                break
            time.sleep(0.1)
        else:
            if len(password) == 0:
                raise SystemError(
                    "GuestSession failed to start. Could be because "
                    "of using an empty password."
                )
            raise SystemError("GuestSession failed to start")
        if timeout_ms != 0:
            # There is probably a better way to to this?
            if "win" in self.os_type_id.lower():
                test_file = "C:\\Windows\\System32\\calc.exe"
            else:
                test_file = "/bin/sh"
            while True:
                try:
                    session.file_exists(test_file)
                except library.VBoxError:
                    time.sleep(0.5)
                    timeout_ms -= 500
                    if timeout_ms <= 0:
                        raise
                    continue
                break
        return session

    create_session.__doc__ = library.IGuest.create_session.__doc__

    # Update guest additions helper
    def update_guest_additions(self, source=None, arguments=None, flags=None):
        if arguments is None:
            arguments = []
        if flags is None:
            flags = [library.AdditionsUpdateFlag.none]
        if source is None:
            manager = virtualbox.Manager()
            source = os.path.join(manager.bin_path, "VBoxGuestAdditions.iso")
        if not os.path.exists(source):
            raise IOError("ISO path '%s' not found" % source)

        return super(IGuest, self).update_guest_additions(source, arguments, flags)

    update_guest_additions.__doc__ = library.IGuest.update_guest_additions.__doc__
