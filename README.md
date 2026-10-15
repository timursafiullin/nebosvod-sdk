# Nebosvod SDK

Public toolkit for building computational modules for Nebosvod, a platform for reproducible experiments with
space systems. A module implements one **port** — for example an orbit estimator, a conjunction risk assessor,
a maneuver planner, an observation scheduler or a routing policy — and is tested inside Nebosvod against
known simulated truth, without ever seeing that truth.

Status: pre-release skeleton: installable, no ports yet.

## Contents (planned)

| Folder | Content |
| --- | --- |
| `schemas/` | Port contracts (JSON Schema), published from the Nebosvod repository; do not edit by hand |
| `python/nebosvod_sdk/` | Base classes for ports, typed data models, standalone test harness |
| `templates/` | One ready-to-fill module template per port |
| `examples/` | Reference modules (e.g. EKF estimator, Monte Carlo collision probability) |
| `fixtures/` | Recorded port inputs for running modules without the application |
| `docs/` | SDK documentation |

## Module in one picture

A module is packaged as a `.nebmod` archive: `module.toml` (id, version, port, execution mode, limits,
decision latency), code or binary or ONNX model, and its own tests. Execution modes: in-process Python,
subprocess in any language (NDJSON + Arrow IPC), container/service, or ONNX model only.

## Development

With Python 3.12+ and uv installed, run from the repository root:

```bash
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest
```

## License

Apache License 2.0 — see `LICENSE` and `NOTICE`.
