"""
Core types for PLATO Training Rooms.

Every training artifact is a tile with lifecycle.
Adapters aren't files — they're tiles in PLATO rooms.
"""

from __future__ import annotations
import json
import time
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, Dict, Any, List


class TileType(Enum):
    """What kind of training artifact this tile represents."""
    DATASET = "dataset"
    ARCHITECTURE = "architecture"
    CHECKPOINT = "checkpoint"
    ADAPTER = "adapter"
    METRICS = "metrics"
    EVALUATION = "evaluation"
    PREDICTION = "prediction"


class TileLifecycle(Enum):
    """PLATO v3 tile lifecycle states."""
    ACTIVE = "active"
    SUPERSEDED = "superseded"
    RETRACTED = "retracted"


class LamportClock:
    """Causal ordering for distributed training rooms."""
    
    def __init__(self, time: int = 0):
        self.time = time
    
    def tick(self) -> int:
        self.time += 1
        return self.time
    
    def merge(self, remote: int) -> int:
        self.time = max(self.time, remote) + 1
        return self.time
    
    def now(self) -> int:
        return self.time


@dataclass
class AdapterConfig:
    """LoRA adapter configuration."""
    rank: int = 8
    alpha: int = 16
    target_modules: List[str] = field(default_factory=lambda: ["W_query", "W_value"])
    dropout: float = 0.0
    # Higher rank = more capacity but more parameters
    # rank=8 for classification, rank=32 for generation
    # alpha=2*rank is "aggressive" (good for domain shift)
    # alpha=rank is "conservative" (good for minor adjustment)


@dataclass
class TrainingConfig:
    """Training hyperparameters."""
    learning_rate: float = 2e-4
    weight_decay: float = 0.01
    epochs: int = 3
    batch_size: int = 8
    eval_interval: int = 100
    warmup_steps: int = 100
    max_grad_norm: float = 1.0
    gradient_accumulation: int = 1
    scheduler: str = "cosine"  # cosine, linear, constant


@dataclass
class TrainingMetrics:
    """Training run metrics — stored as a tile."""
    train_loss: float = 0.0
    val_loss: float = 0.0
    train_accuracy: float = 0.0
    val_accuracy: float = 0.0
    epochs_completed: int = 0
    training_time_seconds: float = 0.0
    peak_memory_mb: float = 0.0
    final_loss: float = 0.0


@dataclass
class TrainingTile:
    """
    A training artifact stored in a PLATO room.
    
    This is the fundamental unit — every dataset, adapter, checkpoint,
    and evaluation result is a TrainingTile with lifecycle management.
    """
    tile_id: str = ""
    room: str = ""
    tile_type: TileType = TileType.ADAPTER
    state: TileLifecycle = TileLifecycle.ACTIVE
    lamport: int = 0
    
    # Content
    name: str = ""
    description: str = ""
    data_path: Optional[str] = None  # Path to actual weights/data on disk
    
    # Training metadata
    base_model: str = ""
    adapter_config: Optional[AdapterConfig] = None
    training_config: Optional[TrainingConfig] = None
    metrics: Optional[TrainingMetrics] = None
    
    # Provenance
    source_room: str = ""  # Which room produced this tile
    parent_tile: str = ""  # Tile this was derived from
    timestamp: float = field(default_factory=time.time)
    
    # PLATO integration
    plato_room_id: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary for PLATO storage."""
        d = asdict(self)
        d["tile_type"] = self.tile_type.value
        d["state"] = self.state.value
        return d
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TrainingTile":
        """Deserialize from PLATO storage."""
        d["tile_type"] = TileType(d["tile_type"])
        d["state"] = TileLifecycle(d["state"])
        if d.get("adapter_config") and isinstance(d["adapter_config"], dict):
            d["adapter_config"] = AdapterConfig(**d["adapter_config"])
        if d.get("training_config") and isinstance(d["training_config"], dict):
            d["training_config"] = TrainingConfig(**d["training_config"])
        if d.get("metrics") and isinstance(d["metrics"], dict):
            d["metrics"] = TrainingMetrics(**d["metrics"])
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
    
    def supersede(self, new_tile: "TrainingTile") -> "TrainingTile":
        """Mark this tile as superseded by new_tile."""
        self.state = TileLifecycle.SUPERSEDED
        new_tile.parent_tile = self.tile_id
        new_tile.state = TileLifecycle.ACTIVE
        return new_tile
    
    def retract(self, reason: str = "") -> None:
        """Retract this tile."""
        self.state = TileLifecycle.RETRACTED
        self.description = f"RETRACTED: {reason}. Original: {self.description}"
    
    def is_active(self) -> bool:
        return self.state == TileLifecycle.ACTIVE
    
    def summary(self) -> str:
        """Human-readable tile summary."""
        return (
            f"[{self.tile_type.value.upper()}] {self.name} "
            f"({self.state.value}, L{self.lamport}) "
            f"base={self.base_model}"
        )
