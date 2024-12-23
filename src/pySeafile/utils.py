
import os
import inspect
import datetime


def path_to_local_file(filename, frame_offset=0):
    """Get the full path to a file in the same folder as the
    executing script, optionally going further up the stack
    to find the "caller" module."""

    # get the caller's frame
    frame = inspect.stack()[1 + frame_offset]
    module = inspect.getmodule(frame[0])
    path = os.path.abspath(os.path.dirname(module.__file__))
    return os.path.join(path, filename)


def to_datetime(date_string):
    """Case a string to a datetime object."""
    return datetime.datetime.strptime(
        date_string, '%Y-%m-%dT%H:%M:%S%z')
