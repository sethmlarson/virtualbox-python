Introduction to pyvbox 
**********************

What's in pyvbox:

* A complete implementation of the VirtualBox Main API
* Create a VirtualBox instance and seamlessly explore the potential of
  VirtualBox's amazing Main API 
* Pythonic functions and names.
* Introspection, documentation strings, getters and setters, and more...

Project documentation at `readthedocs.org`_.

Project hosting provided by `github.com`_.


[mjdorma+pyvbox@gmail.com]


Install 
=======

Simply run the following::

    > python setup.py install
    
or `PyPi`_:: 

    > pip install pyvbox
    

Getting started 
===============

Exploring the library::
    
    > ipython
    In [1]: import virtualbox

    In [2]: virtualbox?

    In [3]: virtualbox.VirtualBox?

    In [4]: virtualbox.library.IMachine?

    In [5]: virtualbox.library.MachineState?

    In [6]: virtualbox.library.MachineState.teleported?


Listing machines::

    > ipython
    In [1]: import virtualbox

    In [2]: vbox = virtualbox.VirtualBox()

    In [3]: print("VM(s):\n + %s" % "\n + ".join([vm.name for vm in vbox.machines]))
    VM(s):
     + filestore
     + xpsp3
     + win7
     + win8
     + test_vm


Launch machine, take a screen shot, stop machine::

    > ipython
    In [1]: import virtualbox

    In [2]: vbox = virtualbox.VirtualBox()

    In [3]: session = virtualbox.Session()

    In [4]: vm = vbox.find_machine('test_vm')

    In [5]: progress = vm.launch_vm_process(session, 'gui', '')

    In [6]: h, w, _, _, _ = session.console.display.get_screen_resolution(0)

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


Write text into a window on a running machine::

    > ipython
    In [1]: import virtualbox

    In [2]: vbox = virtualbox.VirtualBox()

    In [3]: vm = vbox.find_machine('test_vm')

    In [4]: session = vm.create_session() 

    In [5]: session.console.keyboard.put_keys("Q: 'You want control?'\nA: 'Yes, but just a tad...'")


Execute a command in the guest::

    > ipython
    In [1]: import virtualbox

    In [2]: vbox = virtualbox.VirtualBox()

    In [3]: vm = vbox.find_machine('test_vm')

    In [4]: session = vm.create_session() 

    In [5]: gs = session.console.guest.create_session('Michael Dorman', 'password')

    In [6]: process, stdout, stderr = gs.execute('C:\\Windows\\System32\\cmd.exe', ['/C', 'tasklist'])

    In [7]: print stdout

    Image Name                   PID Session Name     Session#    Mem Usage
    ========================= ====== ================ ======== ============
    System Idle Process            0 Console                 0         28 K
    System                         4 Console                 0        236 K
    smss.exe                     532 Console                 0        432 K
    csrss.exe                    596 Console                 0      3,440 K
    winlogon.exe                 620 Console                 0      2,380 K
    services.exe                 664 Console                 0      3,780 K
    lsass.exe                    676 Console                 0      6,276 K
    VBoxService.exe              856 Console                 0      3,972 K
    svchost.exe                  900 Console                 0      4,908 K
    svchost.exe                 1016 Console                 0      4,264 K
    svchost.exe                 1144 Console                 0     18,344 K
    svchost.exe                 1268 Console                 0      2,992 K
    svchost.exe                 1372 Console                 0      3,948 K
    spoolsv.exe                 1468 Console                 0      4,712 K
    svchost.exe                 2000 Console                 0      3,856 K
    wuauclt.exe                  400 Console                 0      7,176 K
    alg.exe                     1092 Console                 0      3,656 K
    wscntfy.exe                 1532 Console                 0      2,396 K
    explorer.exe                1728 Console                 0     14,796 K
    wmiprvse.exe                1832 Console                 0      7,096 K
    VBoxTray.exe                1940 Console                 0      3,196 K
    ctfmon.exe                  1948 Console                 0      3,292 K
    cmd.exe                     1284 Console                 0      2,576 K
    tasklist.exe                 124 Console                 0      4,584 K


Using context to manage opened sessions and locks::

    > ipython
    In [1]: import virtualbox

    In [2]: vbox = virtualbox.VirtualBox()

    In [3]: vm = vbox.find_machine('test_vm')

    In [4]: with vm.create_session() as session:
       ...:     with session.console.guest.create_session('Michael Dorman', 'password') as gs:
       ...:         print(gs.directory_exists("C:\\Windows"))
       ...:         
    True


On an already running VM, register to receive on guest keyboard events::

    >ipython
    In [1]: from virtualbox import library

    In [2]: import virtualbox

    In [3]: vbox = virtualbox.VirtualBox()

    In [4]: vm = vbox.find_machine('test_vm')

    In [5]: s = vm.create_session()

    In [6]: def test(a):
       ...:     print(a.scancodes)
       ...:     

    In [7]: s.console.keyboard.set_on_guest_keyboard(test)
    Out[7]: 140448201250560

    In [8]: [35]
    [23]
    [163]
    [151]
    [57]
    [185]
    [35]
    [24]
    [163]
    [152]



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

version 0.1.1 (17/02/2014)

* Minor improvements
* Additional extensions
* virtualenv support

version 0.1   (05/01/2014)

* As per roadmap v0.1
* type checking baseinteger 
* update to latests Xidl 

version 0.0.7 (09/10/2013)

* machine pool

version 0.0.6 (25/07/2013)

* now with event support

version 0.0.5 (23/07/2013)

* moved manage into library_ext Interfaces
* made library.py compatible with differences found between xpcom and COM
  (Linux Vs Windows)

version 0.0.4 (27/06/2013)

* added execute, context and keyboard

version 0.0.3 (30/05/2012)

* added manage

version 0.0.2 (28/05/2013)

* library ext module

version 0.0.1 (27/05/2013)

* packaged

version 0.0.0 (20/05/2013)

* builder 
* library primitives 





.. _readthedocs.org: https://pyvbox.readthedocs.org/en/latest/
.. _github.com: https://github.com/mjdorma/pyvbox
.. _PyPi: http://pypi.python.org/pypi/pyvbox
