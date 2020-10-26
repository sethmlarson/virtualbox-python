Changelog
=========

2.1.1 (10/26/2020)
------------------

* Fix bug in VirtualBox API specification where ``VBoxEventType.progress_event`` and
  ``VBoxEventType.on_cloud_provider_can_uninstall`` are both mentioned but are not valid event types.

2.1.0 (10/25/2020)
----------------

* Added support for VirtualBox 6.1

2.0.0 (4/2/2019)
----------------

* Added support for VirtualBox 6.0:  
   
   * Added new Recording features
   * Added support configuring network proxies
   * Added support for Cloud features
   * Added new CPU, Hardware, and Virt property types
   * Added new event and error types
* Renamed the PyPI project from ``pyvbox`` to ``virtualbox`` (Installing ``pyvbox`` still works).
* Fixed a bug with streaming output from a console command.
* Dropped explicit support for Python 2.6 and 3.3 (May still work?).
* This is a new major version and many argument and function names have
  changed. Version 2.x of this library only supports VirtualBox 6.0+.

1.3.2 (21/02/2018)
------------------

* Fixed `__name__` which made Python 3 installs break.

1.3.1 (18/01/2018)
------------------

* Added ``SettingsVersion.v1_17`` which is written by VirtualBox 5.2.x
* Added ``VirtualBox.create_unattended_installer()``
* Added ``IUnattended`` interface which can be used to create a Guest OS
  in a fully automated way. (Doesn't work yet in 5.2 beta)
* Added ``IHostNetworkInterface.wireless`` property which returns
  ``True`` if the interface is wireless.

1.2.0 (28/08/2017)
------------------

* Searches for vboxapi installed in Anaconda on Windows. (@sethmlarson PR #80)
* Added ``__lt__`` and ``__gt__`` methods for orderability on Python 3. (@sethmlarson PR #82)

1.1.0 (02/06/2017)
------------------

* IGuest.create_session() now raises a more descriptive error if
  not able to connect with a zero-length password. (@sethmlarson PR #70)
* Add sys.executable-derived paths in list to check for vboxapi (@sethmlarson PR #69)
* Fix IGuestProcess.execute() on Python 3.x (@sethmlarson PR #58)
* Fix errors to not output on Windows platforms. (@sethmlarson PR #57)
* Fix error caused by attempting to set any attribute in the COM interface
  using setattr raising an error. (Reported by @josepegerent, patch by @sethmlarson PR #74)

1.0.0 (18/01/2017)
------------------

* Support for 5.0.x VirtualBox.
* Introduce Major.Minor virtualbox build version assertion when creating a VirtualBox
  instance.
* Fix to IMachine.export_to (contribution from @z00m1n).

0.2.2 (05/08/2015)
------------------

* Cleanup managers at exit (reported by @jiml521).
* Add three time check for attribute in xpcom interface object before failing (reported
  by @shohamp).
* Update library.py to 4.3.28/src/VBox/Main/idl/VirtualBox.xidl

0.2.0
-----

* This change introduces some significant (potential compatability breaking)
  updates from the latest VirtualBox.xidl.
* Bug fixes in IMachine (reported by @danikdanik).
* IHost API issue workaround by @wndhydrnt.

0.1.6 (01/08/2014)
------------------

* Bug fixes (compatability issue with py26 and virtual keyboard).
* Thanks to contributions by @D4rkC4t and @Guilherme Moro.

0.1.5 (11/05/2014)
------------------

* Improve error handling and documentation of error types.
* Appliance extension.
* Update to latest API (includes Paravirt provider).
* Thanks to contributions by @nilp0inter

0.1.4 (09/04/2014)
------------------

* Fixed bug in error class container.

0.1.3 (04/03/2014)
------------------

* Bug fix for API support.
* Added markup generation to library documentation.
* Improved Manager bootstrap design.
* Py3 compatibility (although vboxapi does not support py3).

0.1.2 (28/02/2014)
------------------

* Bug fix for virtualenv support
* `Keyboard scancode decoder`_ (Note: coded in the delivery suite on the day of
  the birth of my baby girl Sophia.)
* Refactored documentation

0.1.1 (17/02/2014)
------------------

* Minor improvements
* Additional extensions
* virtualenv support

0.1 (05/01/2014)
----------------

* As per roadmap v0.1
* type checking baseinteger
* update to latests Xidl

0.0.7 (09/10/2013)
------------------

* machine pool

0.0.6 (25/07/2013)
------------------

* now with event support

0.0.5 (23/07/2013)
------------------

* moved manage into library_ext Interfaces
* made library.py compatible with differences found between xpcom and COM
  (Linux Vs Windows)

0.0.4 (27/06/2013)
------------------

* added execute, context, and keyboard

0.0.3 (30/05/2012)
------------------

* added manage

0.0.2 (28/05/2013)
------------------

* library ext module

0.0.1 (27/05/2013)
------------------

* packaged

0.0.0 (20/05/2013)
------------------

* builder
* library primitives

.. _Keyboard scancode decoder: https://gist.github.com/mjdorma/9132605
