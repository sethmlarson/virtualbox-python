from __future__ import print_function
import sys


def show_progress(progress, ofile=sys.stderr):
    """Print the current progress out to file"""
    try:
        while not progress.completed:
            print(progress, file=ofile)
            progress.wait_for_completion(1000)
    except KeyboardInterrupt:
        if progress.cancelable:
            progress.cancel()

    print(progress, file=ofile)
    print("Progress state: %s" % progress.result_code, file=ofile)
    if progress.error_info:
        print(progress.error_info.text, file=ofile)




