
import virtualbox
from virtualbox import library



class Pool(object):
    def __init__(self, root_machine, min_size=1):
        self._root = root_machine
        self._min_size = min_size
        self._clone_name = '%s Pool' % self._root.name
        self._machines = []
        vbox = virtualbox.VirtualBox()
        for vm in vbox.machines:
            if not vm.name.startswtih(self._root.name):
                continue
            if not vm.name.startswith(self._clone_name):
                continue
            self._machines.append(vm)
        self._adjust_pool()

    def _adjust_pool(self):
        for i in range(self.min_size - len(self.machines)):
            self._machines.append(self._root.clone(name=self._clone_name))

    @property
    def min_size(self):
        return self._min_size

    @settr.min_size
    def min_size(self, min_size):
        self._min_size = min_size
        self._adjust_pool()

    @property
    def machines(self):
        return self._machines

    def __len__(self):
        return len(self.machines) 
    
    




