import sys
from testflows.core import *

from testflows.snapshots import snapshot
from testflows.combinatorics import product

from requirements import *

import actions.snapshot
import actions.python
import actions.values
import actions.model


@TestSketch
def check_combinations(self, number_of_actions):
    """Check a sequence of some combination of snapshot check actions."""
    frame = actions.python.currentframe()

    values = ["hello", "hello2"]
    encoders = [repr]
    modes = actions.values.modes()
    names = ["name1", "name2"]

    self.context.behavior = []
    model = actions.model.Model()

    with Given("unique snapshot file"):
        id = define("id", actions.snapshot.get_unique_id(frame=frame))

    with Then("check sequence of snapshot calls"):
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


@TestCheck
def check_actions(self, combination_of_actions):
    """Check a sequence of some combination of snapshot check actions."""
    append_path(sys.path, ".")
    import actions.snapshot
    import actions.python
    import actions.values
    import actions.model

    frame = actions.python.currentframe()
    model = actions.model.Model()
    self.context.behavior = []

    with Given("unique snapshot file"):
        id = define("id", actions.snapshot.get_unique_id(frame=frame))

    with Then("check sequence of snapshot calls"):
        for i, action in enumerate(combination_of_actions):
            value, encoder, mode, name = action
            actions.snapshot.check(
                expect=model.expect,
                value=value,
                encoder=encoder,
                mode=mode,
                name=name,
                frame=frame,
                id=id,
                path=None,
                version=snapshot.VERSION_V1,
            )


@TestScenario
@Name("chunk")
def check_chunk_of_actions(self, chunk):
    for combination_of_actions in chunk:
        Combination(f"{combination_of_actions}", test=check_actions)(
            combination_of_actions=combination_of_actions
        )


@TestScenario
def check_combinations_v2(self, number_of_actions):
    """Check combinations."""

    values = ["hello", "hello2"]
    encoders = [repr]
    modes = actions.values.modes()
    names = ["name1", "name2"]

    with Given("all possible ways to call snapshot"):
        ways = product(values, encoders, modes, names)

    with Pool(4) as executor:
        for i, chunk in enumerate(
            chunks(product(ways, repeat=number_of_actions), 6000)
        ):
            Scenario(
                f"chunk {i}",
                test=check_chunk_of_actions,
                parallel=True,
                executor=executor,
            )(chunk=chunk)
        join()


@TestFeature
@Name("mode")
def feature(self):
    """Check all spanshot modes."""

    Scenario(test=check_combinations_v2)(number_of_actions=3)
