# TestFlows-Snapshots
TestFlows.com Open-Source Software Testing Framework's module for working with snapshots. 

## What are snapshots?

Snapshots are specialized files designed to capture and store the initial state of the system under test. 
This allows you to identify any changes in the system's behavior during subsequent test runs. The state is saved as key-value pairs in the following format:

```python
key_name_of_the_entry = r"""value that represents the state of the system."""
```

### How snapshots work?
When you execute your test program for the first time, a snapshot file is generated. This file captures and stores the values representing the system's state at that moment. During subsequent test executions, the actual values from the system are compared against those stored in the snapshot file.
If any discrepancies are found between the stored values and the actual output, an assertion error is raised. This error highlights that the expected output differs from the current state of the system, enabling you to detect regressions or unexpected changes effectively.

Snapshots are a powerful way to maintain consistency in testing and ensure that the system behaves as expected over time.

## How to use snapshots in TestFlows?

To utilize snapshots, you need to import the snapshot function from the asserts module:

```python
from testflows.asserts import snapshot
```

Here’s an example of how to use the snapshot function in a test:

```python
with values() as that:
    assert that(
        snapshot(
            system_output,
            name=snapshot_name,
            id=snapshot_id,
            mode=snapshot_mode,
        )
    ), error()
```

system_output here is the actual value from the system that you want to store in the snapshot. During future test runs, these values will be compared against the stored snapshot values.

### Parameters of the snapshot Function

- `name`: The key name within the snapshot file. For example: 

```python
key_name_of_the_entry = r"""value that represents the state of the system."""
```

In this case, `key_name_of_the_entry` is the `name`.

- `id`: Defines the name of the snapshot file itself, helping to distinguish between different snapshot files.
- `mode`: Determines the operation mode of the snapshot function. Modes include:
  - `CHECK`: Compares the actual value against the expected value stored in the snapshot.
  - `UPDATE`: Updates the snapshot file with the current values without performing assertions.
  - `REWRITE`: Rewrites the snapshot file with new values.
The default mode is `CHECK | UPDATE`, allowing the system to either validate or update the snapshot values automatically.