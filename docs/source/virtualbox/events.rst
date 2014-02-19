:mod:`virtualbox.events` -- registration, listening and processing
==================================================================

.. module:: virtualbox.events
    :synopsis: pyvbox
.. moduleauthor:: Michael Dorman <mjdorma+pyvbox@gmail.com>
.. sectionauthor:: Michael Dorman <mjdorma+pyvbox@gmail.com>

.. :py:mod:: virtualbox.events

The `virtualbox.events` module is responsible for the registering and
unregistering callback functions against a specific event source and event 
type.  

All callbacks registered by this module will be cleared *atexit*.  


Code reference
--------------

.. method:: register_callback(callback, event_source, event_type)

    Register a callback function against an event_source for a given
    event_type.  

    Any object in the VirtualBox API that generates an event aggregates an
    event_source (IEventSource) object through its interface object.  Specific
    event_type's (VBoxEventType) can be raised through this event_source.

    Once a listener has been created and registered through to the VBoxSvr, a
    thread is spawned to block on the *event_source.get_event* call.  When an
    event (IEvent) is successfully read, the callback will be called with a
    type case from the IEvent object to the Interface type that has an id of
    specific VBoxEventType that has been listened too. 

    An Integer is returned from this register_callback which is used as the ID
    of the registered callback function.  


    The following code snippet demonstrates how a callback can be registered
    against a specific event_type. ::
        
        def on_property_change(event):
            print("%s %s %s" % (event.name, event.value, event.flags))

        vbox = virtualbox.VirtualBox()
        event.register_callback(on_property_change, vbox.event_source, 
                                library.VBoxEventType.on_guest_property_changed)


.. method:: unregister_callback(callback_id)

    Unregister a callback function using the callback_id returned from the
    register_callback method.

    Each event listener blocks on an event read for 1 second than checks the
    listener's quit Event status.  




