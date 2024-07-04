import json
from testflows.core import *
from testflows.asserts import error, raises
from testflows.snapshots import snapshot
from requirements import *

import actions.python
import actions.snapshot

currentframe = actions.python.currentframe


@TestScenario
def is_first_argument(self):
    """Check value is the first argument."""

    value = "value to be stored and checked"

    with When("value is passed by position as the first argument"):
        r = snapshot(value, id=None, mode=snapshot.CHECK)

    with Then("the snapshot error actual value contains it"):
        assert f'actual_value="""\n    \'{value}\'\n"""' in str(r), error()


@TestScenario
def stored_and_compared(self):
    """Check value is being stored and being compared against"""

    value = "value to be stored and checked"

    with Given("snapshot id"):
        id = actions.snapshot.get_unique_id(frame=currentframe())

    with When("value is stored using the UPDATE mode"):
        assert snapshot(value, id=id, mode=snapshot.UPDATE), error()

    with Then("the snapshot matches the stored value using the CHECK mode"):
        assert snapshot(value, id=id, mode=snapshot.CHECK), error()


@TestScenario
def supported_types(self):
    """Check value can be of any type supported by the encoder"""

    values = [1, 1.0, "string", [1, 2, 3], {"key": "value"}, (1, 2), True, False, None]

    with Given("snapshot id"):
        id = actions.snapshot.get_unique_id(frame=currentframe())

    with Then("supported encoder types can be stored and checked"):
        for value in values:
            assert snapshot(
                value, id=id, encoder=json.dumps, mode=snapshot.UPDATE
            ), error()
            assert snapshot(
                value, id=id, encoder=json.dumps, mode=snapshot.CHECK
            ), error()


@TestScenario
def unsupported_type(self):
    """Check ValueError is raised if encoder fails to encode the value."""

    with Given("snapshot id"):
        id = actions.snapshot.get_unique_id(frame=currentframe())

    with Then("unsupported encoder type raises ValueError"):
        with raises(ValueError):
            try:
                assert snapshot(
                    {1, 2, 3}, id=id, encoder=json.dumps, mode=snapshot.CHECK
                ), error()
            except ValueError as exc:
                assert "failed to encode: {1, 2, 3}" in str(exc), error()
                raise


@TestFeature
@Requirements(RQ_TestFlows_Snapshots_Function_Snapshot_Value("1.0"))
@Name("value")
def feature(self):
    """Check snapshot value."""

    for scenario in loads(current_module(), Scenario):
        scenario()
