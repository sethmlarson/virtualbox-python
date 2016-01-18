Change log
==========

version 1.0.0

* Support for 5.0.x VirtualBox.
* Introduce Major.Minor virtualbox build version assertion when creating a VirtualBox
  instance.
* Fix to iMachine.export_to (contribution from @z00m1n).

version 0.2.2

* Cleanup managers at exiti (reported by @jiml521).
* Add three time check for attribute in xpcom interface object before failing (reported
  by @shohamp). 
* Update library.py to 4.3.28/src/VBox/Main/idl/VirtualBox.xidl

version 0.2.0

* This change introduces some significant (potential compatability breaking) 
  updates from the latest VirtualBox.xidl.
* Bug fixes in IMachine (reported by @danikdanik).
* IHost API issue workaround by @wndhydrnt.

version 0.1.6

* Bug fixes (compatability issue with py26 and virtual keyboard).
* Thanks to contributions by @D4rkC4t and @Guilherme Moro.

version 0.1.5 

* Improve error handling and documentation of error types.
* Appliance extension.
* Update to latest API (includes Paravirt provider).
* Thanks to contributions by @nilp0inter

version 0.1.4 (09/04/2014)
 
* Fixed bug in error class container.

version 0.1.3 (04/03/2014)

* Bug fix for API support.
* Added markup generation to library documentation.
* Improved Manager bootstrap design.
* Py3 compatibility (although vboxapi does not support py3).

version 0.1.2 (28/02/2014)

* Bug fix for virtualenv support
* `Keyboard scancode decoder`_ (Note: coded in the delivery suite on the day of
  the birth of my baby girl Sophia.)
* Refactored documentation

version 0.1.1 (17/02/2014)

* Minor improvements
* Additional extensions
* virtualenv support

version 0.1   (05/01/2014)

* As per roadmap v0.1
* type checking baseinteger 
* update to latests Xidl 

version 0.0.7 (09/10/2013)

* `machine pool`_

version 0.0.6 (25/07/2013)

* now with `event support`_

version 0.0.5 (23/07/2013)

* moved manage into library_ext Interfaces
* made library.py compatible with differences found between xpcom and COM
  (Linux Vs Windows)

version 0.0.4 (27/06/2013)

* added execute, context, and keyboard

version 0.0.3 (30/05/2012)

* added manage

version 0.0.2 (28/05/2013)

* `library ext module`_

version 0.0.1 (27/05/2013)

* packaged

version 0.0.0 (20/05/2013)

* builder 
* library primitives 


.. _event support: http://pythonhosted.org//pyvbox/virtualbox/events.html
.. _library ext module: http://pythonhosted.org/pyvbox/virtualbox/library_ext.html
.. _machine pool: http://pythonhosted.org/pyvbox/virtualbox/pool.html
.. _Keyboard scancode decoder: https://gist.github.com/mjdorma/9132605
