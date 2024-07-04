from testflows.core import *
from requirements import *


@TestFeature
@Requirements(RQ_TestFlows_Snapshots_Function_Snapshot("1.0"))
@Name("snapshot")
def feature(self):
    """Check snapshot() function."""

    Feature(run=load("value", "feature"))
    Feature(run=load("mode", "feature"))
