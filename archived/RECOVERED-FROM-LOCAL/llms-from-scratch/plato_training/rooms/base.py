"""
Training Room — base class for PLATO training rooms.

Every room type inherits from this.
Rooms produce tiles, manage lifecycle, and integrate with PLATO v3.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from ..types import (
    TrainingTile,
    TileType,
    TileLifecycle,
    LamportClock,
    TrainingConfig,
)


class TrainingRoom(ABC):
    """
    Base class for a PLATO training room.
    
    A room is a self-contained training unit that:
    1. Reads input tiles from upstream rooms
    2. Performs training/computation
    3. Produces output tiles with lifecycle management
    4. Integrates with PLATO v3 for tile storage
    """
    
    def __init__(
        self,
        room_name: str,
        room_type: str,
        plato_host: str = "localhost",
        plato_port: int = 8847,
    ):
        self.room_name = room_name
        self.room_type = room_type
        self.plato_host = plato_host
        self.plato_port = plato_port
        
        self.clock = LamportClock()
        self.tiles: Dict[str, TrainingTile] = {}
        self.config: Optional[TrainingConfig] = None
    
    def create_tile(
        self,
        name: str,
        tile_type: TileType,
        description: str = "",
        **kwargs,
    ) -> TrainingTile:
        """Create a new tile in this room."""
        tile = TrainingTile(
            tile_id=f"{self.room_name}-{self.clock.tick()}",
            room=self.room_name,
            tile_type=tile_type,
            state=TileLifecycle.ACTIVE,
            lamport=self.clock.now(),
            name=name,
            description=description,
            source_room=self.room_name,
            **kwargs,
        )
        self.tiles[tile.tile_id] = tile
        return tile
    
    def get_active_tiles(self, tile_type: Optional[TileType] = None) -> List[TrainingTile]:
        """Get all active tiles, optionally filtered by type."""
        tiles = [t for t in self.tiles.values() if t.is_active()]
        if tile_type:
            tiles = [t for t in tiles if t.tile_type == tile_type]
        return sorted(tiles, key=lambda t: t.lamport)
    
    def supersede_tile(self, old_tile_id: str, new_tile: TrainingTile) -> Optional[TrainingTile]:
        """Supersede an old tile with a new one."""
        if old_tile_id not in self.tiles:
            return None
        old = self.tiles[old_tile_id]
        old.state = TileLifecycle.SUPERSEDED
        new_tile.parent_tile = old_tile_id
        new_tile.state = TileLifecycle.ACTIVE
        self.tiles[new_tile.tile_id] = new_tile
        return new_tile
    
    def retract_tile(self, tile_id: str, reason: str = "") -> bool:
        """Retract a tile."""
        if tile_id in self.tiles:
            self.tiles[tile_id].retract(reason)
            return True
        return False
    
    def lifecycle_stats(self) -> Dict[str, int]:
        """Count tiles by lifecycle state."""
        stats = {"active": 0, "superseded": 0, "retracted": 0}
        for tile in self.tiles.values():
            stats[tile.state.value] += 1
        return stats
    
    def summary(self) -> str:
        """Human-readable room summary."""
        stats = self.lifecycle_stats()
        return (
            f"[{self.room_type}] {self.room_name} — "
            f"active={stats['active']} superseded={stats['superseded']} "
            f"retracted={stats['retracted']} L{self.clock.now()}"
        )
    
    @abstractmethod
    def train(self, *args, **kwargs) -> TrainingTile:
        """Run training and produce an output tile."""
        ...
    
    @abstractmethod
    def evaluate(self, tile: TrainingTile) -> Dict[str, float]:
        """Evaluate a tile's quality."""
        ...
