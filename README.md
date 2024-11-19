**TestFlows Snapshots**
=======================

**Overview**
------------

TestFlows Snapshots is a Python module that provides support for snapshot-based testing. It allows you to store results of observed behavior and later compare them to expected values.

**Installation**
---------------

To install TestFlows Snapshots, use the following command:
```bash
pip install testflows
```
**Usage**
-----

The module provides a single function, `snapshot`, which is the main entry point for snapshot-based testing.

### Basic Usage

Here's an example of how to use the `snapshot` function:
```python
from testflows.snapshots import snapshot

# Store a value as a snapshot
snapshot(value="expected_value")

# Later, compare the observed value to the stored snapshot
snapshot(value="observed_value")
```
### Advanced Usage

The `snapshot` function takes several optional arguments that allow you to customize its behavior:

* `id`: a unique identifier for the snapshot
* `output`: a function to output the representation of the value
* `path`: a custom snapshot path
* `name`: the name of the snapshot value inside the snapshots file
* `encoder`: a custom snapshot encoder
* `comment`: a comment for the snapshot (deprecated)
* `mode`: the mode of operation (CHECK, UPDATE, REWRITE)
* `version`: the snapshot version
* `frame`: the caller frame
* `compare`: a custom comparison function

For example:
```python
snapshot(
    value="expected_value",
    id="my_snapshot",
    output=print,
    path="./snapshots",
    name="my_snapshot_value",
    encoder=lambda x: x.upper(),
    mode=snapshot.CHECK | snapshot.UPDATE,
    version=snapshot_v1.VERSION,
    frame=inspect.currentframe(),
    compare=lambda x, y: x == y
)
```
**Modes of Operation**
----------------------

The `snapshot` function can operate in three modes:

* `CHECK`: compare the observed value to the stored snapshot
* `UPDATE`: update the stored snapshot with the observed value
* `REWRITE`: rewrite all values in the snapshot file if the stored value is missing and the new value was added to the snapshot

You can combine these modes using bitwise OR operators.

**Storage Formats**
------------------

The module supports two storage formats:

* Python Module File (Version 1)
* JSON Lines File (Version 2)

You can specify the storage format using the `version` argument.