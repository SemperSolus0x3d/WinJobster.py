import ctypes as c
import functools
import typing
from pathlib import Path

from .WinJobsterLoader import WinJobsterLoader


_F = typing.TypeVar('_F', bound=typing.Callable[..., typing.Any])


def _cleanup_on_fail(func: _F) -> _F:

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except:
            self._cleanup()
            raise

    return wrapper


class Process:
    _library = None

    @classmethod
    def _init(cls):
        if cls._library is None:
            cls._library = WinJobsterLoader().load()

    def __init__(self):
        self._handle = None
        self._init()

    def start_in_base_dir(self, cmdline: typing.Union[str, Path]):
        cmdline = Path(cmdline)
        self.start(cmdline, cmdline.parent)

    @_cleanup_on_fail
    def start(self, cmdline: typing.Union[str, Path], working_directory: typing.Union[str, Path, None] = None):
        cmdline = str(cmdline)
        if working_directory is not None:
            working_directory = str(working_directory)
        self._handle = c.c_void_p(None)
        self._library.StartProcess(
            cmdline,
            working_directory,
            c.byref(self._handle))

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
