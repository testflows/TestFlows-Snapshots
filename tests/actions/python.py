import inspect


def currentframe():
    """Return current caller's frame."""
    return inspect.currentframe().f_back
