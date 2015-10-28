:mod:`virtualbox.library_ext` -- extensions to *virtualbox.library*
===================================================================

.. module:: virtualbox.library_ext
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


Code reference
--------------

The documentation captured in this reference reflects the extensions or fixes
applied to the default library.py.   


.. py:class:: IVirtualBox([interface, manager])

    The VirtualBox interface object is the primary interface into VirtualBox's
    COM API.  The default constructor can take a `library.Interface` object or
    a `virtualbox.Manager` object.

    .. method:: register_on_machine_state_changed(callback)

        The *callback* function is called with a *IMachineStateChangedEvent*
        argument on a machine state changed event.

        :: 
            
            def callback(event):
                print("Machine %s state changed to %s" % (event.machine_id,
                                                          event.state))

            vbox = virtualbox.VirtualBox()
            vbox.register_on_machine_state_changed(callback)

    .. method:: register_on_machine_data_changed(callback)

        The *callback* function is called with a *IMachineDataChangedEvent*
        argument on a machine state changed event.

        :: 
          
            def callback(event):
                print("Settings data changed for %s" % event.machine_id)

            vbox = virtualbox.VirtualBox()
            vbox.register_on_machine_data_changed(callback)

    .. method:: register_on_machine_registered(callback)

        The *callback* function is called with a *IMachineRegisteredEvent*
        argument on a machine registered event.

        :: 
             
            def callback(event):
                if event.registered:
                    action = 'registered'
                else:
                    action = 'unregistered'
                print("%s was %s" % (event.machine_id, action))

            vbox = virtualbox.VirtualBox()
            vbox.register_on_machine_registered(callback)

     .. method:: register_on_snapshot_deleted(callback)

        The *callback* function is called with a *ISnapshotDeletedEvent*
        argument on a snapshot deleted event.

        :: 
            
            def callback(event):
                print(event.snapshot_id)

            vbox = virtualbox.VirtualBox()
            vbox.register_on_snapshot_deleted(callback)
 
    .. method:: register_on_snapshot_taken(callback)

        The *callback* function is called with a *ISnapshotTakenEvent*
        argument on a snapshot taken event.

        :: 
                    
            def callback(event):
                print(event.snapshot_id)

            vbox = virtualbox.VirtualBox()
            vbox.register_on_snapshot_taken(callback)

    .. method:: register_on_snapshot_changed(callback)

        The *callback* function is called with a *ISnapshotChangedEvent* 
        argument on a snapshot changed event.

        :: 
                    
            def callback(event):
                print(event.snapshot_id)

            vbox = virtualbox.VirtualBox()
            vbox.register_on_snapshot_changed(callback)

    .. method:: register_on_guest_property_changed(callback)

        The *callback* function is called with a *IGuestPropertyChangedEvent*
        argument on a guest property changed event.

        :: 
                    
            def callback(event):
                print("%s %s %s" % (event.name, event.value, event.flags))

            vbox = virtualbox.VirtualBox()
            vbox.register_on_guest_property_changed(callback)

    .. method:: register_on_session_state_changed(callback)

        The *callback* function is called with a *ISessionStateChangedEvent*
        argument on a session state changed event.

        :: 
                    
            def callback(event):
                print("Session on machine %s is %s" % (event.machine_id,
                                                       event.state))

            vbox = virtualbox.VirtualBox()
            vbox.register_on_session_state_changed(callback)

    .. method:: register_on_event_source_changed(callback)

        The *callback* function is called with a *IEventSourceChangedEvent* on a
        event source changed event.  This occurs when a listener is added or
        removed.

        :: 
                    
            def callback(event):
                if event.add:
                    action = 'added'
                else:
                    action = 'removed'
                print("A listener was %s from vbox's event_source %s" % \
                        action)

            vbox.register_on_event_source_changed(callback)

    .. method:: register_on_extra_data_changed(callback)

        The *callback* function is called with a *IExtraDataChangedEvent*
        argument on a extra data changed event.

        :: 
                    
            def callback(event):
                print("%s %s=%s" % (event.machine_id, event.key, event.value))

            vbox = virtualbox.VirtualBox()
            vbox.register_on_extra_data_changed(callback)

    .. method:: register_on_extra_data_can_change(callback)

        The *callback* function is called with a *IExtraDataCanChangeEvent*
        argument on a extra data can change event.

        :: 
                    
            def callback(event):
                if event.key == 'blah':
                    print("Veto served")
                    event.add_veto("blah is mine...")
                else:
                    print("Allow %s %s" % (event.key, event.value))

            vbox = virtualbox.VirtualBox()
            vbox.register_on_extra_data_can_change(callback)

        To see this work simply run the following vboxmanage command::
        
            vboxmanage setextradata global blah winner


