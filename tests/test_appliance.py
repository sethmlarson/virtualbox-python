import os
import unittest

import virtualbox
"""
ATENTION: This test case interacts with the local VirtualBox and
          may harm your setup.
"""
FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')
APPLIANCE_FILE = 'appliance_test_1.ova'
MACHINE_NAME = 'appliance_test_1'
MACHINE_NEW_NAME = 'appliance_test_1_RENAMED'

def is_dangerous():
    vbox = virtualbox.VirtualBox()
    current_machines = [m.name for m in vbox.machines]
    test_names = (MACHINE_NAME, MACHINE_NEW_NAME)
    return any(name in current_machines for name in test_names)

@unittest.skipIf(is_dangerous(),
                 "Please delete boxes: {} manually.".format(
                     (', '.join((MACHINE_NAME, MACHINE_NEW_NAME)))))
class TestAppliance(unittest.TestCase):
    def setUp(self):
        self.vbox = virtualbox.VirtualBox()
        self.appliance = self.vbox.create_appliance()
        self.appliance.read(os.path.join(FIXTURES, APPLIANCE_FILE))
        self.desc = self.appliance.find_description(MACHINE_NAME)

    def delete_machine(self, name):
        "Delete this machine if exists."
        try:
            machine = self.vbox.find_machine(name)
        except:
            pass
        else:
            try:
                machine.remove(delete=True)
            except:
                pass

    def do_import(self):
        p = self.appliance.import_machines()
        p.wait_for_completion()

    def tearDown(self):
        self.delete_machine(MACHINE_NAME)
        self.delete_machine(MACHINE_NEW_NAME)

    def test_change_name(self):
        self.desc.set_name(MACHINE_NEW_NAME)
        self.do_import()
        self.assertTrue(self.vbox.find_machine(MACHINE_NEW_NAME))

    def test_change_cpu(self):
        self.desc.set_cpu(MACHINE_NEW_NAME)
        self.do_import()
        self.imported_machine = self.vbox.find_machine(MACHINE_NEW_NAME)
