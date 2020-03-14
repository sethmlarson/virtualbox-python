virtualbox-python
*****************

.. image:: https://img.shields.io/travis/sethmlarson/virtualbox-python/master.svg
   :target: https://travis-ci.org/sethmlarson/virtualbox-python

Complete implementation of VirtualBox's COM API with a Pythonic interface.

Installation
============

Go to VirtualBox's downloads page (https://www.virtualbox.org/wiki/Downloads) and download the VirtualBox SDK.
Within the extracted ZIP file there is a directory called "installer". Open a console within the installer directory
and run ``python vboxapisetup.py install`` using your system Python. This installs ``vboxapi`` which is the interface
that talks to VirtualBox via COM.

Next is to install this library:

To get the latest released version of virtualbox from PyPI run the following::

    $ python -m pip install virtualbox
    
or to install the latest development version from GitHub::

    $ git clone https://github.com/sethmlarson/virtualbox-python
    $ cd virtualbox-python
    $ python setup.py install

Getting Started 
===============

Listing Available Machines
--------------------------

 .. code-block::

    >>> import virtualbox
    >>> vbox = virtualbox.VirtualBox()
    >>> [m.name for m in vbox.machines]
    ["windows"]

Launching a Machine
-------------------

  .. code-block::

    >>> session = virtualbox.Session()
    >>> machine = vbox.find_machine("windows")
    >>> # progress = machine.launch_vm_process(session, "gui", "")
    >>> # For virtualbox API 6_1 and above (VirtualBox 6.1.2+), use the following:
    >>> progress = machine.launch_vm_process(session, "gui", [])
    >>> progress.wait_for_completion()

Querying the Machine
--------------------

 .. code-block::

    >>> session.state
    SessionState(2)  # locked
    >>> machine.state
    MachineState(5)  # running
    >>> height, width, _, _, _, _ = session.console.display.get_screen_resolution()

Interacting with the Machine
----------------------------

 .. code-block::

    >>> session.console.keyboard.put_keys("Hello, world!")
    >>> guest_session = session.console.guest.create_session("Seth Larson", "password")
    >>> guest_session.directory_exists("C:\\Windows")
    True
    >>> proc, stdout, stderr = guest_session.execute("C:\\\\Windows\\System32\\cmd.exe", ["/C", "tasklist"])
    >>> print(stdout)
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

Registering Event Handlers
--------------------------

 .. code-block::

    >>> def test(event):
    >>>    print("scancode received: %r" % event.scancodes)
    >>>
    >>> session.console.keyboard.set_on_guest_keyboard(test)
    140448201250560
    scancode received: [35]
    scancode received: [23]
    scancode received: [163]
    scancode received: [151]
    scancode received: [57]

Powering-Down a Machine
-----------------------

  .. code-block::

    >>> session.console.power_down()

License
=======

Apache-2.0
