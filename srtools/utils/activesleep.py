"""Active sleep counter."""
import sys
import time

def activesleep(total, callback=None, step=30, extra=None):
    """
    Sleep for the given amount of time.
    :param total: Time to wait.
    :type total: int
    :param callback: Callback to call. Returns the amount of seconds left.
    :type callback: function
    """
    current_step = step
    if total > 0:
        index = total
        while index > 0:
            index -= 1

            print(f"Sleeping for {index}...\r")
            sys.stdout.flush()
            time.sleep(1)

            current_step -= 1
            if current_step < 0:
                if callback is not None:
                    index = callback(index, total, extra)

                current_step = step
