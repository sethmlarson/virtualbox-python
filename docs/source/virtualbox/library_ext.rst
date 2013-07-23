:mod:`virtualbox.library_ext` -- Shim class extensions to the library.py
========================================================================

.. module:: virualbox.library_ext
    :synopsis: pyvbox
.. moduleauthor:: Michael Dorman <mjdorma+pyvbox@gmail.com>
.. sectionauthor:: Michael Dorman <mjdorma+pyvbox@gmail.com>

.. :py:mod:: virtualbox.library_ext

The `virtualbox.library_ext` is a container package that makes it simple to
extend and replace the classes that have been automatically generated in
`virtualbox.library`.  

This simplifies the builder code significantly by not having to handle
specific edge cases where bugs have been identified in the VirtualBox.xidl
file.  It also makes it simple to redefine default behaviour, or simply add
various sugar to functions in an interface (such as defining defaults for
function parameters). 


.. note:: 

    The documentation captured in this page reflects the extensions or fixes
    applied to the default library.py.   



:py:class:`IGuest`
------------------

.. py:class:: IGuest()


:py:class:`IGuestSession`
-------------------------

.. py:class:: IGuestSession()


:py:class:`IKeyboard`
---------------------

.. py:class:: IKeyboard()


:py:class:`IProgress`
---------------------

.. py:class:: IProgress()


:py:class:`IMachine`
--------------------

.. py:class:: IMachine()




