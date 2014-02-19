:mod:`virtualbox` -- main module
================================

.. module:: virtualbox
    :synopsis: pyvbox
.. moduleauthor:: Michael Dorman <mjdorma+pyvbox@gmail.com>
.. sectionauthor:: Michael Dorman <mjdorma+pyvbox@gmail.com>


This module is the root module for the pyvbox project.  The name 'virtualbox'
has been chosen to enable explicit naming when using this package.  The author
suggests that people new to VirtualBox's extensive COM interface should take
a moment to delve into the API's documentation which will assist in
understanding how VirtualBox's client server module functions.


Code reference
--------------

.. autofunction:: virtualbox.import_vboxapi

.. py:class:: VirtualBox([interface, manager])

    The VirthalBox class is the primary interface used to interact with a
    VirtualBox server.  It wraps the IVirtualBox interface which "represents
    the main interface exposed by the product that provides virtual machine
    management."

    Optionally, this class can be initialised with an already connected COM
    IVirtualBox interface or by passing in a Manager object which implements a
    :py:class:`virtualbox.Manager` get_virthalbox method. 

.. autoclass:: virtualbox.Manager
    :members:
    :special-members:

.. autoclass:: virtualbox.WebServiceManager



