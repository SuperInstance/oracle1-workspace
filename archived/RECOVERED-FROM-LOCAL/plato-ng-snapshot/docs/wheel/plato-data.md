# plato-data — PLATO Room Data Pipeline

**Repo:** `SuperInstance/plato-data` (2026-05-14)
**Status:** FORGOTTEN GOLD — The missing link between PLATO rooms and training.

## What It Is

A data loading layer that turns PLATO rooms, CSV files, JSONL logs, and fleet telemetry into training-ready tensors. The `DataRoom` class is a unified interface: `from_csv()`, `from_jsonl()`, `from_plato()`, `from_fleet_telemetry()`, `from_tensors()`.

## Why It Matters

Every ML pipeline in the PLATO ecosystem needs this. PLATO rooms → DataRoom → TensorDataset → DataLoader → training loop. It's the *plumbing* — boring but critical.

The **PLATO tile loader** (`from_plato()`) is the killer feature: fetches tiles from a PLATO room over HTTP, extracts features (with a user-provided `label_extractor` callback), and builds labeled tensors. This means any PLATO room full of Q&A tiles can be used as a training dataset directly.

The **fleet telemetry loader** (`from_fleet_telemetry()`) creates sliding windows over time-series agent metrics — CPU, memory, disk, status — for drift detection and anomaly classification.

## Forgotten Gold

- Zero coupling to any ML framework beyond PyTorch tensors
- `DataSpec` dataclass tracks schema: name, input_dim, num_classes, class_names
- `summary()` gives class distributions for imbalanced-data checking
- Full test suite (CSV, JSONL, split, dataset, dataloader, integration)
- Only 250 lines of Python — small enough to audit, complete enough to use

This repo was built to sit between `plato-trainer` and the raw data. It was never integrated. The plumbing works — it just needs to be connected to a training loop.
