from virtualbox import library

"""
Add helper code to the default IProgress class.
"""


# Helper function for IProgress to print out a current progress state
# in __str__ 
_progress_template = """\
(%(o)s/%(oc)s) %(od)s %(p)-3s%% (%(tr)s s remaining)"""
class IProgress(library.IProgress):
    __doc__ = library.IProgress.__doc__

    def __str__(self):
       return _progress_template % dict(o=self.operation, p=self.percent,
               oc=self.operation_count, od=self.operation_description, 
               tr=self.time_remaining)

    def wait_for_completion(self, timeout=-1):
        super(IProgress, self).wait_for_completion(timeout)
    wait_for_completion.__doc__ = library.IProgress.wait_for_completion.__doc__
