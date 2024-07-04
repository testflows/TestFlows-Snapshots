import os

from testflows.core import *


@TestStep(When)
def delete_file(self, path):
    """Try to delete file."""
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
