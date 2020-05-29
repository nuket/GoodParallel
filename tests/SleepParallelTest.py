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
from support import enable_vt100

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
