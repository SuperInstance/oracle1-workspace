"""
Equipment Layer — PLATO Room Server Client.
Shared across all services that read/write tiles.
Python 3.10, zero external dependencies.
"""
import hashlib
import hmac
import json
import os
import time
import urllib.request


class PlatoClient:
    """Client for PLATO Room Server (port 8847)."""
    
    def __init__(self, base_url="http://127.0.0.1:8847", secret=None):
        self.base_url = base_url
        self.secret = secret or os.environ.get("PLATO_SECRET", "cocapn-fleet-2024")
    
    def _sign(self, data):
        """HMAC-SHA256 sign tile data."""
        payload = json.dumps(data, sort_keys=True, default=str)
        return hmac.new(
            self.secret.encode(), payload.encode(), hashlib.sha256
        ).hexdigest()
    
    def _get(self, path):
        req = urllib.request.Request(f"{self.base_url}{path}")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read())
    
    def _post(self, path, data):
        body = json.dumps(data, default=str).encode()
        req = urllib.request.Request(
            f"{self.base_url}{path}", data=body, method="POST"
        )
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    
    # === Status ===
    def status(self):
        return self._get("/status")
    
    def tile_count(self):
        try:
            s = self.status()
            return s.get("total_tiles", 0)
        except:
            return 0
    
    # === Rooms ===
    def list_rooms(self):
        return self._get("/rooms")
    
    def get_room(self, name):
        try:
            return self._get(f"/rooms/{name}")
        except:
            return None
    
    def create_room(self, name, description="", domain="general"):
        return self._post("/rooms", {
            "name": name,
            "description": description,
            "domain": domain,
        })
    
    # === Tiles ===
    def get_tiles(self, room_name):
        room = self.get_room(room_name)
        if room:
            return room.get("tiles", [])
        return []
    
    def submit_tile(self, room_name, domain, question, answer, agent="fleet"):
        """Submit a tile to PLATO. Returns response or error."""
        tile = {
            "domain": domain,
            "question": question,
            "answer": answer,
            "agent": agent,
            "timestamp": time.time(),
        }
        tile["signature"] = self._sign(tile)
        try:
            return self._post("/submit", tile)
        except urllib.error.HTTPError as e:
            return {"error": str(e), "status": e.code}
    
    def search_tiles(self, query, room=None):
        """Search tiles across rooms."""
        path = f"/search?q={urllib.parse.quote(query)}"
        if room:
            path += f"&room={room}"
        return self._get(path)
    
    # === Batch ===
    def submit_batch(self, room_name, tiles, agent="fleet"):
        """Submit multiple tiles at once."""
        results = []
        for tile in tiles:
            r = self.submit_tile(
                room_name,
                tile.get("domain", "general"),
                tile.get("question", ""),
                tile.get("answer", ""),
                agent=agent,
            )
            results.append(r)
        return results


import urllib.parse  # needed for search_tiles
