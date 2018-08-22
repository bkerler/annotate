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


```
MIT License

Copyright (c) 2018 B. Kerler

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