.. py:class:: ISession()

    Just like the *IVirtualBox* interface the *ISession* can be bootstrapped
    from a *virtualbox.Manager* object.  This is special in that it represents
    a client process and allows for locking virtual machines. 

    To reduce complexity over management of an *ISession* lock, the base class
    has been extended to implement the *context management protocol*.  

    Using an ISession object::

        vbox = virtualbox.VirtualBox()
        vm = vbox.find_machine('test_vm')
        with vm.create_session() as session:
            #do stuff with the session



.. py:class:: IGuest()

    .. method:: create_session(user, password, [domain, \
                                                session_name, timeout_ms])
        
        This method extends the default *IGuest.create_session* method by
        adding a polling block operation that waits for the guest session to be
        ready.   It also defaults the values of *domain* to '' and
        *session_name* to 'pyvbox'.

        If *timeout_ms* is not equal to 0, this method block until the session
        is ready and active for querying the Guest operating system.  This test
        is performed by polling for the existence of *C:\autoexec.bat* or
        */bin/sh*.  If the timeout is exceeded a VBoxError will be raised.

        Returns a IGuestSession object on completion. 

    .. method:: update_guest_addtions([source, arguments, flags])

        BUG FIX: This method fixes the bug in the definition for the
        *updateGuestAdditions* method.  In the API definition this function is
        defined to take a list of *arguments* but the implementation only takes
        *source* and *flags*.  

        As an extension to this method, *source* is now an optional arguemnt.
        If the *source* path for the update ISO is not provided, this method
        will attempt to find a copy of the VBoxGuestAdditions.iso file from the
        VirtualBox install path. 

        Returns an IProgress object


.. py:class:: IGuestSession()

    When an IGuestSession is created, it requires that the session is
    explicitly closed after its use.  This is done by calling the
    *IGuestSession.close* method.  To simply this behaviour, the default class
    has been extended to implement the *context management protocol*.

    Using an IGuestSession ojbect::

        guest = session.console.guest
        with guest.create_session('user', 'password') as guest_session:
            #do stuff with the guest session


    .. method:: execute(command, [arguments, stdin, environment, flags, \
                                  priority, affinity, timeout_ms])

        Execute a command in the guest

        
.. py:class:: IEventSource()

    .. method:: register_callback(callback, event_type)
        
        provide a helper function that wraps the *events.register_callback*
        method.  *callback* is the function to be called back when this
        *IEventSource* raises *event_type*. 


.. py:class:: IKeyboard()

    .. method:: put_keys([press_keys, hold_keys, press_delay])
        
        Press the keys listed by the *press_keys* list into the *IKeyboard*
        whilst holding down the *hold_keys*.  Control the press speed by
        defining the *press_delay* which is the number of milliseconds between
        each press.

        For a full list of defined keys, refer to::
        
            virtualbox.library.IKeyboard.SCANCODES.keys()
        
    .. method:: register_on_guest_keyboard(callback)

        The *callback* function is called with a *IGuestKeyboardEvent* argument
        when a guest keyboard event occurs. 

        :: 
                    
            def callback(event):
                print(event.scancodes)

            session.console.keyboard.register_on_guest_keyboard(callback)


