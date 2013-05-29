import unittest

from virtualbox import library

class TestEnumeration(unittest.TestCase):

    def test_machine_state_paused(self):
        self.assertEqual(int(library.MachineState.paused), 6)
        self.assertEqual(str(library.MachineState.paused), "Paused")
        self.assertEqual(repr(library.MachineState.paused), 
                            "MachineState(6)")



