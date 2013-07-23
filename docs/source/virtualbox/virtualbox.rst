:mod:`virtualbox` -- pyvbox package module
==========================================

.. module:: virtualbox
    :synopsis: pyvbox
.. moduleauthor:: Michael Dorman <mjdorma+pyvbox@gmail.com>
.. sectionauthor:: Michael Dorman <mjdorma+pyvbox@gmail.com>



:py:class:`VirtualBox`
----------------------

.. py:class:: VirtualBox([interface, manager])

The VirthalBox class is the primary interface used to interact with a
VirtualBox server.  It wraps the IVirtualBox interface which "represents the
main interface exposed by the product that provides virtual machine management."

Optionally, this class can be initialised with an already connected COM
IVirtualBox interface or by passing in a Manager object which implements a
py:class:`Manager`.get_virthalbox method. 


:py:class:`Manager`
-------------------

.. py:class:: Manager()

This class is responsible for the construction of the ISession object and IVirtualBox object.


:py:class:`Session`
-------------------

.. py:class:: Session()

The Session class is a container for the ISession interface which "represents a
client process and allows for locking virtual machines".


