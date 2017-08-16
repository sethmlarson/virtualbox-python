"""
Add helper code to the default IGuestSession class.
"""

import time
from virtualbox import library


# Add context management to IGuestSession
class IGuestSession(library.IGuestSession):
    __doc__ = library.IGuestSession.__doc__

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def execute(self, command, arguments=None, stdin="", environment=None,
                flags=None, priority=library.ProcessPriority.default,
                affinity=None, timeout_ms=0):
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
        if arguments is None:
            arguments = []
        if environment is None:
            environment = []
        if flags is None:
            flags = [library.ProcessCreateFlag.wait_for_std_err,
                     library.ProcessCreateFlag.wait_for_std_out,
                     library.ProcessCreateFlag.ignore_orphaned_processes]
        if affinity is None:
            affinity = []

        def read_out(process, flags, stdout, stderr):
            if library.ProcessCreateFlag.wait_for_std_err in flags:
                process.wait_for(int(library.ProcessWaitResult.std_err))
                e = bytes(process.read(2, 65000, 0))
                stderr.append(e)
            if library.ProcessCreateFlag.wait_for_std_out in flags:
                process.wait_for(int(library.ProcessWaitResult.std_out))
                o = bytes(process.read(1, 65000, 0))
                stdout.append(o)

        process = self.process_create_ex(command,
                                         [command] + arguments, environment,
                                         flags,
                                         timeout_ms,
                                         priority,
                                         affinity)

        process.wait_for(int(library.ProcessWaitResult.start), 0)

        # write stdin to the process
        if stdin:
            process.wait_for(int(library.ProcessWaitResult.std_in), 0)
            index = 0
            flag_none = [library.ProcessInputFlag.none]
            flag_eof = [library.ProcessInputFlag.end_of_file]
            while index < len(stdin):
                array = map(lambda a: str(ord(a)), stdin[index:])
                wrote = process.write_array(0, flag_none, array, 0)
                if wrote == 0:
                    raise Exception("Failed to write ANY bytes to %s" % process)
                index += wrote
            process.write_array(0, flag_eof, [], 0)

        # read the process output and wait for
        stdout = []
        stderr = []
        while process.status == library.ProcessStatus.started:
            read_out(process, flags, stdout, stderr)
            time.sleep(0.2)
        # make sure we have read the remainder of the out
        read_out(process, flags, stdout, stderr)

        return process, b"".join(stdout), b"".join(stderr)

    def makedirs(self, path, mode=0x777):
        "Super-mkdir: create a leaf directory and all intermediate ones."
        self.directory_create(path, mode, [library.DirectoryCreateFlag.parents])

    # Simplify calling directory_remove_recursive.  Set default flags to
    # content_and_dir if they have not yet been set.
    def directory_remove_recursive(self, path, flags=None):
        if flags is None:
            flags = [library.DirectoryRemoveRecFlag.content_and_dir]
        super(IGuestSession, self).directory_remove_recursive(path, flags)
    directory_remove_recursive.__doc__ = library.IGuestSession.directory_remove_recursive.__doc__

    # Simplify file_exists with default follow_symlink == False
    def file_exists(self, path, follow_symlinks=True):
        return super(IGuestSession, self).file_exists(path, follow_symlinks)
    file_exists.__doc__ = library.IGuestSession.file_exists.__doc__

    # Simplify symlink_exists with default follow_symlink == False
    def symlink_exists(self, path, follow_symlinks=True):
        return super(IGuestSession, self).symlink_exists(path)
    symlink_exists.__doc__ = library.IGuestSession.symlink_exists.__doc__

    # Simplify directory_exists with default follow_symlink == False
    def directory_exists(self, path, follow_symlinks=True):
        return super(IGuestSession, self).directory_exists(path, follow_symlinks)
    directory_exists.__doc__ = library.IGuestSession.directory_exists.__doc__

    def path_exists(self, path, follow_symlinks=True):
        "test if path exists"
        return (self.file_exists(path, follow_symlinks) or
                self.symlink_exists(path, follow_symlinks) or
                self.directory_exists(path, follow_symlinks))

    # TODO: re-introduce copy_to and copy_from. Inspect the source to figure out if its a
    # directory or file...  Use new apis as required.
    """
    # Simplify copy to.  Expand host path to abspath.
    def copy_to(self, host_path, guest_path, flags=[]):
        if not os.path.exists(host_path):
            raise OSError("Failed to find %s on host" % host_path)
        copy_to = super(IGuestSession, self).copy_to
        p = copy_to(os.path.abspath(host_path), guest_path, flags)
        p.wait_for_completion()
        return p
    copy_to.__doc__ = library.IGuestSession.copy_to.__doc__

    # Simplify copy from.  Expand host path to abspath.
    def copy_from(self, guest_path, host_path, flags=[]):
        # Dodgy exists check...
        for x in range(10):
            try:
                self.file_exists(guest_path)
                break
            except:
                time.sleep(0.1)
        else:
            raise OSError("Failed to find %s on guest" % guest_path)
        copy_from = super(IGuestSession, self).copy_from
        p = copy_from(guest_path, os.path.abspath(host_path), flags)
        p.wait_for_completion()
        return p
    copy_from.__doc__ = library.IGuestSession.copy_from.__doc__
    """
