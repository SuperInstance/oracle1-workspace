#!/usr/bin/env python3
"""
PLATO Decay Engine — Synaptic half-life for knowledge tiles.

Tiles lose energy over time. Frequently-used tiles get reinforced.
Dead tiles (energy < threshold) get archived.

Domain-specific half-lives:
  - Math/constraint theory: 365 days (math is forever)
  - Architecture/code: 90 days (code changes)
  - Fleet state: 7 days (ephemeral)
  - Model experiments: 30 days (configs shift)
  - Documentation: 180 days (semi-stable)
  - Default: 30 days

Run as a background thread or standalone cron.
"""

import json
import time
import threading
import hashlib
from pathlib import Path
from datetime import datetime, timezone

PLATO_DATA = Path("/tmp/plato-server-data")
ROOMS_DIR = PLATO_DATA / "rooms"
ARCHIVE_DIR = PLATO_DATA / "archive"
ARCHIVE_DIR.mkdir(exist_ok=True)

DECAY_INTERVAL = int(time.time())  # Run every hour

# Domain → half-life in days
DOMAIN_HALF_LIVES = {
    "constraint_theory": 365,
    "mathematics": 365,
    "ct_geometry": 365,
    "ct_holonomy": 365,
    "ct_farey": 365,
    "ct_proofs": 365,
    "pythagorean": 365,
    "codearchaeology": 90,
    "code_architecture": 90,
    "architecture": 90,
    "fleethealth": 7,
    "fleet_ops": 7,
    "fleet_state": 7,
    "modelexperiment": 30,
    "model_experiment": 30,
    "documentation": 180,
    "docs": 180,
}

DEFAULT_HALF_LIFE = 30  # days
DEATH_THRESHOLD = 0.05  # Energy below this → archive
REINFORCEMENT_BOOST = 0.3  # Per reinforcement


def get_half_life(tile: dict, room_name: str) -> float:
    """Determine half-life based on domain and room."""
    domain = tile.get("domain", "").lower()
    # Check domain first
    for key, hl in DOMAIN_HALF_LIVES.items():
        if key in domain or key in room_name.lower():
            return hl
    return DEFAULT_HALF_LIFE


def compute_energy(tile: dict, room_name: str, now: float) -> float:
    """Compute current energy of a tile based on age and reinforcements."""
    # Get tile age
    prov = tile.get("provenance", {})
    timestamp = prov.get("timestamp", now)
    if isinstance(timestamp, str):
        try:
            ts = datetime.fromisoformat(timestamp).timestamp()
        except:
            ts = now
    else:
        ts = timestamp if timestamp else now

    age_days = (now - ts) / 86400.0
    if age_days < 0:
        age_days = 0

    half_life = get_half_life(tile, room_name)

    # Exponential decay: energy = 2^(-age/half_life)
    decay = 2.0 ** (-age_days / half_life)

    # Reinforcement boost
    reinforcements = tile.get("reinforcement_count", 0)
    boost = 1.0 + reinforcements * REINFORCEMENT_BOOST

    energy = min(decay * boost, 2.0)  # Cap at 2x (super-reinforced)
    return round(energy, 6)


def reinforce_tile(tile: dict, reason: str = "search_hit") -> dict:
    """Reinforce a tile (called when it's consumed/useful)."""
    tile["reinforcement_count"] = tile.get("reinforcement_count", 0) + 1
    tile["last_reinforced"] = datetime.now(timezone.utc).isoformat()
    if "reinforced_by" not in tile:
        tile["reinforced_by"] = []
    tile["reinforced_by"].append({
        "reason": reason,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    return tile


def run_decay_cycle(dry_run: bool = False) -> dict:
    """
    Run one decay cycle across all rooms.
    Returns stats about what happened.
    """
    now = time.time()
    stats = {
        "rooms_scanned": 0,
        "tiles_scanned": 0,
        "tiles_updated": 0,
        "tiles_archived": 0,
        "tiles_reinforced": 0,
        "rooms_affected": [],
        "started": datetime.now(timezone.utc).isoformat(),
    }

    if not ROOMS_DIR.exists():
        stats["error"] = "No rooms directory"
        return stats

    for room_file in sorted(ROOMS_DIR.glob("*.json")):
        room_name = room_file.stem
        try:
            room = json.loads(room_file.read_text())
        except:
            continue

        tiles = room.get("tiles", [])
        if not tiles:
            continue

        stats["rooms_scanned"] += 1
        stats["tiles_scanned"] += len(tiles)

        alive = []
        dead = []
        updated = False

        for tile in tiles:
            # Ensure energy fields exist
            if "energy" not in tile:
                tile["energy"] = 1.0
                tile["reinforcement_count"] = 0
                updated = True

            # Compute current energy
            energy = compute_energy(tile, room_name, now)
            old_energy = tile.get("energy", 1.0)

            if abs(energy - old_energy) > 0.001:
                tile["energy"] = energy
                updated = True
                stats["tiles_updated"] += 1

            # Check if dead
            if energy < DEATH_THRESHOLD:
                tile["death_reason"] = "energy_decay"
                tile["died_at"] = datetime.now(timezone.utc).isoformat()
                dead.append(tile)
            else:
                alive.append(tile)

        if dead:
            stats["tiles_archived"] += len(dead)
            stats["rooms_affected"].append(room_name)

            # Archive dead tiles
            archive_file = ARCHIVE_DIR / f"{room_name}_dead.json"
            existing = []
            if archive_file.exists():
                try:
                    existing = json.loads(archive_file.read_text())
                except:
                    pass
            existing.extend(dead)

            if not dry_run:
                archive_file.write_text(json.dumps(existing, indent=2))

            # Update room with only alive tiles
            room["tiles"] = alive
            room["tile_count"] = len(alive)

        if updated and not dry_run:
            room_file.write_text(json.dumps(room, indent=2))

    stats["completed"] = datetime.now(timezone.utc).isoformat()
    return stats


class DecayEngine(threading.Thread):
    """Background decay engine — runs every hour."""

    def __init__(self, interval_seconds: int = 3600):
        super().__init__(daemon=True)
        self.interval = interval_seconds
        self.running = True
        self.last_run = None
        self.last_stats = None

    def run(self):
        while self.running:
            time.sleep(self.interval)
            self.last_stats = run_decay_cycle(dry_run=False)
            self.last_run = datetime.now(timezone.utc).isoformat()
            print(f"[DecayEngine] {self.last_stats['tiles_scanned']} scanned, "
                  f"{self.last_stats['tiles_archived']} archived")

    def stop(self):
        self.running = False


if __name__ == "__main__":
    import sys
    dry = "--dry-run" in sys.argv
    stats = run_decay_cycle(dry_run=dry)
    print(json.dumps(stats, indent=2))
