#!/usr/bin/env python
"""A loading spinner that you can use as a context manager or a decorator.

This module has the :class:Loader class.
The spinner runs on a separate thread and prints one character at a time
to the standard output. The spinner only runs when the standard output
is a TTY.
"""

import sys
from contextlib import ContextDecorator
from itertools import cycle
from threading import Thread
from time import sleep


class Loader(ContextDecorator):
    """A loading spinner that runs on a background thread.

    Use this class as a context manager or as a function decorator.
    The spinner prints characters in a loop while the work runs.
    It stops when you close the context or when the function ends.

    Attributes:
        CHARS: The list of characters that the spinner uses.
        desc: The text that the spinner prints next to the character.
        end: The text that the spinner prints when it stops.
            When the value is empty, the spinner clears the line.
        timeout: The time in seconds between two characters.
    """

    CHARS = ["⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self, desc="Loading...", end="", timeout=0.1):
        """Set the text, the end text, and the speed of the spinner.

        Args:
            desc: The text to print next to the character.
                The default value is "Loading...".
            end: The text to print when the spinner stops.
                When the value is empty, the spinner clears the line.
                The default value is "".
            timeout: The time in seconds between two characters.
                The default value is 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self.done = False
        self._thread = None

    def start(self):
        """Start the spinner on a new thread.

        Returns:
            The :class:Loader object itself, so you can use the
            return value in a chain.
        """
        self.done = False
        self._thread = Thread(target=self._animate, daemon=True)
        self._thread.start()
        return self

    def _animate(self):
        """Print the spinner characters in a loop.

        The function does nothing when the standard output is not a TTY.
        It stops the loop when self.done is True.
        """
        if not sys.stdout.isatty():
            return
        for c in cycle(self.CHARS):
            if self.done:
                break
            sys.stdout.write(f"\r{c} {self.desc}")
            sys.stdout.flush()
            sleep(self.timeout)

    def stop(self):
        """Stop the spinner and then clean up the line.

        The function waits for the spinner thread to end.
        When the standard output is not a TTY and self.end is set,
        it prints the end text only.
        When the standard output is a TTY, it clears the spinner line
        and then prints the end text when it is set.
        """
        self.done = True
        if self._thread is not None:
            self._thread.join()

        if not sys.stdout.isatty():
            if self.end:
                print(self.end)
            return

        if not self.end:
            sys.stdout.write("\r\033[K")
        else:
            sys.stdout.write(f"\r\033[K{self.end}\n")
        sys.stdout.flush()

    def __enter__(self):
        """Enter the context and then start the spinner.

        Returns:
            The :class:Loader object itself.
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        """Exit the context and then stop the spinner.

        Args:
            exc_type: The exception type, when an exception occurred.
            exc_value: The exception value, when an exception occurred.
            tb: The traceback, when an exception occurred.
        """
        self.stop()
