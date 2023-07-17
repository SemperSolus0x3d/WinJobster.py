import ctypes as c
import platform
import sys
from pathlib import Path

if sys.version_info < (3, 10, 0):
    import pkg_resources


    def files(path: str):
        return Path(pkg_resources.resource_filename(__name__, "..")).joinpath(path)
else:
    from importlib.resources import files

from .exceptions import CallFailedException, ErrorCode


def _errcheck(result, func, arguments) -> None:
    if result != ErrorCode.Success:
        raise CallFailedException(result)


c_error_code = c.c_uint32
c_uint64_p = c.POINTER(c.c_uint64)
c_uint64_pp = c.POINTER(c_uint64_p)
c_size_t_p = c.POINTER(c.c_size_t)

# @formatter:off
_SIGNATURES = [
    # Name             Return type    Error check  [Args...]
    ('CreateJob',      c.c_void_p,    None,        []),
    ('StartProcess',   c_error_code,  _errcheck,   [c.c_void_p, c.c_wchar_p, c.c_wchar_p, c.c_uint32]),
    ('IsAlive',        c.c_bool,      None,        [c.c_void_p]),
    ('Kill',           None,          None,        [c.c_void_p]),
    ('Terminate',      c_error_code,  _errcheck,   [c.c_void_p, c.c_uint32]),
    ('DestroyJob',     None,          None,        [c.c_void_p]),
    ('FreeMemory',     None,          None,        [c.c_void_p]),
    ('GetProcessIds',  c_error_code,  _errcheck,   [c.c_void_p, c_uint64_pp, c_size_t_p]),
]
# @formatter:on


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

        for name, returnType, errorCheck, args in _SIGNATURES:
            func = getattr(lib, name)

            func.restype = returnType
            func.argtypes = args

            if errorCheck is not None:
                func.errcheck = errorCheck

        self.__class__._common_lib = lib
        return lib
