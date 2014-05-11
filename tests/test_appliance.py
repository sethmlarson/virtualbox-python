import os
import unittest

import virtualbox
"""
ATENTION: This test case interacts with the local VirtualBox and
          may harm your setup.
"""
FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')

APPLIANCE_FILE = 'appliance_test_1.ova'

APPLIANCE_NAME = 'appliance_test_1'
APPLIANCE_CPU = 1
APPLIANCE_MEM = 5
APPLIANCE_AUDIO = virtualbox.library.AudioControllerType(0)  # AC97

MACHINE_NEW_NAME = 'appliance_test_1_RENAMED'
MACHINE_CPU = 2
MACHINE_MEM = 64
MACHINE_AUDIO = virtualbox.library.AudioControllerType(1)  # SB16


def is_dangerous():
    vbox = virtualbox.VirtualBox()
    current_machines = [m.name for m in vbox.machines]
    test_names = (APPLIANCE_NAME, MACHINE_NEW_NAME)
    return any(name in current_machines for name in test_names)


@unittest.skipIf(is_dangerous(),
                 "Please delete boxes: {} manually.".format(
                     (', '.join((APPLIANCE_NAME, MACHINE_NEW_NAME)))))
class TestAppliance(unittest.TestCase):
    def setUp(self):
        self.vbox = virtualbox.VirtualBox()
        self.appliance = self.vbox.create_appliance()
        self.appliance.read(os.path.join(FIXTURES, APPLIANCE_FILE))
        self.desc = self.appliance.find_description(APPLIANCE_NAME)

    def delete_machine(self, name):
        """Delete this machine if exists."""
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
        """Import the current appliance."""
        p = self.appliance.import_machines()
        p.wait_for_completion()
        self.assertTrue(self.appliance.machines)

    def tearDown(self):
        self.delete_machine(APPLIANCE_NAME)
        self.delete_machine(MACHINE_NEW_NAME)

    def test_import_unchanged(self):
        self.do_import()
        i_machine = self.vbox.find_machine(APPLIANCE_NAME)

        self.assertTrue(i_machine.cpu_count == APPLIANCE_CPU)
        self.assertTrue(i_machine.memory_size == APPLIANCE_MEM)
        self.assertTrue(i_machine.audio_adapter.audio_controller == APPLIANCE_AUDIO)

    def test_change_name(self):
        self.desc.set_name(MACHINE_NEW_NAME)

        self.do_import()

        self.assertTrue(self.vbox.find_machine(MACHINE_NEW_NAME))

    def test_change_cpu(self):
        self.desc.set_cpu(MACHINE_CPU)

        self.do_import()

        i_machine = self.vbox.find_machine(APPLIANCE_NAME)
        self.assertTrue(i_machine.cpu_count == MACHINE_CPU)

    def test_change_memory(self):
        self.desc.set_memory(MACHINE_MEM)

        self.do_import()

        i_machine = self.vbox.find_machine(APPLIANCE_NAME)
        self.assertTrue(i_machine.memory_size == MACHINE_MEM)

    def test_change_soundcard(self):
        self.desc.set_soundcard(MACHINE_AUDIO)

        self.do_import()

        i_machine = self.vbox.find_machine(APPLIANCE_NAME)
        self.assertTrue(i_machine.audio_adapter.audio_controller == MACHINE_AUDIO)

    @unittest.skip("Discover the correct value to set in the appliance.")
    def test_change_usb_controller(self):
        pass

    @unittest.skip("Discover the correct value to set in the appliance.")
    def test_change_network_adapter(self):
        pass

    @unittest.skip("Discover the correct value to set in the appliance.")
    def test_change_cdrom(self):
        pass

    @unittest.skip("Discover the correct value to set in the appliance.")
    def test_change_hard_disk_controller_ide(self):
        pass

    @unittest.skip("Discover the correct value to set in the appliance.")
    def test_change_hard_disk_controller_sas(self):
        pass

    @unittest.skip("Discover the correct value to set in the appliance.")
    def test_change_hard_disk_controller_sata(self):
        pass

    @unittest.skip("Discover the correct value to set in the appliance.")
    def test_change_hard_disk_controller_scsi(self):
        pass

    @unittest.skip("Discover the correct value to set in the appliance.")
    def test_change_hard_disk_image(self):
        pass

    def test_change_multiple_values(self):
        """
        Change multiple values and test if they are not overridden by
        the defaults.

        """
        self.desc.set_name(MACHINE_NEW_NAME)
        self.desc.set_cpu(MACHINE_CPU)
        self.desc.set_memory(MACHINE_MEM)

        self.do_import()
        i_machine = self.vbox.find_machine(MACHINE_NEW_NAME)

        self.assertTrue(i_machine.cpu_count == MACHINE_CPU)
        self.assertTrue(i_machine.memory_size == MACHINE_MEM)
