import ctypes as c
import functools
import shutil
import typing
from typing import Optional, Union, Callable
from pathlib import Path

from .loader import LibLoader


_F = typing.TypeVar('_F', bound=Callable[..., typing.Any])


def _cleanup_on_fail(func: _F) -> _F:

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except:
            self._cleanup()
            raise

    return wrapper


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
        self._handle = None
        self._init()

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

    @_cleanup_on_fail
    def _start_process(self, cmdline: str, working_directory: Optional[str] = None):
        self._handle = c.c_void_p(None)
        self._library.StartProcess(
            cmdline,
            working_directory,
            c.byref(self._handle),
        )

    @property
    @_cleanup_on_fail
    def is_alive(self) -> bool:
        if self._handle is None:
            return False

        return self._library.IsAlive(self._handle)

    @_cleanup_on_fail
    def kill(self):
        if self._handle is None:
            return

        self._library.Kill(self._handle)

    def _cleanup(self):
        if self._handle is not None:
            self._library.Cleanup(self._handle)
            self._handle = None

    def __del__(self):
        self._cleanup()
