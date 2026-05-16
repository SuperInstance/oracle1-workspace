"""PLATO-native data/store room. Decomposed from clay."""
import json, urllib.request
PLATO = "http://localhost:8847"
ROOM = "decomp/clay/store"
store = {{}}
def handle(key, value=None):
    if value is not None:
        store[key] = value
        tile = {{"domain": "research_log", "question": f"{ROOM}/key/{{key}}",
                "answer": json.dumps({{"value": value}}),
                "tags": ["decomp/clay/store", "store", str(key)],
                "source": "decomp/clay/store", "confidence": 0.99}}
        try:
            data = json.dumps(tile).encode()
            urllib.request.urlopen(urllib.request.Request(f"{{PLATO}}/submit", data=data,
                headers={{"Content-Type": "application/json"}}), timeout=5)
        except: pass
        return "OK"
    return store.get(key)
def keys(): return list(store.keys())
def size(): return len(store)
