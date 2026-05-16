"""Shared PLATO client — single source of truth for tile operations.
All services and game rooms import from here instead of duplicating code.
"""

import json, urllib.request, time, ssl, os

PLATO_URL = os.environ.get("PLATO_URL", "https://localhost:8847")
PLATO_API_KEY = os.environ.get("PLATO_API_KEY", "")

def _get_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def submit(domain, question, answer, tags=None, source="plato-client", confidence=0.95):
    """Submit a tile to PLATO. Returns status dict."""
    answer_str = answer if isinstance(answer, str) else json.dumps(answer)
    tile = {
        "domain": domain,
        "question": question,
        "answer": answer_str[:1950],
        "tags": tags or [],
        "source": source,
        "confidence": confidence,
    }
    try:
        data = json.dumps(tile).encode()
        headers = {"Content-Type": "application/json"}
        if PLATO_API_KEY:
            headers["Authorization"] = f"Bearer {PLATO_API_KEY}"
        req = urllib.request.Request(
            f"{PLATO_URL}/submit", data=data,
            headers=headers
        )
        resp = json.loads(urllib.request.urlopen(req, timeout=10, context=_get_ctx()).read())
        return resp.get("status", "?")
    except Exception as e:
        return f"err:{e}"

def read_room(room, limit=50):
    """Read tiles from a room. Returns list of tiles."""
    try:
        resp = json.loads(
            urllib.request.urlopen(f"{PLATO_URL}/room/{room}/history", timeout=10).read()
        )
        tiles = resp.get("tiles", []) if isinstance(resp, dict) else resp
        return tiles[-limit:]
    except:
        return []

def status():
    """Get PLATO server status."""
    try:
        headers = {}
        if PLATO_API_KEY:
            headers["Authorization"] = f"Bearer {PLATO_API_KEY}"
        req = urllib.request.Request(f"{PLATO_URL}/status", headers=headers)
        resp = json.loads(
            urllib.request.urlopen(req, timeout=5, context=_get_ctx()).read()
        )
        return resp
    except Exception as e:
        return {"status": "unreachable", "error": str(e)[:60]}

def submit_result(room, result_dict, result_type, tags=None):
    """Submit a tournament/game result with standard format."""
    return submit(
        "research_log",
        f"{room}/{result_type}",
        json.dumps(result_dict),
        tags=tags,
        source=room.replace("/", "-"),
    )
