from library_ext import library

__doc__ = library.__doc__


VirtualBox = library.IVirtualBox
Session = library.ISession


class Manager(object):
    manager = None
    def __init__(self):
        """Create a default Manager object
        
        Builds a singleton VirtualBoxManager object.

        Note: It is not necessary to build this object when defining a
        Session or VirtualBox object as both of these classes will default
        to this object's global singleton during construction. 
        """
        if Manager.manager is None:
            import vboxapi
            Manager.manager = vboxapi.VirtualBoxManager(None, None)
        self.manager = Manager.manager

    def get_virtualbox(self):
        """Return a VirtualBox interface"""
        return VirtualBox(interface=self.manager.getVirtualBox())

    def get_session(self):
        """Return a Session interface"""
        # The inconsistent vboxapi implementation makes this annoying...
        if hasattr(self.manager, 'mgr'):
            manager = getattr(self.manager, 'mgr')
        else:
            manager = self.manager
        return Session(interface=manager.getSessionObject(None))

    def cast_object(self, interface_object, interface_class):
        """Cast the obj to the interface class"""
        name = interface_class.__name__
        i = self.manager.queryInterface(interface_object._i, name)
        return interface_class(interface=i)

    @property
    def bin_path(self):
        """return the virtualbox install directory"""
        return self.manager.getBinDir()


class WebServiceManager(Manager):
    def __init__(url='http://localhost/', user='', password=''):
        """Create a VirtualBoxManager WEBSERVICE manager for IVirtualBox
        
        Options:
            url - url to connect with the VirtualBox server 
            user - username used to auth to the VirtualBox server service
            password - password used to auth to the VirtualBox server service

        Example:
            manager = WebServiceManager(user="mick", password="password")
            vbox = VirtualBox(manager=manager)
            ...
        """
        import vboxapi
        params = (url, user, password)
        self.manager = vboxapi.VirtualBoxManager("WEBSERVICE", params)

