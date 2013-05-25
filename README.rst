Introduction to pyvbox 
**********************

What is pyvbox:

* A complete implementation of the VirtualBox Main API
* Create a VirtualBox instance and explorer the potential of VirtualBox's
  amazing COM API 

Project hosting provided by `github.com`_.


Install and run
===============

Simply run the following::

    > python setup.py install
    > python setup.py test
    > python -m restq -h


Example::

    > ipython
    import virtualbox
    vbox = virtualbox.VirtualBox()
    session = virtualbox.Session()
    vm = vbox.find_machine('test_vm')
    progress = vm.launch_vm_process(session, 'headless', '')
    session.console ...
    #WIN WIN

Issues
======

Source code for *pyvbox* is hosted on `GitHub
<https://github.com/mjdorma/pyvbox>`_. 
Please file `bug reports <https://github.com/mjdorma/pyvbox/issues>`_
with GitHub's issues system.


Compatibility
=============

*pyvbox* utilises the VirtualBox project's vboxapi to gain access to the
underlying COM API primitives, which makes pyvbox compatible on systems where
vboxapi is installed and functioning.  


Change log
==========

version 0.0.0 (10/05/2013)

* builder 
* library primitives 






.. _github.com: https://github.com/provoke-vagueness/restq

