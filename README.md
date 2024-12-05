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

Here is an example of a snapshot file content:

```python
SNAPPY_BINARY_UTF8_optional_1_0_toString = r"""'{rows_read: 100}, initial_rows: 1500, file_structure: utf8\tNullable(String), condition: WHERE utf8 = toString(value)'"""

SNAPPY_BINARY_UTF8_optional_1_0_toStringCutToZero = r"""'{rows_read: 100}, initial_rows: 1500, file_structure: utf8\tNullable(String), condition: WHERE utf8 = toStringCutToZero(value)'"""

SNAPPY_BINARY_UTF8_optional_1_0_reinterpretAsString = r"""'{rows_read: 100}, initial_rows: 1500, file_structure: utf8\tNullable(String), condition: WHERE utf8 = reinterpretAsString(value)'"""

SNAPPY_BINARY_UTF8_optional_1_0_toLowCardinality = r"""'{rows_read: 100}, initial_rows: 1500, file_structure: utf8\tNullable(String), condition: WHERE utf8 = toLowCardinality(value)'"""
```
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
            value=system_output,
            name=snapshot_name,
            id=snapshot_id,
            mode=snapshot.CHECK,
        )
    ), error()
```

### Parameters of the snapshot Function
- `value:` The actual value from the system that you want to store in the snapshot.
- `name`: The key name within the snapshot file. For example:

  ```python
  key_name_of_the_entry = r"""value that represents the state of the system."""
  ```

- `id:` Defines the name of the snapshot file itself, helping to distinguish between different snapshot files.
- `mode:` Determines the operation mode of the snapshot function. Modes include:
  - `CHECK:` Compares the actual value against the expected value stored in the snapshot.
  - `UPDATE:` Updates the snapshot file with the current values without performing assertions.
  - `REWRITE:` Rewrites the snapshot file with new values.

The default mode is `CHECK | UPDATE`, allowing the system to either validate or update the snapshot values automatically.

### Custom Comparison

The `testflows.snapshots` module offers the ability to specify custom comparison functions, providing flexibility for handling complex or dynamic use cases. Here are some interesting use cases:

#### Regex Substitution for Snapshot and Actual Value

You can use regular expression substitution to strip dynamic parts from both the snapshot and the actual value before performing the comparison. This ensures that only the static portions are validated.

```python
snapshot(
    value=f"hello {time.time()}",
    mode=snapshot.CHECK,
    compare=snapshot.COMPARE.resub(r"\d+(\.\d+)?")
)
```

In this case:

- The dynamic numeric portion (e.g., timestamps) is removed from both the snapshot and actual value using `re.sub`.
- The remaining static portions are compared for equality.

#### Regex Match for Comparison

Instead of checking for strict equality, you can use regular expression matching to validate both the snapshot and the actual value.

```python
snapshot(
    value=f"hello {time.time()}",
    mode=snapshot.CHECK,
    compare=snapshot.COMPARE.rematch(r"hello.*")
)
```

Here a regex pattern (e.g., hello.*) ensures that both values match a specified format or pattern rather than being exactly identical.


#### Dynamic Evaluation

You can dynamically evaluate the actual value at runtime and compare it without strictly relying on the snapshot value. This is useful for scenarios where the snapshot serves as a placeholder but the actual validation is context-sensitive.

```python
snapshot(
    value=f"{time.time()}",
    mode=snapshot.CHECK,
    compare=lambda a, b: time.time() - 1 < float(b[1:-1]) < time.time() + 1
)
```

In this scenario:

- A lambda function dynamically checks if the actual value is within a specific range (e.g., within ±1 second of the current time).
- The snapshot value is effectively bypassed for comparison, allowing fully dynamic validation.