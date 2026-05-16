# Wheel Rebirth: plato-calibration-early-version

**Repo:** `SuperInstance/plato-calibration-early-version`
**Archived:** 2026-05-13 | **Scaffolding:** ~1KB

## What Was It?

An early experiment in **asynchronous calibration logic** — the mathematical machinery that determines when a PLATO agent has converged enough to "snap" (commit its context to an alignment artifact).

The core concepts:

- **MeasurementTriangle** — a triangle formed by three (time, weight) measurements. Its residual measures divergence from closed-loop convergence. When `a + b - c ≈ 0`, the triangle is aligned.
- **calibrate()** — given 3+ measurements, finds the point where residual falls below a threshold. This is the snap point.
- **snap()** — adjusts raw input to calibrated time/weight coordinates, producing a "snap" with a known residual.
- **CalibrationSecurity** — a 3-state drift monitor (normal → investigate → alarm) that watches agent residuals over time. Missing agents trigger glitch detection.

## What Was the Design Intent?

The design intent was **measurement-driven alignment**: agents don't arbitrarily declare themselves aligned — they accumulate observations until three consecutive measurements form a tight triangle, proving convergence mathematically. Calibration becomes a mathematical guarantee, not a heuristic. The security layer added operational confidence: if residuals spike or agents go silent, the system escalates.

## Absorbed Into What?

The **measurement triangle** and **snap-point residual** concepts are the mathematical foundation for plato-sdk's alignment lifecycle. plato-alignments uses `CalibrationSnapshot` objects. plato-sdk's tile lifecycle inherits the residual threshold logic. The security/glitch detection pattern lives in PLATO room fencing and agent health monitoring.

## Why It Matters

Without calibration, alignment is arbitrary. This repo encoded the insight that **alignment is measurable** — the triangle residual gives you a concrete number for "how aligned is this agent right now." That number is what makes the rest of the system deterministic.
