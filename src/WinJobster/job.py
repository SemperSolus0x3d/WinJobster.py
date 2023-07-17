import ctypes as c
import shutil
import typing
from pathlib import Path
from typing import Union

from .loader import LibLoader


class Job:
    _library = None

    class AppLocal:
        """Special value for express path local for new executable,
           not for current script"""
        pass

    APP_LOCAL = AppLocal()
    """
    Default value for working directory to handle local executable base dir as its working directory
    Don't put call_params inside of path string, when using this value!
    """

    TIMEOUT_INFINITY = 4294967295
    """
    Special value for :meth:`Job.start_process`. 
    Can be used when process awaiting must be infinite.
    """

    @classmethod
    def _init(cls):
        if cls._library is None:
            cls._library = LibLoader().load()

    def __init__(self):
        self._init()
        self._handle = self._library.CreateJob()

    def start_process(
        self,
        path: Union[str, Path],
        call_params: str = "",
        working_directory: Union[str, Path, AppLocal, None] = APP_LOCAL,
        timeout=100,
    ):
        """
        Method to start new process in job scope, can be called multiple times to start multiple processes
        :param path: Path to executable, %PATH% variables resolved automatically, e.g. cmd.exe
        :param call_params: Arguments for executable to be called with, this string will be transferred
            "as-is" without any escaping
        :param working_directory: Current Working Directory of process:
            "."/Path(".") = CWD of current script
            APP_LOCAL = parent dir of process path (this is default)
            Prefer using absolute path here
        :param timeout: Timeout in milliseconds for awaiting of process to become alive.
            Use :attr:`Job.TIMEOUT_INFINITY` or -1 for infinite await.
            Use 0 to not wait.
        """
        if isinstance(working_directory, Job.AppLocal):
            resolved_path = shutil.which(str(path))
            if resolved_path is None:
                resolved_path = path
            working_directory = Path(resolved_path).parent

        cmdline = str(path)
        if call_params:
            cmdline += " " + call_params

        if working_directory is not None:
            working_directory = str(working_directory)

        self._library.StartProcess(
            self._handle,
            cmdline,
            working_directory,
            timeout if timeout >= 0 else Job.TIMEOUT_INFINITY,
        )

    @property
    def is_alive(self) -> bool:
        """
        Method to check if job has any alive processes
        :return: True if any alive process found,
                 False if no processes, no job created or no alive processes found.
        """
        if self._handle is None:
            return False

        return self._library.IsAlive(self._handle)

    def terminate(self, timeout=1000):
        """
        Method for gracefully terminating all processes in job
        :param timeout: Timeout in milliseconds, how much time processes have to finish itself.
            When times out, force kill applied.
        """
        if self._handle is None:
            return

        if timeout > 0:
            self._library.Terminate(self._handle, timeout)
        else:
            self.kill()

    def kill(self):
        """
        Method for forcefully killing all processes in job with no wait.
        For most cases, please consider using :meth:`Job.terminate`, to let process exit properly.
        """
        self._library.Kill(self._handle)

    @property
    def process_ids(self) -> typing.Set[int]:
        """
        Provides ids of alive processes in job scope
        :return: Set of ids of processes in job
        """
        if self._handle is None:
            return set()

        ids = c.POINTER(c.c_uint64)()
        size = c.c_size_t()

        self._library.GetProcessIds(self._handle, c.byref(ids), c.byref(size))

        result = {int(ids[i]) for i in range(size.value)}

        self._library.FreeMemory(ids)
        return result

    def _cleanup(self):
        if self._handle is not None:
            self._library.DestroyJob(self._handle)
            self._handle = None

    def __del__(self):
        self._cleanup()
