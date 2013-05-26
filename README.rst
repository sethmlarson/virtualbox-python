Introduction to pyvbox 
**********************

What's in pyvbox:

* A complete implementation of the VirtualBox Main API
* Create a VirtualBox instance and seamlessly explorer the potential of
  VirtualBox's amazing Main API 
* Pythonic functions and names.
* Introspection, documentation strings, getters and setters...


Project hosting provided by `github.com`_.

Install and run
===============

Simply run the following::

    > python setup.py install
    > python setup.py test

Start stop example::

    > ipython
    In [1]: import virtualbox

    In [2]: vbox = virtualbox.VirtualBox()

    In [3]: session = virtualbox.Session()

    In [4]: vm = vbox.find_machine('test_vm')

    In [5]: progress = vm.launch_vm_process(session, 'headless', '')

    In [6]: h, w, d = session.console.display.get_screen_resolution(0)

    In [7]: png = session.console.display.take_screen_shot_png_to_array(0, h, w)

    In [8]: with open('screenshot.png', 'wb') as f:
      ....:     f.write(png)

    In [9]: print(session.state)
    Locked

    In [10]: session.state
    Out[10]: SessionState(2)

    In [11]: session.state >= 2
    Out[11]: True
    
    In [12]: session.console.power_down()

Exploring the interface example::
    
    >ipython
    In [1]: virtualbox?

    In [2]: virtualbox.VirtualBox?

    In [3]: virtualbox.library.IMachine?

    In [4]: virtualbox.library.MachineState?

    In [5]: virtualbox.library.MachineState.teleported?


Issues
======

Source code for *pyvbox* is hosted on `GitHub
<https://github.com/mjdorma/pyvbox>`_. 
Please file `bug reports <https://github.com/mjdorma/pyvbox/issues>`_
with GitHub's issues system.


Compatibility
=============

*pyvbox* utilises the VirtualBox project's vboxapi to gain access to the
underlying COM API primitives.  Therefore, pyvbox is compatible on systems
which have a running vboxapi.

Change log
==========

version 0.0.0 (10/05/2013)

* builder 
* library primitives 






.. _github.com: https://github.com/provoke-vagueness/restq

