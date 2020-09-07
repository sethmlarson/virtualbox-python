"""Manage VBoxEvent, registration, listening and processing

By Michael Dorman
[mjdorma+pyvbox@gmail.com]
"""
from __future__ import print_function
import sys
import atexit
import inspect
import traceback
import threading

from virtualbox import library


_lookup = {}


def type_to_interface(event_type):
    """Return the event interface object that corresponds to the event type
    enumeration"""
    global _lookup
    if not isinstance(event_type, library.VBoxEventType):
        raise TypeError("event_type was not of VBoxEventType")
    if not _lookup:
        for attr in dir(library):
            event_interface = getattr(library, attr)
            if not inspect.isclass(event_interface):
                continue
            if not issubclass(event_interface, library.Interface):
                continue
            et = getattr(event_interface, "id", None)
            if et is None:
                continue
            if not isinstance(et, library.VBoxEventType):
                continue
            _lookup[int(et)] = event_interface
    return _lookup[int(event_type)]


_callbacks = {}


def _event_monitor(callback, event_source, listener, event_interface, quit):
    global _callbacks
    try:
        while not quit.is_set():
            try:
                event = event_source.get_event(listener, 1000)
            except library.VBoxError:
                print(
                    "Unregistering %s due to VBoxError on get_event" % listener,
                    file=sys.stderr,
                )
                break
            if event:
                try:
                    callback(event_interface(event))
                except Exception:
                    print(
                        "Unhanded exception in callback: \n%s" % traceback.format_exc(),
                        file=sys.stderr,
                    )
                event_source.event_processed(listener, event)
    finally:
        _callbacks.pop(threading.current_thread().ident, None)
        try:
            event_source.unregister_listener(listener)
        except Exception:
            print("Failed to unregister listener %s" % listener, file=sys.stderr)


def register_callback(callback, event_source, event_type):
    """register a callback function against an event_source for a given
    event_type.

    Arguments:
        callback - function to call when the event occurs
        event_source - the source to monitor events in
        event_type - the type of event we're monitoring for

    returns the registration id (callback_id)
    """
    global _callbacks
    event_interface = type_to_interface(event_type)
    listener = event_source.create_listener()
    event_source.register_listener(listener, [event_type], False)
    quit = threading.Event()
    t = threading.Thread(
        target=_event_monitor,
        args=(callback, event_source, listener, event_interface, quit),
    )
    t.daemon = True
    t.start()
    while t.is_alive() is False:
        continue
    _callbacks[t.ident] = (t, quit)
    return t.ident


def unregister_callback(callback_id):
    """unregister a callback registration"""
    global _callbacks
    obj = _callbacks.pop(callback_id, None)
    threads = []
    if obj is not None:
        t, quit = obj
        quit.set()
        threads.append(t)
    for t in threads:
        t.join()


def _remove_all_callbacks():
    global _callbacks
    for callback_id in list(_callbacks):
        unregister_callback(callback_id)


atexit.register(_remove_all_callbacks)
