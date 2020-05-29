# GoodParallel: FfmpegParallelTest
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
    import os
    import sys

    # Assume that console has color unless it is the pre-Windows 10 Command Prompt.
    theme_colors = console_color

    if sys.platform == 'win32':
        try:
            enable_vt100()
        except:
            # If no VT100 is available, then strip off the color codes.
            theme_colors = no_console_color

    test_command = 'ffmpeg -y -i {0} -an -filter_complex "[0:v] palettegen [palette]; [0:v][palette] paletteuse" {1}'

    commands = [test_command.format(f, os.path.splitext(f)[0] + '.gif') for f in ['Cli-Ubuntu.mkv', 'Cli-Windows-Legacy.mkv', 'Cli-Windows-Terminal.mkv', 'Transcoding-Single-Core.mkv', 'Transcoding-Multicore.mkv']]
    results = simple_process_pool(commands, theme=theme_colors)

# Try it out.
if __name__ == '__main__':
    test()
