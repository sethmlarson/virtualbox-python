:mod:`virtualbox.library` -- transform of VirtualBox.xidl
=========================================================

.. module:: virtualbox.library
    :synopsis: pyvbox
.. moduleauthor:: Michael Dorman <mjdorma+pyvbox@gmail.com>
.. sectionauthor:: Michael Dorman <mjdorma+pyvbox@gmail.com>

.. :py:mod:: virtualbox.library

The `virtualbox.library` is generated using the VirtualBox project's
VirtualBox.xidl file.  This file contains a complete definition of the
VirtualBox interface.  

pyvbox ships with a builder in it's root folder called build.py.  This builder
is responsible for implementing the code that transforms VirtualBox.xidl into
library.py.

Code reference
--------------

This code reference is the result of using *automodule* to generate
code for the entire *virtualbox.library* module, followed by *autoclass*
to generate doc for the extended classes found in `library_ext`.

:py:mod:`virtualbox.library`
---------------------------

    .. automodule:: virtualbox.library
        :members: 

    .. autoclass:: virtualbox.library.IVirtualBox
        :members: 
        :inherited-members:

    .. autoclass:: virtualbox.library.ISession
        :members: 
        :inherited-members:

    .. autoclass:: virtualbox.library.IKeyboard
        :members: 
        :inherited-members:

    .. autoclass:: virtualbox.library.IGuestSession
        :members: 
        :inherited-members:

    .. autoclass:: virtualbox.library.IGuest
        :members: 
        :inherited-members:

    .. autoclass:: virtualbox.library.IGuestProcess
        :members: 
        :inherited-members:

    .. autoclass:: virtualbox.library.IMachine
        :members: 
        :inherited-members:

    .. autoclass:: virtualbox.library.IProgress
        :members: 
        :inherited-members:

    .. autoclass:: virtualbox.library.IConsole
        :members: 
        :inherited-members:

    .. autoclass:: virtualbox.library.IEventSource
        :members: 
        :inherited-members:

    .. autoclass:: virtualbox.library.IMouse
        :members: 
        :inherited-members:

    .. autoclass:: virtualbox.library.IProcess
        :members: 
        :inherited-members:

    .. autoclass:: virtualbox.library.IConsole
        :members: 
        :inherited-members:

    .. autoclass:: virtualbox.library.IAppliance
        :members: 
        :inherited-members:

    .. autoclass:: virtualbox.library.IVirtualSystemDescription
        :members: 
        :inherited-members:


