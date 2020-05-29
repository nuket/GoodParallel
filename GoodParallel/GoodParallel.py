# GoodParallel: A Simple Native-Executable Process Pool
#
# A super easy way to run native command lines in parallel,
# without needing to wrap them up in Python first.
#
# All you have to do is provide the list of command strings you want
# executed, and it will keep as many cores busy as it can.
# 
# For example, using GraphicsMagick to convert a bunch of image files:
#
# gm convert -size 1280x! input/image-1.png -resize 1280x! -sharpen 1.0 +profile "*" -quality 100 output/image-1-1280.png
# gm convert -size 1280x! input/image-2.png -resize 1280x! -sharpen 1.0 +profile "*" -quality 100 output/image-2-1280.png
# gm convert -size 1280x! input/image-3.png -resize 1280x! -sharpen 1.0 +profile "*" -quality 100 output/image-3-1280.png
# gm convert -size 1280x! input/image-4.png -resize 1280x! -sharpen 1.0 +profile "*" -quality 100 output/image-4-1280.png
# gm convert -size 1280x! input/image-5.png -resize 1280x! -sharpen 1.0 +profile "*" -quality 100 output/image-5-1280.png
# gm convert -size 1280x! input/image-6.png -resize 1280x! -sharpen 1.0 +profile "*" -quality 100 output/image-6-1280.png
# gm convert -size 1280x! input/image-7.png -resize 1280x! -sharpen 1.0 +profile "*" -quality 100 output/image-7-1280.png
# gm convert -size 1280x! input/image-8.png -resize 1280x! -sharpen 1.0 +profile "*" -quality 100 output/image-8-1280.png
# 
# is as easy as:
#
# commands = [ 'gm convert -size 1280x! input/image-{}.png -resize 1280x! -sharpen 1.0 +profile "*" -quality 100 output/image-{}-1280.png'.format(i) for i in range(1, 9) ]
# simple_process_pool(commands)
#
# If you're on a multicore computer, you'll see your CPU go to 100% use
# as the work is spread out! Excellent!

import subprocess
import time

from multiprocessing import cpu_count

class console_color:
    HEADER   = '\033[94m'
    STARTING = '\033[92m'
    FINISHED = '\033[93m'
    END      = '\033[0m'

class no_console_color:
    HEADER   = ''
    STARTING = ''
    FINISHED = ''
    END      = ''

def simple_process_pool(commands_to_run, max_process_count=cpu_count(), time_between_checks=0.05, theme=console_color):
    """A simple way to run multiple commands in parallel using the subprocess
    module only.
    
    Easier to run command strings directly and no need to spawn extra Python
    interpreters, as with the multiprocessing module. 
    
    Also, no need to conform to this multiprocessing requirement. What?
    "Functionality within this package requires that the __main__ module be importable by the children."

    :param commands_to_run:     List of command strings to run.
    :param max_process_count:   The number of commands to run in parallel.
    :param time_between_checks: When process pool is fully busy running commands, sleep between 
                                checks for pool slots freeing up. Otherwise it will spin too much.
    :param theme:               A list of colors to use to highlight different output rows.
    """
    print(theme.HEADER + "GoodParallel: Simple Process Pool " + theme.END + "({0} cores usable)".format(max_process_count))

    # Mutable copy of commands.
    commands  = list(commands_to_run)
    processes = []
    finished  = []

    while len(commands) or len(processes):
        # Check any existing processes and remove completed.
        for p in processes:
            if p.poll() is not None:
                print(theme.FINISHED + "Finished: (pid: {0}) (returned: {1})".format(p.pid, p.returncode) + theme.END) # ' '.join(p.args or ''), 
                finished.append(p)
                processes.remove(p)
                break # continue the while loop (restart the for .. in loop)

        # Check for space in the pool and start new processes.
        if len(commands) and len(processes) < max_process_count:
            command = commands.pop(0)
            processes.append(subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)) # .split(' ')
            print(theme.STARTING + "Starting: (pid: {0}) '{1}', {2} commands left".format(processes[-1].pid, command, len(commands)) + theme.FINISHED)
        else:
            # Slow down the finish-check if all pool slots are in use.
            time.sleep(time_between_checks)

    # Pass back the Popen objects, in case the caller wants to check them.
    return finished
