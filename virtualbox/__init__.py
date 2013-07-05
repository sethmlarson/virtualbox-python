from _library_ext import library

__doc__ = library.__doc__


VirtualBox = library.IVirtualBox
Session = library.ISession


class Manager(object):
    manager = None
    def __init__(self):
        """Create a default Manager object
        
        Builds a singleton VirtualBoxManager object.

        Note: It is not necessary to build this object when defining an
        Session or VirtualBox object as both of these classes will default
        to this object's global singleton during construction. 
        """
        if Manager.manager is None:
            import vboxapi
            Manager.manager = vboxapi.VirtualBoxManager(None, None)
        self.manager = Manager.manager

    def get_virtualbox(self):
        return self.manager.getVirtualBox()

    def get_session(self):
        return self.manager.getSessionObject(None)


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

