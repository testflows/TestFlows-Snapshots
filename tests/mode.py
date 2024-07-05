from testflows.core import *
from testflows.snapshots import snapshot

from requirements import *

import actions.snapshot
import actions.python
import actions.values
import actions.model


@TestSketch
def check_combinations(self, number_of_actions):
    """Check combinations."""
    frame = actions.python.currentframe()

    values = ["hello", "hello2"]
    encoders = [repr]
    modes = actions.values.modes()
    names = ["name1", "name2"]

    self.context.behavior = []
    model = actions.model.Model()

    with Given("unique snapshot file"):
        id = define("id", actions.snapshot.get_unique_id(frame=frame))

    for i in range(number_of_actions):
        actions.snapshot.check(
            expect=model.expect,
            value=either(*values, i=f"value-{i}"),
            encoder=either(*encoders, i=f"encoder-{i}"),
            mode=either(*modes, i=f"mode-{i}"),
            name=either(*names, i=f"name-{i}"),
            frame=frame,
            id=id,
            path=None,
            version=snapshot.VERSION_V1,
        )


@TestFeature
@Name("mode")
def feature(self):
    """Check all spanshot modes."""

    Scenario(test=check_combinations)(number_of_actions=3)
