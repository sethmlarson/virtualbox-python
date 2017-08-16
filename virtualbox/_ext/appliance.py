"""
Add helper code to the default Appliance class.
"""

from .._library import Appliance as _Appliance
from .._library import (VirtualSystemDescriptionType,
                        VirtualSystemDescriptionValueType)


# Define some default params for create session
class Appliance(_Appliance):
    __doc__ = _Appliance.__doc__

    # Extend read to wait and interpret the values into Description
    # objects.
    def read(self, ova_path):
        "Read and interpret ova file into this Appliance object."
        p = super(IAppliance, self).read(ova_path)
        p.wait_for_completion()
        self.interpret()
        warnings = self.get_warnings()
        if warnings:
            warning = Warning("\n".join(warnings))
            warning.warnings = warnings
            raise warning
    read.__doc__ = _Appliance.read.__doc__

    def find_description(self, name):
        "Find a description for the given appliance name."
        for desc in self.virtual_system_descriptions:
            values = desc.get_values_by_type(VirtualSystemDescriptionType.name,
                                             VirtualSystemDescriptionValueType.original)
            if name in values:
                break
        else:
            raise Exception("Failed to find description for %s" % name)
        return desc

    # Simply this call by setting options to default []
    def import_machines(self, options=None):
        if options is None:
            options = []
        return super(IAppliance, self).import_machines(options)
    import_machines.__doc__ = _Appliance.import_machines.__doc__
