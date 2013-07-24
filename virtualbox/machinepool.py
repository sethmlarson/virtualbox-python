
import virtualbox
from virtualbox import library



class ClonePool(object):
    def __init__(self, root_machine, size=1):
        self._root = root_machine
        self._size = size
        self._clone_name = '%s Pool' % self._root.name
        self._machines = []
        vbox = virtualbox.VirtualBox()
        for vm in vbox.machines:
            if not vm.name.startswith(self._clone_name):
                continue
            self._machines.append(vm)

    @property
    def size(self):
        return self._size

    @settr.size
    def size(self, size):
        self._size = size
        self._adjust_pool()

    @property
    def machines(self):
        return self._machines

    def __len__(self):
        return len(self.machines) 



pool = Pool('cuckoo1', 10)


