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
job = WinJobster.Job()
print(job.is_alive)  # False, no alive processes found
job.start_process(cmdline)
print(job.is_alive)  # True, 1 alive process found
job.terminate()  # Will close original app and everything which was started by it
```

> `job.start_process`' first argument can be path, 
> or any string interpreted as console input (Windows will expand %PATH% values for you)
