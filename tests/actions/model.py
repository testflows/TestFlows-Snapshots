from testflows.core import current, debug
from testflows.snapshots import snapshot
from testflows.snapshots.snapshots import get_snapshot_filename

import actions.expect


class State:
    """Snapshot state."""

    __slots__ = ("value", "name", "filename", "encoder", "mode", "version")

    def __init__(self, **kwargs):
        self.value = kwargs.pop("value")
        self.name = kwargs.pop("name", "snapshot")
        self.encoder = kwargs.pop("encoder", "repr")
        self.mode = kwargs.pop("mode", snapshot.CHECK | snapshot.UPDATE)
        self.version = kwargs.pop("version", snapshot.VERSION_V1)
        self.filename = get_snapshot_filename(
            frame=kwargs.pop("frame"),
            path=kwargs.pop("path", None),
            id=kwargs.pop("id", None),
        )

    def __str__(self):
        mode = []
        if self.mode & snapshot.CHECK:
            mode.append("CHECK")
        if self.mode & snapshot.UPDATE:
            mode.append("UPDATE")
        if self.mode & snapshot.REWRITE:
            mode.append("REWRITE")
        mode = "|".join(mode)

        return f"filename={self.filename} name={self.name} value={self.value} mode={mode} encoder={self.encoder} version={self.version}"


class Model:
    """Snapshots behavior model."""

    def __init__(self) -> None:
        pass

    def expect_ok(self, behavior: list[State]):
        """Expect that found a match or added a new value to the snapshot."""
        return actions.expect.expect_ok

    def expect_value_error(self, behavior: list[State]):
        """Expect value error exception."""
        current = behavior[-1]
        try:
            current.encoder(current.value)
        except Exception:
            return actions.expect.expect_value_error

    def expect_file_not_found_error(self, behavior: list[State]):
        """Expect file not found error exception."""
        # not implemented
        return

    def expect_snapshot_error(self, behavior: list[State]):
        """Expect snapshot error."""
        current = behavior[-1]

        if not current.mode & snapshot.CHECK:
            return

        stored_value = None

        for state in behavior[:-1]:
            if state.filename == current.filename and state.name == current.name:
                if stored_value is not None:
                    if state.mode & snapshot.CHECK:
                        continue
                    elif state.mode & snapshot.UPDATE:
                        stored_value = state.value
                else:
                    if state.mode & snapshot.UPDATE:
                        stored_value = state.value

        debug(f"stored_value={stored_value} current.value={current.value}")
        if stored_value is not None and stored_value != current.value:
            return actions.expect.expect_snapshot_error

    def expect_snapshot_not_found_error(self, behavior: list[State]):
        """Expect snapshot not found error."""
        current = behavior[-1]

        if current.mode & snapshot.UPDATE:
            return

        stored_value = None

        for state in behavior[:-1]:
            if state.filename == current.filename and state.name == current.name:
                if stored_value is not None:
                    if state.mode & snapshot.CHECK:
                        continue
                    elif state.mode & snapshot.UPDATE:
                        stored_value = state.value
                else:
                    if state.mode & snapshot.UPDATE:
                        stored_value = state.value

        if stored_value is None:
            return actions.expect.expect_snapshot_not_found_error
        else:
            if not (current.mode & snapshot.CHECK) and not (
                current.mode & snapshot.UPDATE
            ):
                if current.value != stored_value:
                    return actions.expect.expect_snapshot_not_found_error

    def expect(self, exc, result=None):
        """Get expected action for the given the behavior."""
        behavior = current().context.behavior

        for i, state in enumerate(behavior):
            debug(f"state #{i}: {state}")

        return (
            self.expect_value_error(behavior)
            or self.expect_file_not_found_error(behavior)
            or self.expect_snapshot_error(behavior)
            or self.expect_snapshot_not_found_error(behavior)
            or self.expect_ok(behavior)
        )(exc=exc, result=result)
