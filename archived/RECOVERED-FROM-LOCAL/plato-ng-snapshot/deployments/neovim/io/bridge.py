"""PLATO-native io/bridge room. Decomposed from neovim."""
import json, urllib.request, time
PLATO = "http://localhost:8847"
ROOM = "decomp/neovim/bridge"
def handle(method, path, body=None):
    if method == "GET":
        try:
            resp = json.loads(urllib.request.urlopen(f"{PLATO}/room/{ROOM}/history", timeout=5).read())
            tiles = resp.get("tiles", []) if isinstance(resp, dict) else resp
            return {"status": "ok", "tiles": len(tiles)}
        except: return {"status": "error"}
    elif method == "POST":
        tile = {"domain": "research_log", "question": f"{ROOM}/{path}",
                "answer": json.dumps(body or {}),
                "tags": ["decomp/neovim/bridge", "io"],
                "source": "decomp/neovim/bridge", "confidence": 0.99}
        try:
            data = json.dumps(tile).encode()
            urllib.request.urlopen(urllib.request.Request(f"{PLATO}/submit", data=data,
                headers={"Content-Type": "application/json"}), timeout=5)
            return {"status": "accepted"}
        except: return {"status": "error"}
