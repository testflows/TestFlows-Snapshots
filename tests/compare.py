from testflows.core import *
from testflows.snapshots import snapshot

import time

import actions.python
import actions.snapshot
import actions.expect

currentframe = actions.python.currentframe


@TestOutline
def check(self, value, ok_value, fail_value, compare):
    """Check calling snashot function with the specified comparison function."""

    self.context.behavior = []

    with Given("snapshot id"):
        id = actions.snapshot.get_unique_id(frame=currentframe())

    with When("store value"):
        actions.snapshot.check(
            id=id,
            name="value",
            value=value,
            mode=snapshot.UPDATE,
            compare=compare,
            expect=actions.expect.expect_ok,
        )

    with Then("check ok value"):
        actions.snapshot.check(
            id=id,
            name="value",
            value=ok_value,
            mode=snapshot.CHECK,
            compare=compare,
            expect=actions.expect.expect_ok,
        )

    with And("check fail value"):
        actions.snapshot.check(
            id=id,
            name="value",
            value=fail_value,
            mode=snapshot.CHECK,
            compare=compare,
            expect=actions.expect.expect_snapshot_error,
        )


@TestScenario
def compare_eq(self):
    """Check equal comparison."""
    check(value=1, ok_value=1, fail_value=2, compare=snapshot.COMPARE.eq)


@TestScenario
def compare_ne(self):
    """Check not equal comparison."""
    check(value=1, ok_value=2, fail_value=1, compare=snapshot.COMPARE.ne)


@TestScenario
def compare_lt(self):
    """Check less than comparison."""
    check(value=1, ok_value=2, fail_value=1, compare=snapshot.COMPARE.lt)


@TestScenario
def compare_gt(self):
    """Check greater than comparison."""
    check(value=2, ok_value=1, fail_value=3, compare=snapshot.COMPARE.gt)


@TestScenario
def compare_le(self):
    """Check less than or equal comparison."""
    with Check("equals"):
        check(value=2, ok_value=2, fail_value=1, compare=snapshot.COMPARE.le)

    with Check("less than"):
        check(value=2, ok_value=3, fail_value=1, compare=snapshot.COMPARE.le)


@TestScenario
def compare_ge(self):
    """Check greater than or equal comparison."""
    with Check("equals"):
        check(value=2, ok_value=2, fail_value=4, compare=snapshot.COMPARE.ge)

    with Check("greater than"):
        check(value=2, ok_value=1, fail_value=4, compare=snapshot.COMPARE.ge)


@TestScenario
def compare_contains(self):
    """Check contains comparison."""
    check(
        value="hello there",
        ok_value="hello",
        fail_value="foo",
        compare=snapshot.COMPARE.contains,
    )


@TestScenario
def compare_resub(self):
    """Check regex substitution comparison."""
    with Check("stripping"):
        check(
            value=f"hello {time.time()}",
            ok_value="hello 222.333",
            fail_value="hellok 222.333",
            compare=snapshot.COMPARE.resub(r"\d+(\.\d+)?"),
        )

    with Check("bringing to common form"):
        check(
            value=f"hello 555.333",
            ok_value="hello 222.333",
            fail_value="hello2 222.333",
            compare=snapshot.COMPARE.resub(r"\d+(\.\d+)?", sub="d"),
        )


@TestScenario
def compare_rematch(self):
    """Check regex match comparison."""
    check(
        value="hello there",
        ok_value="hello foo boo",
        fail_value="foo",
        compare=snapshot.COMPARE.rematch(r"hello.*"),
    )


@TestScenario
def compare_renotmatch(self):
    """Check regex not match comparison."""
    check(
        value="hell2o there",
        ok_value="hell2o foo boo",
        fail_value="hello foo boo",
        compare=snapshot.COMPARE.renotmatch(r"hello.*"),
    )


@TestFeature
@Name("compare")
def feature(self):
    """Check specifying comparison function."""
    for scenario in loads(current_module(), Scenario):
        scenario()
