import unittest
import time

import virtualbox


class TestEvents(unittest.TestCase):
    def extra_data_callback(self, event):
        self.called = True
        print(
            "Event key=%s value=%s machineid %s"
            % (event.key, event.value, event.machine_id)
        )

    def test_extra_data_changed(self):
        vbox = virtualbox.VirtualBox()
        vbox.register_on_extra_data_changed(self.extra_data_callback)
        # Cause a change event
        vbox.set_extra_data("test", "data")
        vbox.set_extra_data("test", "dataa")

        time.sleep(1)
        self.assertTrue(self.called)
