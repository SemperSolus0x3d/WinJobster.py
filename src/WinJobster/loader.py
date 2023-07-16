import platform
import ctypes as c
import sys
from pathlib import Path

if sys.version_info < (3, 10, 0):
    import pkg_resources

    def files(path: str):
        return Path(pkg_resources.resource_filename(__name__, "..")).joinpath(path)
else:
    from importlib.resources import files


from .exceptions import CallFailedException, ErrorCode


class LibLoader:
    _common_lib = None

    @property
    def filename(self):
        name = "WinJobster-{}.dll"
        if platform.architecture()[0] == '64bit':
            return name.format("x64")
        return name.format("x86")

    @property
    def file_path(self):
        return files("libs").joinpath(self.filename)

    def load(self, new_instance=False) -> c.WinDLL:
        if self.__class__._common_lib is not None and not new_instance:
            return self.__class__._common_lib

        lib = c.WinDLL(str(self.file_path))

        lib.StartProcess.restype = c.c_uint32
        lib.StartProcess.errcheck = LibLoader._errcheck
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

        self.__class__._common_lib = lib
        return lib

    @staticmethod
    def _errcheck(result, func, arguments):
        if result != ErrorCode.Success:
            raise CallFailedException(result)
