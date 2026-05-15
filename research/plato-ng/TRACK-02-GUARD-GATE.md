# Track 2: GUARD-as-Gate for PLATO-NG

> **P5 Constraint Gate — Tile validation through FLUX GUARD constraints**
>
> Research Track Lead: Oracle1
> Date: 2026-05-15
> Status: Design sketch

---

## 1. Problem Statement

PLATO's current gate system (P0-P4) validates tiles through procedural Python code in `plato-room-server.py`:

| Gate | Check | Implementation |
|------|-------|----------------|
| P0 | Required fields | `if field not in tile` — 5 lines |
| P1 | Length bounds | `if len(answer) < 20` — 4 lines |
| P2 | No absolute claims | `if word in answer` — 8 lines |
| P3 | Confidence bounds | `if not (0.0 <= conf <= 1.0)` — 3 lines |
| P4 | Duplicate detection | `hashlib.sha256(...)` — 5 lines |

This works but has **no schema**: every tile is validated against the same generic rules. PLATO-NG needs **per-tile validation** — each tile type (chess-move, training-tile, sensor-reading) should declare its own constraint schema.

GUARD (FM's constraint DSL) already exists as a full compilation pipeline. The question: **Can GUARD constraints serve as PLATO tile schemas and validation gates?**

---

## 2. Existing Infrastructure Summary

### 2.1 GUARD DSL (CHIPS Alliance + Fleet Fork)

GUARD is a declarative constraint language. Standard syntax:

```guard
// Constraint with typed inputs and a named predicate
type chess_move: struct {
    from: string,         // Algebraic notation: "e2"
    to: string,           // "e4"
    piece_type: string,   // "pawn"
    captured: string?,    // Optional: piece captured
    is_capture: bool,
    move_number: uint32,
    side: enum { white, black }
}

constraint valid_chess_move {
    // Required fields must be non-empty
    from != "" && to != "" && piece_type != ""
    
    // Piece must be recognized
    piece_type in ["pawn", "knight", "bishop", "rook", "queen", "king"]
    
    // Move number must be positive
    move_number >= 1
    
    // Consistency: if captured piece set, is_capture must be true
    captured != "" IMPLIES is_capture == true
}
```

**Compilation targets** (via `guardc`):
- `--target c` → C runtime checker function
- `--target systemverilog` → Hardware assertions
- `--target eBPF` → Linux security module rules
- `--target wasm32` → WebAssembly sandbox
- `--target flux-ir` → FLUX intermediate representation (fleet extension)
- `--arget avx-512` → Vectorized assembly (fleet extension)
- `--target smt` → Z3/CVC5 SMT obligations (fleet extension)

### 2.2 FLUX Compilation Pipeline (Fleet Fork)

```
GUARD (.guard)
    ↓
guardc --target flux-ir
    ↓
FLUX IR (JSON AST)
    ↓
flux-compiler Plane 2 → Plane 1 → Plane 0
    ↓
FLUX Bytecode (.fluxb)
    ↓
FLUX VM (Rust/Python/C)
```

Key: GUARD → FLUX IR is a **compilation target** of `guardc`. The FLUX compiler takes it the rest of the way.

### 2.3 PLATO Tile Format (Current)

```python
tile = {
    "domain": "chess",
    "question": "e2-e4",
    "answer": "...long explanation...",
    "confidence": 0.92,
    "_hash": "a1b2c3d4",
    "provenance": [
        {"agent": "oracle1", "cycle": 42, "timestamp": "..."}
    ]
}
```

### 2.4 PLATO-NG Tile Format (Planned)

```python
tile = {
    "type": "chess-move",       # ← schema selector
    "version": 1,
    "data": {
        "from": "e2",
        "to": "e4",
        "piece_type": "pawn",
        "is_capture": False,
        "move_number": 1,
        "side": "white"
    },
    "provenance": [
        {"agent": "lucineer", "cycle": 43, "timestamp": "..."}
    ],
    "signature": "..."           # Optional: FM consensus signature
}
```

The `type` field selects a GUARD constraint. The `data` field is validated against that constraint.

---

## 3. Design: P5 Constraint Gate

### 3.1 Gate Architecture

```
Human/Agent submits tile
    │
    ▼
┌─────────────────────────────────────────────────┐
│                  GATE PIPELINE                    │
│                                                   │
│  P0: Required fields (fast path, procedural)      │
│  P1: Length bounds (fast path, procedural)         │
│  P2: Truthfulness (fast path, procedural)          │
│  P3: Confidence bounds (fast path, procedural)     │
│  P4: Duplicate check (fast path, hash)             │
│  ─────────────────────────────────────────────    │
│  P5: CONSTRAINT GATE ⭐ ← NEW                      │
│      │                                             │
│      ├── Look up tile["type"] in constraint reg.   │
│      ├── GUARD constraint loaded? → validate      │
│      ├── No GUARD constraint? → pass through       │
│      └── Constraint fails? → REJECT + reason      │
│                                                   │
│  P6: Provenance signature check (future)           │
└─────────────────────────────────────────────────┘
    │
    ▼
Accepted (tile added to room) / Rejected (error returned)
```

### 3.2 The Constraint Registry

A registry maps `tile_type → GUARD constraint file`:

```python
CONSTRAINT_REGISTRY = {
    "chess-move": {
        "guard_file": "schemas/chess-move.guard",
        "compiled": "schemas/chess-move.fluxb",     # FLUX bytecode (fast path)
        "validator": None,                            # fallback: native function
        "description": "Standard chess move schema"
    },
    "training-tile": {
        "guard_file": "schemas/training-tile.guard",
        "compiled": None,                              # Use runtime compiler
        "validator": "builtin",                        # Built-in P0-P4 gates
        "description": "Default training tile (backward compat)"
    },
    "sensor-reading": {
        "guard_file": "schemas/sensor.guard",
        "compiled": "schemas/sensor.wasm",             # WebAssembly sandbox
        "validator": None,
        "description": "Temperature/pressure sensor reading"
    }
}
```

**Design decision: 3 execution modes for P5**

| Mode | How | When | Latency |
|------|-----|------|---------|
| **FLUX bytecode** | `FLUX-VM` evaluates `.fluxb` | Pre-compiled constraints | ~1-10µs |
| **Native C** | `guardc --target c` → dlopen | Z3-validated constraints | ~0.1µs |
| **Interpreted** | GUARD → JSON IR → tree-walk | Dynamic/experimental constraints | ~100µs |

The **simplest possible implementation** uses interpretative mode: parse the GUARD constraint into a JSON AST tree, walk it against the tile. No pre-compilation needed.

### 3.3 Execution Flow (Interpretive Mode)

```python
class P5ConstraintGate:
    """PLATO-NG P5: GUARD constraint validation gate."""
    
    def __init__(self):
        self.registry = {}           # tile_type → constraint spec
        self.parsed_cache = {}       # guard_path → AST tree
        self.stats = {"passed": 0, "failed": 0}
    
    def register(self, tile_type: str, guard_path: str):
        """Register a GUARD constraint for a tile type."""
        self.registry[tile_type] = {"path": guard_path, "parsed": None}
    
    def validate(self, tile: dict) -> tuple[bool, str]:
        """Validate a tile against its type's GUARD constraint."""
        tile_type = tile.get("type", "training-tile")
        
        # No constraint registered → pass through (backward compat)
        if tile_type not in self.registry:
            return True, "no constraint registered"
        
        spec = self.registry[tile_type]
        
        # Parse GUARD → JSON AST (cached)
        if spec["parsed"] is None:
            with open(spec["path"]) as f:
                ast = parse_guard_to_ast(f.read())
            spec["parsed"] = ast
        
        # Evaluate AST against tile data
        return evaluate_constraint(ast, tile.get("data", {}))
```

---

## 4. How GUARD Constraint Becomes a Tile Validation Rule

### 4.1 The Compilation Chain (Formal Path)

```
GUARD constraint file
    │
    ▼
┌─────────────────────────────────────────────────────┐
│              guardc --target flux-ir                  │
│                                                       │
│  Input:  .guard file with type declarations           │
│  Output: JSON IR (constraints, types, metadata)        │
│                                                       │
│  Example output:                                      │
│  {                                                     │
│    "types": {                                          │
│      "tile_data": {                                   │
│        "fields": {                                     │
│          "from": "string",                             │
│          "to": "string",                               │
│          "piece_type": "string",                       │
│          "is_capture": "bool",                         │
│          "move_number": "uint32"                       │
│        }                                               │
│      }                                                 │
│    },                                                  │
│    "constraints": [{                                   │
│      "name": "valid_chess_move",                       │
│      "predicate": {                                    │
│        "op": "and",                                    │
│        "args": [...]                                   │
│      }                                                  │
│    }]                                                   │
│  }                                                     │
└─────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────┐
│              PLATO-NG P5 Gate Engine                   │
│                                                       │
│  1. Load JSON IR                                      │
│  2. Extract types → field schema                      │
│  3. Extract field-level constraints                   │
│  4. Compile to PLATO evaluation tree                  │
│  5. Cache for replay                                  │
└─────────────────────────────────────────────────────┘
    │
    ▼
Tile validation at runtime

**Deep optimization path** (not required for MVP):
    │
    ▼
┌─────────────────────────────────────────────────────┐
│         FLUX Compiler Planes 2→1→0                    │
│                                                       │
│  FLUX IR → FLUX Bytecode → Native/AVX-512            │
│  → 50µs per constraint eval → 38 billion/sec vec     │
└─────────────────────────────────────────────────────┘
```

### 4.2 The Evaluation Tree

The JSON IR is compiled to an evaluation tree that PLATO walks directly:

```python
class ConstraintEval:
    """Evaluator for parsed GUARD constraints against tile data."""
    
    def __init__(self, ir: dict):
        self.types = ir.get("types", {})
        self.constraints = ir.get("constraints", [])
    
    def evaluate(self, data: dict) -> tuple[bool, list[str]]:
        """Evaluate all constraints against data. Returns (pass, reasons)."""
        violations = []
        
        # 1. Type check: verify all fields have correct types
        for type_name, type_spec in self.types.items():
            fields = type_spec.get("fields", {})
            for field_name, expected_type in fields.items():
                val = data.get(field_name)
                if val is None:
                    violations.append(f"Missing field: {field_name}")
                    continue
                if not self._check_type(val, expected_type):
                    violations.append(
                        f"Type mismatch: {field_name} should be {expected_type}"
                    )
        
        # 2. Constraint evaluation
        for constraint in self.constraints:
            if not self._eval_node(constraint["predicate"], data):
                violations.append(f"Constraint violated: {constraint['name']}")
        
        return len(violations) == 0, violations
```

### 4.3 Guardc Integration (MVP)

The simplest path: **invoke `guardc` as a subprocess at registration time**, parse the emitted JSON IR.

```python
import subprocess
import json

def compile_guard(guard_path: str) -> dict:
    """Compile a GUARD file to JSON IR using guardc."""
    result = subprocess.run(
        ["guardc", "compile", "--emit-ir", guard_path],
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode != 0:
        raise ValueError(f"GUARD compilation failed: {result.stderr}")
    return json.loads(result.stdout)
```

This is the simplest possible implementation: subprocess, JSON IR, tree evaluation. No FLUX VM required for MVP.

---

## 5. Concrete Example: Chess Move Tile Schema

### 5.1 GUARD Constraint Definition

```guard
// File: schemas/chess-move.guard
// PLATO-NG P5 constraint: validates chess move tiles

// ── Tile schema ──
type chess_move_tile: struct {
    from: string,                // Starting square: "a1" through "h8"
    to: string,                  // Target square: "a1" through "h8"
    piece_type: string,          // One of 6 standard pieces
    is_capture: bool,
    captured_piece: string?,     // Optional: piece captured (only if is_capture)
    move_number: uint32,
    side: enum { white, black },
    promotion: string?,          // Optional: promoted piece (only for pawns on 8th)
    castle: enum { none, kingside, queenside },
    en_passant: bool,
    check: bool,
    checkmate: bool
}

// ── Helper constraints ──
constraint valid_square(s: string): bool {
    // Chess squares go a1-h8
    let valid_files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
    let valid_ranks = ['1', '2', '3', '4', '5', '6', '7', '8'];
    return len(s) == 2 && s[0] in valid_files && s[1] in valid_ranks;
}

constraint valid_piece(p: string): bool {
    return p in ["pawn", "knight", "bishop", "rook", "queen", "king"];
}

constraint valid_promotion(p: string): bool {
    // Pawns can promote to anything except pawn and king
    return p in ["knight", "bishop", "rook", "queen"];
}

// ── Main constraint ──
constraint valid_chess_move(tile: chess_move_tile): bool {
    // Field-level: required
    valid_square(tile.from) &&
    valid_square(tile.to) &&
    valid_piece(tile.piece_type) &&
    tile.from != tile.to &&  // Must move
    
    // Move number
    tile.move_number >= 1u &&
    
    // Capture consistency
    (tile.is_capture == true IMPLIES tile.captured_piece != "" &&
                                valid_piece(tile.captured_piece)) &&
    (tile.is_capture == false IMPLIES tile.captured_piece == "") &&
    
    // Castle consistency
    (tile.castle != none IMPLIES tile.piece_type == "king") &&
    
    // Promotion consistency (pawn reaching 8th rank)
    (tile.promotion != "" IMPLIES 
        tile.piece_type == "pawn" &&
        valid_promotion(tile.promotion) &&
        (tile.to[1] == '8' || tile.to[1] == '1')) &&
    
    // Side is valid
    tile.side in {white, black};
}
```

### 5.2 PLATO-NG Registration

```bash
# Register a GUARD constraint for chess-move tiles
curl -X POST http://localhost:8847/plato-ng/gate/register \
  -H "Content-Type: application/json" \
  -d '{
    "tile_type": "chess-move",
    "guard_source": "schemas/chess-move.guard",
    "mode": "interpretive"
  }'
```

Response:
```json
{
  "status": "ok",
  "tile_type": "chess-move",
  "compiled": true,
  "constraints": 1,
  "types": 1,
  "memory_kb": 4
}
```

### 5.3 Submission Flow

```
Submit valid tile:
  POST /plato-ng/room/chess-game/tile
  {"type": "chess-move", "data": {"from": "e2", "to": "e4", ...}}
  → 200 Accepted (tile added to room)
  → Room passes through R0-R4 gates
  → P5 constraint evaluates: passes
  → Tile stored

Submit invalid tile:
  POST /plato-ng/room/chess-game/tile
  {"type": "chess-move", "data": {"from": "e9", "to": "e4", ...}}  ← invalid square
  → P0-P4 pass
  → P5 constraint evaluates:
    - "valid_square('e9'): 'e9'[0] not in valid_files"
    - "from field validation failed"
  → 422 Unprocessable Entity
    {"error": "Constraint violation", "reasons": ["Invalid from square: e9"]}
```

---

## 6. Z3 SMT Integration Path

### 6.1 Why Z3 for PLATO Gates

Some validation goes beyond field checking. Examples:
- **Mutually exclusive fields**: "captured_piece must be set iff is_capture is true"
- **Cross-field consistency**: "promotion implies pawn is on 8th rank"
- **State-dependent rules**: "Castling requires game state where king+rook haven't moved"
- **Temporal constraints**: "move_number must be +1 from previous tile"

GUARD already compiles these constraints to SMT obligations (from the onboarding docs: "GUARD → SMT obligations" → Z3/CVC5). PLATO can leverage this for **stateful gate validation**:

```python
def evaluate_stateful(tile: dict, previous_tile: dict, guard_ir: dict) -> bool:
    """
    Evaluate constraints that depend on previous state.
    
    GUARD constraints with temporal operators compile to SMT
    obligations that Z3 resolves.
    """
    from z3 import Solver, Int, Bool, And, Or, Not, Implies
    
    s = Solver()
    
    # Tile fields as Z3 variables
    t_from = Int("tile.from")
    t_to = Int("tile.to")
    t_move = Int("tile.move_number")
    
    # Previous tile fields
    p_move = Int("prev.move_number")
    
    # Constraint: move_number increments by exactly 1
    s.add(t_move == p_move + 1)
    
    return s.check() == sat
```

### 6.2 When to Use Z3 vs. Direct Eval

| Evaluation Pattern | Direct Eval | Z3 SMT |
|-------------------|-------------|--------|
| Field type checking | ✅ Fast | ❌ Overkill |
| Field range/domain | ✅ Fast | ❌ Overkill |
| Cross-field logic | ✅ Fast (~10 fields) | ✅ Good (>10 fields) |
| Temporal/sequence | ❌ Can't do | ✅ Required |
| Proves: "no valid tile violates constraint" | ❌ Can't do | ✅ Required |

**MVP decision**: Direct evaluation only. Z3 integration is Phase 2.

---

## 7. Implementation Sketch (MVP)

### 7.1 File Structure

```
plato-ng/
├── gate/
│   ├── __init__.py
│   ├── p5_constraint_gate.py     # P5 gate implementation
│   ├── guard_compiler.py         # GUARD → IR compiler bridge
│   ├── constraint_eval.py        # IR evaluation tree walker
│   ├── registry.py               # Tile type → constraint mapping
│   └── schemas/                  # .guard files (shipped defaults)
│       ├── chess-move.guard
│       ├── training-tile.guard
│       └── sensor-reading.guard
├── tests/
│   └── test_p5_gate.py
└── research/
    └── TRACK-02-GUARD-GATE.md    # This document
```

### 7.2 Core Logic (p5_constraint_gate.py)

```python
"""
PLATO-NG P5 Constraint Gate

Validates tiles against GUARD constraint schemas.
Modes: interpretive (default), native, flux-vm
"""

import json
import hashlib
from pathlib import Path
from typing import Optional

# Mode constants
MODE_INTERPRETIVE = "interpretive"   # Parse GUARD→IR, tree-walk
MODE_NATIVE = "native"               # guardc --target c → dlopen .so
MODE_FLUX_VM = "flux-vm"             # guardc --target flux-ir → FLUX VM


class P5ConstraintGate:
    """The P5 gate. Validates tile data against GUARD constraints."""
    
    def __init__(self, schemas_dir: str = "schemas"):
        self.schemas_dir = Path(schemas_dir)
        self.registry: dict[str, ConstraintSpec] = {}
        self.stats = {"passed": 0, "rejected": 0, "unknown": 0}
    
    def register(self, tile_type: str, guard_file: str,
                 mode: str = MODE_INTERPRETIVE) -> dict:
        """Register a tile type with its GUARD constraint."""
        guard_path = self.schemas_dir / guard_file
        if not guard_path.exists():
            return {"status": "error", "message": f"File not found: {guard_path}"}
        
        # Compile GUARD → JSON IR
        from .guard_compiler import compile_guard
        ir = compile_guard(str(guard_path))
        
        self.registry[tile_type] = ConstraintSpec(
            tile_type=tile_type,
            guard_path=guard_path,
            ir=ir,
            mode=mode
        )
        
        return {
            "status": "ok",
            "tile_type": tile_type,
            "constraints": len(ir.get("constraints", [])),
            "types": len(ir.get("types", {}))
        }
    
    def validate(self, tile: dict) -> tuple:
        """
        Validate a tile against its registered GUARD constraint.
        Returns (passed: bool, reasons: list[str], mode: str)
        """
        tile_type = tile.get("type")
        
        # No constraint registered → pass (backward compat)
        if tile_type not in self.registry:
            self.stats["unknown"] += 1
            return True, [], "passthrough"
        
        spec = self.registry[tile_type]
        data = tile.get("data", {})
        
        # Evaluate based on mode
        if spec.mode == MODE_INTERPRETIVE:
            from .constraint_eval import ConstraintEval
            evaler = ConstraintEval(spec.ir)
            passed, reasons = evaler.evaluate(data)
        elif spec.mode == MODE_NATIVE:
            import ctypes
            lib = ctypes.CDLL(str(spec.compiled_so))
            passed = lib.validate(json.dumps(data).encode("utf-8"))
            reasons = []
        else:
            return True, [], "unknown_mode"
        
        if passed:
            self.stats["passed"] += 1
        else:
            self.stats["rejected"] += 1
        
        return passed, reasons, spec.mode
```

### 7.3 guard_compiler.py (MVP)

```python
"""
Bridge from .guard files to PLATO JSON IR.
MVP: subprocess invoke guardc. Phase 2: native Python parser.
"""

import json
import subprocess
import tempfile


def compile_guard(guard_source_or_path: str) -> dict:
    """Compile GUARD to JSON IR. Accepts file path or inline source."""
    
    # If it's a file path, read it
    if "\n" not in guard_source_or_path and len(guard_source_or_path) < 500:
        with open(guard_source_or_path) as f:
            guard_source = f.read()
    else:
        guard_source = guard_source_or_path
    
    # MVP: call guardc as subprocess
    with tempfile.NamedTemporaryFile(suffix=".guard", mode="w", delete=False) as f:
        f.write(guard_source)
        tmp_path = f.name
    
    try:
        result = subprocess.run(
            ["guardc", "compile", "--emit-ir", tmp_path],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            raise ValueError(f"guardc error: {result.stderr}")
        return json.loads(result.stdout)
    except FileNotFoundError:
        # Fallback: simple internal parser for basic constraints
        return _parse_guard_simple(guard_source)
    finally:
        import os
        os.unlink(tmp_path)


def _parse_guard_simple(source: str) -> dict:
    """
    Fallback parser for simple GUARD-style constraints.
    Handles: field type declarations, range checks, domain checks.
    
    This lets PLATO-NG work WITHOUT guardc installed.
    """
    # Simplified parser — recognizes:
    #   type X: struct { field_name: type }
    #   constraint X: predicate
    # Returns same JSON IR format as guardc
    ...
```

### 7.4 constraint_eval.py (Tree Walker)

```python
"""
Evaluates GUARD constraint IR against tile data.
Pure Python, zero dependencies.
"""

from typing import Any


class ConstraintEval:
    """Walk the GUARD IR tree and evaluate against tile data."""
    
    def __init__(self, ir: dict):
        self.types = ir.get("types", {})
        self.constraints = ir.get("constraints", [])
    
    def evaluate(self, data: dict) -> tuple[bool, list[str]]:
        violations = []
        
        # Phase 1: Type checking
        for type_name, type_spec in self.types.items():
            self._check_type_fields(type_spec.get("fields", {}), data, violations)
        
        # Phase 2: Constraint evaluation
        for constraint in self.constraints:
            if not self._eval(constraint.get("predicate", {}), data):
                violations.append(f"Constraint: {constraint['name']}")
        
        return len(violations) == 0, violations
    
    def _check_type_fields(self, fields: dict, data: dict, violations: list):
        for field, expected in fields.items():
            val = data.get(field)
            if val is None:
                violations.append(f"Missing: {field}")
                continue
            if not self._match_type(val, expected):
                violations.append(f"Type: {field} expected {expected}")
    
    def _match_type(self, val: Any, expected: str) -> bool:
        type_map = {
            "string": str, "uint32": int, "bool": bool,
            "float32": (int, float), "int32": int
        }
        expected_type = type_map.get(expected)
        if expected_type:
            return isinstance(val, expected_type)
        return True  # Unknown types pass through
    
    def _eval(self, node: dict, data: dict) -> bool:
        """Recursive node evaluation."""
        op = node.get("op")
        
        if op == "and":
            return all(self._eval(arg, data) for arg in node.get("args", []))
        elif op == "or":
            return any(self._eval(arg, data) for arg in node.get("args", []))
        elif op == "not":
            return not self._eval(node.get("arg", {}), data)
        elif op == "gte":
            return self._val(node["left"], data) >= self._val(node["right"], data)
        elif op == "lte":
            return self._val(node["left"], data) <= self._val(node["right"], data)
        elif op == "eq":
            return self._val(node["left"], data) == self._val(node["right"], data)
        elif op == "neq":
            return self._val(node["left"], data) != self._val(node["right"], data)
        elif op == "implies":
            antecedent = self._eval(node["left"], data)
            consequent = self._eval(node["right"], data)
            return (not antecedent) or consequent
        elif op == "in":
            val = self._val(node["value"], data)
            domain = node.get("domain", [])
            return val in domain
        else:
            return True  # Unknown ops pass through
```

---

## 8. The Bridge: GUARD → FLUX → PLATO

### 8.1 Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                     PLATO-NG GATE BRIDGE                          │
│                                                                   │
│    GUARD (.guard)                                                 │
│       │                                                           │
│       ▼                                                           │
│    guardc --emit-ir                                               │
│       │                                                           │
│       ▼                                                           │
│    ┌─────────────────┐    ┌───────────────────────────┐           │
│    │ guard_compiler.py│───▶│ Type system + constraints │           │
│    └─────────────────┘    │ (JSON IR)                 │           │
│                           └───────────┬───────────────┘           │
│                                       │                           │
│                    ┌──────────────────▼──────────────────┐        │
│                    │         P5 GATE ENGINE                │        │
│                    │                                      │        │
│                    │  ┌────────────┐  ┌───────────────┐  │        │
│                    │  │ constraint  │  │   constraint   │  │        │
│                    │  │ _eval.py   │  │   cache       │  │        │
│                    │  │ (tree walk) │  │ (LRU, 1024)   │  │        │
│                    │  └────────────┘  └───────────────┘  │        │
│                    └──────────────────┬──────────────────┘        │
│                                       │                           │
│                    ┌──────────────────▼──────────────────┐        │
│                    │       PLATO ROOM SERVER               │        │
│                    │                                      │        │
│                    │  HTTP POST /room/{name}/tile          │        │
│                    │  → P0-P4 pass → P5 pass → tile saved │        │
│                    └──────────────────────────────────────┘        │
│                                                                   │
│    OPTIMIZATION PATHS (Phase 2+):                                │
│    ┌────────────────┐   ┌────────────────┐   ┌──────────────┐    │
│    │ guardc --target │   │ FLUX Compiler  │   │ guardc Z3    │    │
│    │ c → dlopen .so  │   │ → flux-vm eval │   │ → SMT check │    │
│    │ (nanosecond)    │   │ (microsecond)  │   │ (stateful)   │    │
│    └────────────────┘   └────────────────┘   └──────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

### 8.2 Relationship to Existing Infrastructure

| Existing Component | Role in GUARD-Gate Bridge |
|--------------------|--------------------------|
| `guardc` (CLI) | GUARD → JSON IR compilation (primary path) |
| `guard_compiler` (crate) | Could serve as native lib instead of subprocess |
| FLUX IR / FIR | Intermediate format produced by `--emit-ir` |
| FLUX VM (Python/Rust/C) | Fast-path constraint evaluation (Phase 2) |
| `flux-runtime` (Python) | Potential PLATO integration host |
| `plato-room-server.py` | Target for P5 gate integration |
| Z3 / CVC5 | SMT-level checking for stateful/temporal constraints |

### 8.3 Key Design Decisions

**Decision 1: GUARD compilation happens at registration time, not at submit time.**
- Constraint is compiled once when registered
- JSON IR is cached in memory
- Every tile submission just evaluates the cached IR

**Decision 2: Multiple execution modes, single interface.**
- `P5ConstraintGate.validate(tile)` works identically regardless of backend
- Simplest mode (interpretive) needs no native compilation
- Hot path (native/FLUX-VM) drops latency by 100-1000x

**Decision 3: GUARD is the schema language, not a separate format.**
- No proto, no JSON Schema, no OpenAPI
- One constraint definition in .guard → serves as schema + validator + documentation
- Every tile type HAS a GUARD constraint, or it doesn't get validated

**Decision 4: Unknown tile types pass through (graceful degradation).**
- Migration path: existing tiles without type declarations pass P5 silently
- Only registered types get P5 validation
- No breaking change to existing PLATO clients

---

## 9. Performance Analysis

| Mode | Throughput (tiles/sec) | Latency | Depends On | Best For |
|------|----------------------|---------|------------|----------|
| Interpretive (Python) | ~50,000 | ~20µs | Nothing | MVP, dynamic constraints |
| Native (C .so) | ~5,000,000 | ~200ns | `guardc --target c` | Production, high volume |
| FLUX-VM (Python) | ~100,000 | ~10µs | flux-runtime | FLUX-native deployment |
| FLUX-VM (Rust) | ~2,000,000 | ~500ns | `flux` crate | Rust-native deployment |
| AVX-512 (asm) | ~38B/s vector | ~26ns | x86-64 AVX-512 | Batch validation |

**MVP bottleneck**: subprocess `guardc` call during registration (~100ms one-time cost). Submit-time validation is pure Python tree walk (~20µs).

---

## 10. Roadmap

### Phase 1 — MVP (Week 1)
- [ ] `guard_compiler.py` — subprocess guardc bridge + fallback simple parser
- [ ] `constraint_eval.py` — tree walker for AND/OR/NOT/IMPLIES/IN/RANGE
- [ ] `p5_constraint_gate.py` — P5 gate integrated into plato-room-server
- [ ] `registry.py` — tile type → constraint mapping with API endpoint
- [ ] `schemas/chess-move.guard` — working example
- [ ] Test: valid/invalid chess moves pass/fail correctly

### Phase 2 — Performance (Week 2)
- [ ] Native compilation path: `guardc --target c` → dlopen `.so`
- [ ] LRU constraint cache (1024 entries)
- [ ] FLUX-VM evaluation path (requires FLUX IR import)
- [ ] Benchmark: interpretive vs native vs flux-vm
- [ ] Batch tile validation (AVX-512 if available)

### Phase 3 — Stateful Validation (Week 3)
- [ ] Z3 integration for cross-tile constraints
- [ ] Temporal constraints: "move_number must increment by 1"
- [ ] Game-state constraints: "castle requires king-side rook unmoved"
- [ ] Achievement loss metric in P5 feedback

### Phase 4 — Fleet-Wide Schema Registry (Week 4)
- [ ] PLATO room stores GUARD constraints as tiles in `schemas/ room`
- [ ] Self-registering: agent declares type, submits `.guard` inline
- [ ] PLATO-to-PLATO schema federation
- [ ] `.guard` linting and constraint validation

---

## 11. Open Questions

1. **Who defines the GUARD schema?**
   - Agent that creates the tile type? Authority agent? Human?
   - Answer (provisional): The first agent to submit a tile of a given type must also submit a .guard constraint. If no .guard is provided, the tile is accepted through P5 passthrough.

2. **How does a tile reference its constraint?**
   - `tile["type"]` → looked up in registry
   - What if the type is unknown? → passthrough (graceful degradation)
   - What if a malicious agent spoofs a known type? → P5 still validates, constraint catches bad data

3. **Should GUARD constraints live in PLATO rooms or in files?**
   - Answer (provisional): Files during MVP (deterministic, no network dependency).
   - Phase 4: Store as tiles in `schemas/` room (federated, versioned).

4. **Can PLATO-NG run without guardc?**
   - Yes. The fallback parser (`_parse_guard_simple`) handles basic constraints.
   - Full compilation (nested constraints, enums, `IMPLIES`) requires guardc.

5. **What about constraint composition?**
   - A tile type should be able to reference multiple GUARD constraints.
   - Example: chess-move has both `valid_chess_move` and `valid_squares` constraints.
   - Solution: GUARD groups (`group chess_validations: { ... }`) map to PLATO constraint bundles.

---

## 12. Conclusion

The GUARD-as-Gate bridge is feasible with minimal infrastructure:

1. **GUARD → JSON IR** via `guardc --emit-ir` (existing guardc feature)
2. **JSON IR → Tree Walker** in pure Python (~100 lines)
3. **Tree Walker → Tile validation** via P5 gate inserted into gate pipeline
4. **Zero new dependencies** for MVP (guardc optional for basic constraints)

The bridge is **not a rewrite** — it's a compilation chain that plugs GUARD's existing output format into PLATO's existing gate pipeline. The GUARD constraint IS the schema, the validator, and the documentation, all in one `.guard` file.

**Latency budget:**
- Registration: ~100ms (one-time, subprocess guardc)
- Validation: ~20µs (interpretive) or ~200ns (native fallback)
- Incremental over current P0-P4: negligible

**Key insight:** PLATO already has P0-P4 as procedural checks. P5 as a GUARD constraint gate is not replacing them — it's adding schema-level validation that P0-P4 can't express. A chess-move tile needs `from != to` and `valid_square(from)` — P0-P4 can't know that. P5 with GUARD can.
