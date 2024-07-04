from testflows.core import *

from testflows.snapshots.errors import SnapshotError, SnapshotNotFoundError


@TestStep(Then)
def expect_value_error(self, exc, result):
    """Check that ValueError was raised."""
    assert isinstance(
        exc, ValueError
    ), f"expected ValueError, got {exc} and {result} result"


@TestStep(Then)
def expect_file_not_found_error(self, exc, result=None):
    """Check that FileNotFoundError was raised."""
    assert isinstance(
        exc, FileNotFoundError
    ), f"expected FileNotFoundError, got {exc} and {result} result"


@TestStep(Then)
def expect_snapshot_error(self, exc, result=None):
    """Check that result is SnapshotError."""
    assert exc is None, f"unexpected error {exc}"
    assert isinstance(
        result, SnapshotError
    ), f"expected SnapshotError, got {result} result"


@TestStep(Then)
def expect_snapshot_not_found_error(self, exc, result=None):
    """Check that result is SnapshotNotFoundError."""
    assert exc is None, f"unexpected error {exc}"
    assert isinstance(
        result, SnapshotNotFoundError
    ), f"expected SnapshotNotFoundError, got {result} result"


@TestStep(Then)
def expect_ok(self, exc, result):
    """Check that no exception was reaised and the result is True."""
    assert exc is None, f"unexpected error {exc}"
    assert result is True, f"unexpected result {result}"
