import time

from virtualbox import library

"""
Add helper code to the default IGuest class.
"""


# Define some default params for create session 
class IGuest(library.IGuest):
    __doc__ = library.IGuest.__doc__
    def create_session(self, user, password, domain='', session_name='pyvbox',
                        timeout_ms=0):
        session = super(IGuest, self).create_session(user, password, domain,
                                                    session_name)
        if timeout_ms != 0:
            # There is probably a better way to to this?
            if 'win' in self.os_type_id.lower():
                test_file = 'C:\\autoexec.bat'
            else:
                test_file = '/bin/sh'
            while True:
                try:
                    session.file_query_info(test_file)
                except library.VBoxError as err:
                    time.sleep(0.5)
                    timeout_ms -= 500
                    if timeout_ms <= 0:
                        raise
                    continue
                break
        return session
    create_session.__doc__ = library.IGuest.create_session.__doc__



