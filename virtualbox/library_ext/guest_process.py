from virtualbox import library

"""
Add helper code to the default IProcess class.
"""
from virtualbox.library_ext import process

# Because there is a bug in IProcess, which is the super class of 
# IGuestProcess, we'll inherit from our fixed IProcess to ensure
# that IGuestPRocess behaves correctly.
class IGuestProcess(process.IProcess):
    __doc__ = library.IGuestProcess.__doc__

    