.. py:class:: IMouse()

    .. method:: register_on_guest_mouse(callback)

        The *callback* function is called with a *IGuestMouseEvent* argument
        when mouse event occurs. 

        :: 
                    
            def callback(event):
                print(("%s %s %s" % (event.x, event.y, event.z)) 

            session.console.mouse.set_guest_mouse(callback)
        

.. py:class:: IProgress()

    .. method:: __str__()

        Returns a progress string in a human readable format.


.. py:class:: IMachine()

    .. method:: remove([delete])
        
        Unregister and delete this *Machine*.  If *delete* is set to False, the
        machine will only be detached and unregistered from the VBoxSvr.

    .. method:: clone([snapshot_name_or_id, \
                       mode, options, name, \
                       uuid, groups, basefolder, register])
                        
        Clone this *Machine*.  The options for this method have been setup to
        default create a linked clone.  Depending on the mode and the options
        VirtualBox will require the *Machine* to have different state. 

        To clone from a snapshot, the *snapshot_name_or_id* value needs to
        be defined.  This value can be either an ISnapshot object or a unicode
        or str value for the name or the id of a snapshot. 

        If *name* is not defined, the chosen name will be the name of this
        *Machine* concatenated with " Clone".  When deciding a final name, this
        method will check if the name already exists.  If it exists, it will
        automatically append " (N)" to the end of the name string where N is
        the number that did not exist. 

        To understand the complexities behind the options of this method,
        please read through the documentation for the
        *library.IVirtualBox.create_machine* and *library.IMachine.clone_to*
        methods. 

    .. method:: delete_config(media)
        
        BUG FIX:  This method fixes a bug in the interface definition for the
        default method name 'deleteConfig'.  As it turns out, the actual name
        implemented is 'delete'.

    .. method:: create_session([lock_type, session])

        A helper function to simplify the creation of a *ISession* lock over
        this *Machine*.  *lock_type* defaults to *library.LockType.shared*.
        If *session* is not passed in, a new ISession object is created and
        returned. 

    .. method:: launch_vm_process([session, type_p, environment])

        This method sets the default values for the original
        *IMachine.launch_vm_process*.  If *session* is not defined it will be
        created and on completion of the launch, will be unlocked.  *type_p* is
        set to default 'gui' and *environment* is set to default ''.


.. py:class:: IConsole()

    .. method:: restore_snapshot([snapshot])
        
        *snapshot* is now an optional argument.  If it is not supplied, an
        attempt to pull the *machine.current_snapshot* is made, if there is no
        snapshot available, an Exception is raised.

    .. method:: register_on_network_adapter_changed(callback)

        The *callback* function is called with a *INetworkAdapterChangedEvent*
        argument when a network adapter changed event occurs.

        :: 
                    
            def callback(event):
                adapter = event.network_adapter
                print("Enabled = %s, connected = %s" % (adapter.enabled,
                                                 adapter.cable_connected))

            session.console.register_on_network_adapter_changed(callback)

    .. method:: register_on_serial_port_changed(callback)

        The *callback* function is called with a *ISerialPortChangedEvent*
        argument when a serial port changed event occurs.

        :: 

            def callback(event):
                port = event.serial_port
                print("Enabled = %s, path = %s" % (port.enabled,
                                                   port.path))

            session.console.register_on_serial_port_changed(callback)

    .. method:: register_on_parallel_port_changed(callback)

        The *callback* function is called with a *IParallelPortChangedEvent*
        argument on a parallel port changed event.

        :: 
                    
            def callback(event):
                port = event.parallel_port
                print("Enabled = %s, path = %s" % (port.enabled,
                                                   port.path))

            session.console.register_on_parallel_port_changed(callback)       

    .. method:: register_on_medium_changed(callback)

        The *callback* function is called with a *IMediumChangedEvent* on a
        medium changed event.

        :: 
                    
            def callback(event):
                medium = event.medimum_attachment
                print(medium.controller)

            session.console.register_on_medium_changed(callback)

    .. method:: register_on_clipboard_mode_changed(callback)

        The *callback* function is called with a *IClipboardModeChangedEvent*
        on a clipboard mode changed event.

        :: 
                    
            def callback(event):
                print(event.clipboard_mode)

            session.console.register_on_clipboard_mode_changed(callback)

    .. method:: register_on_drag_and_drop_mode_changed(callback)

        The *callback* function is called with a *IDragAndDropModeChangedEvent*
        on a drag and drop mode changed event.

        :: 
                    
            def callback(event):
                print(event.drag_and_drop_mode)

            session.console.register_on_drag_and_drop_mode_changed(callback)

    .. method:: register_on_vrde_server_changed(callback)

        The *callback* function is called with a *IVRDEServerChangedEvent*
        on a drag and drop mode changed event.

        :: 
                    
            def callback(event):
                print("VirtualBox remote display extension server changed")

            session.console.register_vdre_server_changed(callback)

    .. method:: register_on_additions_state_changed(callback)

        The *callback* function is called with a *IAdditionsStateChangedEvent*
        argument on a additions state changed event.  To find out what has
        changed, a probe into the attributes of IGuest is required.

        :: 
                    
            def callback(event):
                print("State changed in IGuest...")

            session.console.register_on_additions_state_changed(callback)

    .. method:: register_on_shared_folder_changed(callback)

        The *callback* function is called with a *ISharedFolderChangedEvent*
        argument on a shared folder changed event.

        :: 
                    
            def callback(event):
                print("Folder changed scope %s" % event.scope)

            session.console.register_on_shared_folder_changed(callback)

    .. method:: register_on_state_changed(callback)

        The *callback* function is called with a *IStateChangedEvent* on a
        machine state changed event.

        :: 
                    
            def callback(event):
                print("State changed to %s" % event.state)

            session.console.register_on_state_changed(callback)

    .. method:: register_on_event_source_changed(callback)

        The *callback* function is called with a *IEventSourceChangedEvent* on a
        event source changed event.  This occurs when a listener is added or
        removed.

        :: 
                    
            def callback(event):
                if event.add:
                    action = 'added'
                else:
                    action = 'removed'
                print("A listener was %s from console's event_source %s" % \
                        action)

            session.console.register_on_event_source_changed(callback)

    .. method:: register_on_can_show_window(callback)

        The *callback* function is called with a *ICanShowWindowEvent* on a
        show window event.  This occurs when the console window is to be
        activated and brought to the foreground of the desktop of the host PC.
        If this behaviour is not desired a call to event.add_veto will stop
        this from happening. 

        :: 
                    
            def callback(event):
                print("veto this event")
                event.add_veto("No you shall never do this!")

            session.console.register_on_can_show_window(callback)

    .. method:: register_on_show_window(callback)

        The *callback* function is called with a *IShowWindowEvent* on a show
        window event.  This occurs when the console window is to be activated
        and brought to the foreground of the desktop of the host PC.

        :: 
                    
            def callback(event):
                print("Window id = %s" % event.win_id)

            session.console.register_on_show_window(callback)


