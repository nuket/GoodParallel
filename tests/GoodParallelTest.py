# GoodParallel
# Copyright (c) 2020 Max Vilimpoc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from GoodParallel import console_color, no_console_color, simple_process_pool

# Nice.
# https://bugs.python.org/issue30075

def enable_vt100():
    import os
    import msvcrt
    import ctypes

    from ctypes import wintypes

    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

    ERROR_INVALID_PARAMETER = 0x0057
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

    def _check_bool(result, func, args):
        if not result:
            raise ctypes.WinError(ctypes.get_last_error())
        return args

    LPDWORD = ctypes.POINTER(wintypes.DWORD)
    kernel32.GetConsoleMode.errcheck = _check_bool
    kernel32.GetConsoleMode.argtypes = (wintypes.HANDLE, LPDWORD)
    kernel32.SetConsoleMode.errcheck = _check_bool
    kernel32.SetConsoleMode.argtypes = (wintypes.HANDLE, wintypes.DWORD)

    def set_conout_mode(new_mode, mask=0xffffffff):
        # don't assume StandardOutput is a console.
        # open CONOUT$ instead
        fdout = os.open('CONOUT$', os.O_RDWR)
        try:
            hout = msvcrt.get_osfhandle(fdout)
            old_mode = wintypes.DWORD()
            kernel32.GetConsoleMode(hout, ctypes.byref(old_mode))
            mode = (new_mode & mask) | (old_mode.value & ~mask)
            kernel32.SetConsoleMode(hout, mode)
            return old_mode.value
        finally:
            os.close(fdout)

    def enable_vt_mode():
        mode = mask = ENABLE_VIRTUAL_TERMINAL_PROCESSING
        try:
            return set_conout_mode(mode, mask)
        except WindowsError as e:
            if e.winerror == ERROR_INVALID_PARAMETER:
                raise NotImplementedError
            raise

    enable_vt_mode()

# Unit test the process pool.

def test():
    import sys

    # Assume that console has color unless it is the pre-Windows 10 Command Prompt.
    theme_colors = console_color

    if sys.platform == 'win32':
        try:
            enable_vt100()
        except:
            # If no VT100 is available, then strip off the color codes.
            theme_colors = no_console_color

        test_command = 'timeout /t {0}'
    else:
        test_command = 'sleep {0}'

    # Run 16 instances of command.
    commands = [test_command.format(i) for i in range(1, 5)] * 4
    simple_process_pool(commands, theme=theme_colors)

# Try it out.
if __name__ == '__main__':
    test()
