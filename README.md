## BinaryNinja universal annotate plugin

### Why
I know there are already Annotator and WinAPI-Annotator .. BUT:

* This one combines both plugins for windows and linux, sorts out some issues
* And adds reg based approach using llil and mlil to support other platforms, such as ARM
* Also has a database for libc and has a tool to convert libc man to database :)
* Has both python2 and python3 support

Big thanks to @carstein and @levyjm for setting the foundation.

### Supported modules
* kernel32.dll
* user32.dll
* ole32.dll
* advapi32.dll
* libc
* Some openssl libs
* Any json in generic folder

#### Any new supported module and/or bug fix and/or feature improvement is welcome !

## ToDo
* MIPS support
* Other arch support such as MACH

### Disclaimer
* This plugin has been tested for Windows-32/64, Linux-32/64, and Android ARM Libraries


