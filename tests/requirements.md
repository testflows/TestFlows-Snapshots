# SRS TestFlows Snapshots
# Software Requirements Specification

## Table of Contents

* 1 [Introduction](#introduction)
* 2 [Snapshots Module](#snapshots-module)
    * 2.1 [RQ.TestFlows.Snapshots](#rqtestflowssnapshots)
* 3 [Installing and Uninstalling](#installing-and-uninstalling)
    * 3.1 [RQ.TestFlows.Snapshots.InstallingAndUninstalling](#rqtestflowssnapshotsinstallinganduninstalling)
* 4 [The snapshot Function](#the-snapshot-function)
    * 4.1 [RQ.TestFlows.Snapshots.Function.Snapshot](#rqtestflowssnapshotsfunctionsnapshot)
* 5 [Storing or Comparing Value](#storing-or-comparing-value)
    * 5.1 [RQ.TestFlows.Snapshots.Function.Snapshot.Value](#rqtestflowssnapshotsfunctionsnapshotvalue)
* 6 [The Unique Identifier](#the-unique-identifier)
    * 6.1 [RQ.TestFlows.Snapshots.Function.Snapshot.Id](#rqtestflowssnapshotsfunctionsnapshotid)
* 7 [Outputing Encoded Value](#outputing-encoded-value)
    * 7.1 [RQ.TestFlows.Snapshots.Function.Snapshot.Output](#rqtestflowssnapshotsfunctionsnapshotoutput)
* 8 [Storage Path](#storage-path)
    * 8.1 [RQ.TestFlows.Snapshots.Function.Snapshot.Path](#rqtestflowssnapshotsfunctionsnapshotpath)
* 9 [Storing Multiple Values](#storing-multiple-values)
    * 9.1 [RQ.TestFlows.Snapshots.Function.Snapshot.Name](#rqtestflowssnapshotsfunctionsnapshotname)
* 10 [Value Encoder](#value-encoder)
    * 10.1 [RQ.TestFlows.Snapshots.Function.Snapshot.Encoder](#rqtestflowssnapshotsfunctionsnapshotencoder)
* 11 [Adding Comment](#adding-comment)
    * 11.1 [RQ.TestFlows.Snapshots.Function.Snapshot.Comment](#rqtestflowssnapshotsfunctionsnapshotcomment)
* 12 [Operation Modes](#operation-modes)
    * 12.1 [The CHECK Mode](#the-check-mode)
        * 12.1.1 [RQ.TestFlows.Snapshots.Function.Snapshot.Mode.CHECK](#rqtestflowssnapshotsfunctionsnapshotmodecheck)
    * 12.2 [The UPDATE Mode](#the-update-mode)
        * 12.2.1 [RQ.TestFlows.Snapshots.Function.Modes.UPDATE](#rqtestflowssnapshotsfunctionmodesupdate)
    * 12.3 [The REWRITE Mode](#the-rewrite-mode)
        * 12.3.1 [RQ.TestFlows.Snapshots.Function.Modes.REWRITE](#rqtestflowssnapshotsfunctionmodesrewrite)
* 13 [Storage Formats](#storage-formats)
    * 13.1 [Python Module File (Version 1)](#python-module-file-version-1)
        * 13.1.1 [RQ.TestFlows.Snapshots.Version1](#rqtestflowssnapshotsversion1)
    * 13.2 [JSON Lines File (Version 2)](#json-lines-file-version-2)
        * 13.2.1 [RQ.TestFlows.Snapshots.Version2](#rqtestflowssnapshotsversion2)

## Introduction

Snapshot testing is a practical approach to recording the behavior of software systems under test.

In many cases, the exact behavior might be unknown, the test oracle problem, or hard to determine,
however changes in behavior between different executions or versions might not be expected and therefore comparing
behavior between runs, software version, or even different software implementations is often useful. 

## Snapshots Module

### RQ.TestFlows.Snapshots
version: 1.0

The `snapshots` module SHALL implement functionality that supports snapshot-testing
by storing results of the observed behavior and comparing bahavior to the stored values.

## Installing and Uninstalling

### RQ.TestFlows.Snapshots.InstallingAndUninstalling
version: 1.0

The `snapshots` module SHALL support to be installed and uninstalled using the `pip` Python package manager.

```
pip install testflows.snapshots
pip uninstall testflows.snapshots
```

## The snapshot Function

### RQ.TestFlows.Snapshots.Function.Snapshot
version: 1.0

The `snapshots` module SHALL provide the `snapshot()` function that SHALL server
as the main function provided by the module.

The `snapshot()` function SHALL have the following definition.

```python
def snapshot(
    value,
    id=None,
    output=None,
    path=None,
    name="snapshot",
    encoder=repr,
    comment=None,
    mode=SNAPSHOT_MODE_CHECK | SNAPSHOT_MODE_UPDATE,
    version=snapshot_v1.VERSION,
)
```

## Storing or Comparing Value

### RQ.TestFlows.Snapshots.Function.Snapshot.Value
version: 1.0

The value that SHALL be stored or compared against the snapshot
SHALL be specified using the `value` argument of the `snapshot()` function.
The `value` can be of any type that can be encoded by the `encoder`
or the `ValueError` exception SHALL be raise if the `value` can't be encoded.

The `value` argument SHALL be the first argument of the `snapshot()` function
and the only argument that SHALL be expected to be specified by the user by its position.

```python
snapshot("my value", encoder=str)
```

## The Unique Identifier

### RQ.TestFlows.Snapshots.Function.Snapshot.Id
version: 1.0

The unique idenfier SHALL be specified using the `id` argument of the `snapshot()` function.

Different values of the `id` argument SHALL cause the `snapshot()` function
to store values uniquely for the exact same caller source code file
and `name`.

```python
snapshot("my value", id="1", name="name")
snapshot("my value", id="2", name="name")
```

## Outputing Encoded Value

### RQ.TestFlows.Snapshots.Function.Snapshot.Output
version: 1.0

Outputting encoded value SHALL be supported using the `output` argument of the `snapshot()` function
that SHALL accept a callable to which the encoded value SHALL be passed.

```python
snapshot("my value", encoder=json, output=lambda v: print(v))
```

## Storage Path

### RQ.TestFlows.Snapshots.Function.Snapshot.Path
version: 1.0

The storage path for the value snapshots SHALL be specified using the `path` argument of the `snapshot()` function.

The default `path` SHALL be `./snapshots`.

```python
snapshot("my value", path="./custom-path")
```

## Storing Multiple Values

### RQ.TestFlows.Snapshots.Function.Snapshot.Name
version: 1.0

Multiple values SHALL stored in the snapshot if unique value name is epcified using the `name` argument of the `snapshot()` function.

```python
snapshot("my value", name="v1")
snapshot("my value", name="v2")
```

## Value Encoder

### RQ.TestFlows.Snapshots.Function.Snapshot.Encoder
version: 1.0

The encoder used to conver value into its stored representation SHALL be specified using the `encoder`
argument of the `snapshot()` function.

The default encoder SHALL be `repr`.

```python
snapshot(my_object, encoder=str)
```

## Adding Comment

### RQ.TestFlows.Snapshots.Function.Snapshot.Comment
version: 1.0

Adding custom comment for the stored value inside the snapshot SHALL be deprecated
and any value passed to the `comment` argument in the `sanpshot()` function SHALL be ignored.

```python
snapshot("my value", comment="comment that will be ignored")
```

## Operation Modes

### The CHECK Mode

#### RQ.TestFlows.Snapshots.Function.Snapshot.Mode.CHECK
version: 1.0

The `CHECK` mode SHALL be specified using the `mode` argument of the `snapshot()` function
and SHALL cause the function to raise `SnapshotError` exception
if the stored value does not match the expected `value`.

The `CHECK` mode SHALL be set using the `snapshot.CHECK` flag. 

```python
snapshot("expected value", mode=snapshot.CHECK)
```

### The UPDATE Mode

#### RQ.TestFlows.Snapshots.Function.Modes.UPDATE
version: 1.0

The `UPDATE` mode SHALL be specified using the `mode` argument of the `snapshot()` function
and SHALL cause the function to raise `SnapshotError` exception
if the stored value is missing and this mode is not set.

If the stored value is missing and this mode is set then the `snapshot()` function
SHALL add the expected value to the snapshot and no exception SHALL be raised.

The `UPDATE` mode SHALL be set using the `snapshot.UPDATE` flag. 

```python
snapshot("expected value", mode=snapshot.UPDATE)
```

### The REWRITE Mode

#### RQ.TestFlows.Snapshots.Function.Modes.REWRITE
version: 1.0

The `REWRITE` mode SHALL be specified using the the `mode` argument of the `snapshot()` function
and SHALL cause the function to rewrite all the values in the snapshot
in a fixed order if and only if the stored value is missing and the new value was added to the snapshot.

```python
snapshot("expected value", mode=snapshot.REWRITE)
```

## Storage Formats

### Python Module File (Version 1)

#### RQ.TestFlows.Snapshots.Version1
version: 1.0

The `snapshot` module SHALL support storing snapshots as a Python module file
by specifying the `version` argument of the `snapshot()` function.

The Python module file format SHALL be specified as `snapshot.VERSION_V1` and
SHALL be the default format.

The `snapshot.VERSION_V1` SHALL be equal to integer value of `1`.

```python
snapshot("my value", version=snapshot.VERSION_V1)
```

### JSON Lines File (Version 2)

#### RQ.TestFlows.Snapshots.Version2
version: 1.0

The `snapshot` module SHALL support storing snapshots as a JSON lines file
by specifying the `version` argument of the `snapshot()` function.

The JSON lines format SHALL store each value as JSON object on its own line.

The JSON lines file format SHALL be specified as `snapshot.VERSION_V2` and
must be specified explicitly.

The `snapshot.VERSION_V2` SHALL be equal to integer value of `2`.

```python
snapshot("my value", version=snapshot.VERSION_V2)
```







