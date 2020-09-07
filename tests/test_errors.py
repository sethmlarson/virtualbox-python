import unittest

import virtualbox
from virtualbox.library import VBoxError


class TestErrors(unittest.TestCase):
    def test_raises(self):
        vbox = virtualbox.VirtualBox()
        try:
            vbox.find_machine("blah blah X")
        except VBoxError as exc:
            pass
        else:
            self.fail("VBoxError not raised")
