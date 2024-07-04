#!/usr/bin/env python3
import sys
from testflows.core import *

append_path(sys.path, ".")
from requirements import *


@TestFeature
@Specifications(SRS_TestFlows_Snapshots_Module)
@Requirements(RQ_TestFlows_Snapshots("1.0"))
@Name("snapshots module")
def regression(self):
    """The snapshots module regression tests."""
    Feature(run=load("snapshot", "feature"))


if main():
    regression()
