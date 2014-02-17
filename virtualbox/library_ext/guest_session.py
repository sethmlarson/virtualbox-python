import time

from virtualbox import library

"""
Add helper code to the default IGuestSession class.
"""


# Add context management to IGuestSession
class IGuestSession(library.IGuestSession):
    __doc__ = library.IGuestSession.__doc__
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.close()

    def execute(self, command, arguments=[], stdin="", environment=[],
                 flags=[library.ProcessCreateFlag.wait_for_std_err,
                        library.ProcessCreateFlag.wait_for_std_out,
                        library.ProcessCreateFlag.ignore_orphaned_processes],
                 priority=library.ProcessPriority.default,
                 affinity=[], timeout_ms=0):
        """Execute a command in the Guest

            Arguments:
                command - Command to execute.
                arguments - List of arguments for the command
                stdin - A buffer to write to the stdin of the command.
                environment - See IGuestSession.create_process?
                flags - List of ProcessCreateFlag objects.  
                    Default value set to [wait_for_std_err, 
                                          wait_for_stdout,
                                          ignore_orphaned_processes]
                timeout_ms - ms to wait for the process to complete.  
                    If 0, wait for ever... 
                priority - Set the ProcessPriority priority to be used for
                    execution.
                affinity - Process affinity to use for execution. 

            Return IProcess, stdout, stderr 
        """
        def read_out(process, flags, stdout, stderr):
            if library.ProcessCreateFlag.wait_for_std_err in flags:
                e = str(process.read(2, 65000, 0))
                stderr.append(e)
            if library.ProcessCreateFlag.wait_for_std_out in flags:
                o = str(process.read(1, 65000, 0))
                stdout.append(o)

        process = self.process_create_ex(command, arguments, environment,
                            flags, timeout_ms, priority, affinity)
        process.wait_for(int(library.ProcessWaitResult.start), 0)

        # write stdin to the process 
        if stdin:
            index = 0
            while index < len(stdin):
                index += process.write(0, [library.ProcessInputFlag.none], 
                                        stdin[index:], 0)
            process.write(0, [library.ProcessInputFlag.end_of_file], 0)

        # read the process output and wait for 
        stdout = []
        stderr = []
        while process.status == library.ProcessStatus.started:
            read_out(process, flags, stdout, stderr)
            time.sleep(0.2)
        # make sure we have read the remainder of the out
        read_out(process, flags, stdout, stderr)
        return process, "".join(stdout), "".join(stderr)

    def makedirs(self, path, mode=0x777):
        """Super-mkdir: create a leaf directory and all intermediate ones."""
        self.directory_create(path, mode, [library.DirectoryCreateFlag.parents])

    # Simplify calling directory_remove_recursive.  Set default flags to
    # content_and_dir if they have not yet been set.
    def directory_remove_recursive(self, path, flags=None):
        if flags is None:
            flags = [library.DirectoryRemoveRecFlag.content_and_dir]
        super(IGuestSession, self).directory_remove_recursive(path, flags)
    directory_remove_recursive.__doc__ = \
            library.IGuestSession.directory_remove_recursive.__doc__

    def copy_to_vm(self, host_path, guest_path):
        "Copy a single file to the vm. Wraps copy_to."
        if not os.path.exists(host_path):
            raise OSError("Failed to find %s on host" % host_path)
        p = self.copy_to_vm(host_path, guest_path, [])
        p.wait_for_completion()
        return p

    def copy_from_vm(self, guest_path, host_path):
        "Copy a single file from the vm. Wraps copy_from."
        # Dodgy exists check...
        for x in range(10):
            try:
                self.file_exists(guest_path)
                break
            except:
                time.sleep(0.1)
        else:
            raise OSError("Failed to find %s on guest" % guest_path)    
        p = self.copy_from(guest_path, host_path, [])
        p.wait_for_completion()
        return p



    
