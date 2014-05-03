import time
import os

import virtualbox
from virtualbox import library
from virtualbox.library import VirtualSystemDescriptionType as DescType

"""
Add helper code to the default IVirtualSystemDescription class.
"""


class IVirtualSystemDescription(library.IVirtualSystemDescription):
    __doc__ = library.IVirtualSystemDescription.__doc__

    def set_name(self, new_name):
        "Set the name of the appliance (name of machine when imported)."
        types, _, _, vbox_values, extra_config = self.get_description()

        # find offset to Name
        nameoffset = 0
        for nameoffset, t in enumerate(types):
            if t == DescType.name:
                break
        else:
            raise Exception("Failed to find name type")

        enabled = [True] * len(types)
        vbox_values = list(vbox_values)
        extra_config = list(extra_config)
        vbox_values[nameoffset] = new_name
        self.set_final_values(enabled, vbox_values, extra_config)    


