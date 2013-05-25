import unittest

import virtualbox



class TestVBox(unittest.TestCase):

    def test_gettr_safearray(self):
        vbox = virtualbox.VirtualBox()
        vbox.machines
        vbox.machine_groups
        vbox.dvd_images
        vbox.floppy_images
        vbox.progress_operations
        vbox.guest_os_types
        vbox.dhcp_servers
        vbox.internal_networks
        vbox.generic_network_drivers

    def test_method_out_safearray(self):
        vbox = virtualbox.VirtualBox()
        vbox.get_extra_data_keys()

    def test_method_in_safearray(self):
        vbox = virtualbox.VirtualBox()
        vbox.get_machine_states(vbox.machines)




