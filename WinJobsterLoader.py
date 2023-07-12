import platform
import ctypes as c
from WinJobsterCallFailedException import WinJobsterCallFailedException

class WinJobsterLoader:
    def load(self) -> c.WinDLL:
        if platform.architecture()[0] == '64bit':
            lib = c.WinDLL('./libs/WinJobster-x64.dll')
        else:
            lib = c.WinDLL('./libs/WinJobster-x86.dll')

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
        if result != 0:
            raise WinJobsterCallFailedException(result)
