# Package meta information

# Major, Minor, Patch, Extra (alpha/beta/rc1/rc2..)
__version_info__ = (2, 1, 0, None)  # None for stable release
__version__ = '.'.join(map(str, __version_info__[:-1]))
if __version_info__[-1] is not None:
    __version__ += '-' + __version_info__[-1]
