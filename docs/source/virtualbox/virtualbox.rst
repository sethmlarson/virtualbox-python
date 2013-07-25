:mod:`virtualbox` -- pyvbox package
===================================

.. module:: virtualbox
    :synopsis: pyvbox
.. moduleauthor:: Michael Dorman <mjdorma+pyvbox@gmail.com>
.. sectionauthor:: Michael Dorman <mjdorma+pyvbox@gmail.com>


This module is the root module for the pyvbox project.  The name has been chosen
to enable explicit naming when using this package.  The author suggests that
people new to VirtualBox's extensive COM interface should take some time to
delve into the API's documentation to understand how this package can be used
and how it will help you to win at controlling VirtualBox.  


.. py:class:: VirtualBox([interface, manager])

    The VirthalBox class is the primary interface used to interact with a
    VirtualBox server.  It wraps the IVirtualBox interface which "represents
    the main interface exposed by the product that provides virtual machine
    management."

    Optionally, this class can be initialised with an already connected COM
    IVirtualBox interface or by passing in a Manager object which implements a
    :py:class:`virtualbox.Manager` get_virthalbox method. 


.. py:class:: Manager()

    This class is responsible for the construction of
    :py:class:`virtualbox.library_ext.ISession` and
    :py:class:`virtualbox.library_ext.IVirtualBox`. 

    .. attribute:: manager

        *manager* is the singleton which is the result of a call to
        vboxapi.VirtualBoxManager(None, None). 

    .. attribute:: bin_path

        The path to the virtualbox install directory.

    .. method:: get_virtualbox()
        
        Returns a :py:class:`virtualbox.library.IVirtualBox` object constructed
        through the vboxapi's getVirtualBox() function. 
    
    .. method:: get_session()

        Returns a :py:class:`virtualbox.library.ISession` object constructed
        through the vboxapi's getSessionObject() function.

    .. method:: cast_object(interface_object, interface_class)
        
        Casts the :py:class:`virtualbox.library.Interface` *interface_object*
        into the *interface_class* type by calling the vboxapi's manager
        queryInterface function.  


.. py:class:: Session()

    The Session class simply references :py:class:`virtualbox.library.ISession`
    which "represents a client process and allows for locking virtual machines".


