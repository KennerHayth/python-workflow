# Python Workflow Template

A lightweight Python task orchestrator that runs multi-step automation 
workflows with dependency management and parallel execution — built 
entirely with the standard library under strict policy and resource 
constraints (no external packages).

## How It Works

Each step in the workflow is defined as a `Function` object with a name, 
a script to run, and a list of dependencies. The orchestrator resolves 
the dependency graph at runtime, launches tasks as their dependencies 
complete, and tracks pass/fail state for every step.
```python
# Define tasks and their dependencies
export_step  = Function(name="export",  dependencies=[],            script="export.py")
process_step = Function(name="process", dependencies=[export_step], script="process.py")

task_list = [export_step, process_step]
run_workflow(task_list)
```

## Features

- Dependency-aware execution — tasks wait for upstream steps to complete
- Cascading failure — if a dependency fails, dependent tasks are 
  automatically marked failed
- Parallel execution up to a configurable `MAX_TASK` limit
- Per-task status tracking: `PENDING → RUNNING → PASSED / FAILED`
- No external dependencies — standard library only (`subprocess`, 
  `enum`, `os`, `sys`)

## Requirements

- Python 3.6+

## Usage

1. Define your scripts as `Function` objects with their dependencies
2. Append them to `task_list`
3. Call `run_workflow(task_list)`

## Why This Exists

Built for a production environment where only Python was available and 
no third-party orchestration tools (Airflow, Prefect, etc.) could be 
installed. This covers the core use case: run a sequence of scripts 
in the right order, in parallel where possible, and stop cleanly on 
failure.

## Status
Stable template. Extend by adding your own script references to 
`task_list`.
