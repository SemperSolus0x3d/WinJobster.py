import platform
import ctypes as c
from importlib.resources import files, as_file

from .WinJobsterCallFailedException import WinJobsterCallFailedException, ErrorCode


class WinJobsterLoader:
    @property
    def filename(self):
        name = "WinJobster-{}.dll"
        if platform.architecture()[0] == '64bit':
            return name.format("x64")
        return name.format("x86")

    @property
    def file_path(self):
        return files("libs").joinpath(self.filename)

    def load(self) -> c.WinDLL:
        lib = c.WinDLL(str(self.file_path))

        lib.StartProcess.restype = c.c_uint32
        lib.StartProcess.errcheck = WinJobsterLoader._errcheck
        lib.StartProcess.argtypes = [
            c.c_wchar_p,
            c.c_wchar_p,
            c.POINTER(c.c_void_p)
        ]

        lib.IsAlive.restype = c.c_bool
        lib.IsAlive.argtypes = [c.c_void_p]

        lib.Kill.restype = None
        lib.Kill.argtypes = [c.c_void_p]

        lib.Cleanup.restype = None
        lib.Cleanup.argtypes = [c.c_void_p]

        return lib

    @staticmethod
    def _errcheck(result, func, arguments):
        if result != ErrorCode.Success:
            raise WinJobsterCallFailedException(result)
