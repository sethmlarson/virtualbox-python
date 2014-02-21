from virtualbox import library

"""
Add helper code to the default IProcess class.
"""

class IProcess(library.IProcess):
    __doc__ = library.IProcess.__doc__
    
    def wait_for(self, wait_for, timeout_ms=0):
        return super(IProcess, self).wait_for(int(wait_for), timeout_ms)
    wait_for.__doc__ = library.IProcess.__doc__
