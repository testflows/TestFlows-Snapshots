import os
import uuid
import inspect

from testflows.core import *

from testflows.snapshots import snapshot
from testflows.snapshots.errors import SnapshotError
from testflows.snapshots.snapshots import get_snapshot_filename


@TestStep(Given)
def get_unique_id(self, frame=None, path=None):
    """Generate unique snapshot id and delete snapshot file for that id
    at the end of the test."""

    if frame is None:
        frame = inspect.currentframe()

    try:
        id = uuid.uuid4().hex
        yield id

    finally:
        filename = get_snapshot_filename(frame=frame, path=path, id=id)
        with By("deleting file for the snapshot id", description=f"{filename}"):
            try:
                os.remove(filename)
            except FileNotFoundError:
                pass


@TestStep(When)
def check(self, expect, **kwargs):
    """Call snapshot with the provided arguments and check the expected result."""
    exc, result = None, None

    try:
        result = snapshot(**kwargs)
    except SnapshotError as e:
        exc = e

    expect(exc=exc, result=result)
