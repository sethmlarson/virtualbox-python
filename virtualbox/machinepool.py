

import virtualbox
from virtualbox import manage
from virtualbox import library


def create_machine_pool(name, machine_or_name_or_id):
    """create a pool of ready to execute liked clones from the Machine"""
    pass


class Pool(object):
    def __init__(self, name):
        self._name = name           
        self._update_pool()

    def _update_pool(self):
        # load configuration for pool
    
    def open(self, block=True):
        """get a Machine resource from the pool"""
        vbox = virtualbox.VirtualBox()
        for vm in vbox.machines:
            if not vm.name.startswtih(self._name):
                continue
            if not '_pool_' in vm.name:
                continue
            # check state, acquire resource
            if vm.machine_state ???
                #

        return Machine(machine, session)

