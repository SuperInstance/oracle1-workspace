"""
PLATO Training Rooms — Turn every PLATO room into a LoRA training lab.

Every adapter has lifecycle (Active/Superseded/Retracted).
Agents discover and compose adapters via PLATO rooms.
Simulation-first: predict before you train.
"""

from .types import (
    TrainingTile,
    TileType,
    TileLifecycle,
    LamportClock,
    TrainingConfig,
    AdapterConfig,
    TrainingMetrics,
)
from .rooms.base import TrainingRoom
from .rooms.lora_factory import LoRAFactory
from .adapters.lora import LoRALayer, inject_lora

__version__ = "0.1.0"
__all__ = [
    "TrainingTile",
    "TileType",
    "TileLifecycle",
    "LamportClock",
    "TrainingConfig",
    "AdapterConfig",
    "TrainingMetrics",
    "TrainingRoom",
    "LoRAFactory",
    "LoRALayer",
    "inject_lora",
]
