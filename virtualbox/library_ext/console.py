from __future__ import print_function

import virtualbox
from virtualbox import library

"""
Add helper code to the default IConsole class.
"""

class IConsole(library.IConsole):
    __doc__ = library.IConsole.__doc__

    def restore_snapshot(self, snapshot=None):
        if snapshot is None:
            if self.machine.current_snapshot:
                snapshot = self.machine.current_snapshot
            else:
                raise Exception("Machine has no snapshots")
        return super(IConsole, self).restore_snapshot(snapshot)
    restore_snapshot.__doc__ = library.IConsole.restore_snapshot.__doc__


