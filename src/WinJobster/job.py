import ctypes as c
import functools
import shutil
import typing
from typing import Optional, Union, Callable
from pathlib import Path

from .loader import LibLoader


class Job:
    _library = None

    class AppLocal:
        pass

    APP_LOCAL = AppLocal()

    @classmethod
    def _init(cls):
        if cls._library is None:
            cls._library = LibLoader().load()

    def __init__(self):
        self._init()
        self._handle = self._library.CreateJob()

    def start_process(
        self,
        path: typing.Union[str, Path],
        call_params: str = "",
        working_directory: typing.Union[str, Path, AppLocal, None] = APP_LOCAL,
    ):
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

        self._start_process(cmdline, working_directory)


    def _start_process(self, cmdline: str, working_directory: Optional[str] = None):
        self._library.StartProcess(
            cmdline,
            working_directory,
            self._handle,
        )

    @property
    def is_alive(self) -> bool:
        if self._handle is None:
            return False

        return self._library.IsAlive(self._handle)


    def terminate(self, gracefully=True):
        if self._handle is None:
            return

        if gracefully:
            self._library.Terminate(self._handle)
        else:
            self._library.Kill(self._handle)


    @property
    def process_ids(self) -> set[int]:
        if self._handle is None:
            return set()
        
        ids = c.POINTER(c.c_uint64)()
        size = c.c_size_t

        self._library.GetProcessIds(self._handle, c.byref(ids), c.byref(size))

        result = { int(ids[i]) for i in range(size) }

        self._library.FreeMemory(ids)

        return result


    def _cleanup(self):
        if self._handle is not None:
            self._library.DestroyJob(self._handle)
            self._handle = None

    def __del__(self):
        self._cleanup()
