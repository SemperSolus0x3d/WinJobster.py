# WinJobster
[![PyPI version shields.io](https://img.shields.io/pypi/v/WinJobster.svg)](https://pypi.org/project/WinJobster/)
[![GitHub license](https://img.shields.io/github/license/SemperSolus0x3d/WinJobster.py.svg)](https://github.com/SemperSolus0x3d/WinJobster.py/blob/master/LICENSE.md)
[![Python versions](https://img.shields.io/pypi/pyversions/WinJobster.svg)](https://pypi.org/project/WinJobster/)
---
WinJobster is a library, which can start processes in a Windows job, monitor their state (dead or alive) and kill them all at once, 
including their children, children of their children... you know where I'm going...

## Installation
```cmd
pip install WinJobster
```

## Usage
```py
import WinJobster


cmdline = "notepad.exe"  # Path to any app, which can also start other app
process = WinJobster.Process()
process.start(cmdline)
print(process.is_alive)  # True
process.kill()  # Will close original app and everything which was started by it
```

> By default, script root dir will be used as working directory for any started app,
> to avoid this use `start_in_base_dir` method or set working directory explicitly in `start`

> `process.start`'s first argument can be path, 
> or any string interpreted as console input (Windows will expand path for you) 