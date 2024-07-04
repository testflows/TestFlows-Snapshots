import operator

from functools import reduce

from testflows.snapshots import snapshot
from testflows.combinatorics import combinations


def modes():
    """Return all possible combinations of modes."""

    flags = [snapshot.CHECK, snapshot.UPDATE, snapshot.REWRITE]

    modes = list(combinations(flags, 3))
    modes += list(combinations(flags, 2))
    modes += list(combinations(flags, 1))

    return [reduce(operator.or_, combination) for combination in modes]
