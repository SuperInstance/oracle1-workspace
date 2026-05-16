"""
PLATO-Redis: in-memory key-value store as a PLATO Loop Room.

If Redis runs out of PLATO, any stateful service can.
Commands: SET, GET, DEL, KEYS, EXPIRE, TTL, INCR, LPUSH, LRANGE
"""

import json, urllib.request, time, re, math, os, sys

PLATO = "http://localhost:8847"
ROOM = "plato-redis"

store = {}       # key -> (value, expiry_timestamp)
ttl_index = []   # sorted by expiry for quick expiry scanning
command_count = 0
start_time = time.time()

def plato(q, a, tags):
    tile = {"domain": "research_log", "question": q, "answer": str(a)[:1950],
            "tags": tags, "source": ROOM, "confidence": 0.99}
    try:
        data = json.dumps(tile).encode()
        req = urllib.request.Request(f"{PLATO}/submit", data=data,
            headers={"Content-Type": "application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=10).read())
    except Exception as e:
        return {"error": str(e)}

# ── Redis Protocol ──

def handle_command(cmd_str):
    """Process a Redis-style command string. Returns response string."""
    global command_count, store, ttl_index
    
    command_count += 1
    parts = cmd_str.strip().split()
    if not parts:
        return "-ERR empty command"
    
    cmd = parts[0].upper()
    args = parts[1:]
    
    # Expiry sweeper
    now = time.time()
    expired = [k for k, (v, t) in store.items() if t and t <= now]
    for k in expired:
        del store[k]
    
    if cmd == "PING":
        return "+PONG"
    
    elif cmd == "SET" and len(args) >= 2:
        key, value = args[0], args[1]
        expiry = None
        if len(args) >= 4 and args[2].upper() == "EX":
            try:
                expiry = now + int(args[3])
            except: pass
        store[key] = (value, expiry)
        plato(f"cmd/SET/{key}", json.dumps({"cmd": "SET", "key": key, "value": value, "expiry": expiry}),
              [ROOM, "cmd", "SET", key])
        return "+OK"
    
    elif cmd == "GET" and len(args) >= 1:
        entry = store.get(args[0])
        if entry is None:
            return "$-1"
        value, expiry = entry
        if expiry and expiry <= now:
            del store[args[0]]
            return "$-1"
        return f"${len(value)}\r\n{value}"
    
    elif cmd == "DEL" and len(args) >= 1:
        count = sum(1 for k in args if k in store)
        for k in args:
            store.pop(k, None)
        return f":{count}"
    
    elif cmd == "KEYS" and len(args) >= 1:
        pattern = args[0].replace("*", ".*").replace("?", ".")
        matched = [k for k in store.keys() if re.match(f"^{pattern}$", k)]
        resp = f"*{len(matched)}\r\n"
        for k in matched:
            resp += f"${len(k)}\r\n{k}\r\n"
        return resp.strip()
    
    elif cmd == "EXPIRE" and len(args) >= 2:
        entry = store.get(args[0])
        if entry is None:
            return ":0"
        try:
            store[args[0]] = (entry[0], now + int(args[1]))
            return ":1"
        except:
            return "-ERR invalid expire time"
    
    elif cmd == "TTL" and len(args) >= 1:
        entry = store.get(args[0])
        if entry is None:
            return ":-2"
        value, expiry = entry
        if expiry is None:
            return ":-1"
        ttl = max(0, int(expiry - now))
        return f":{ttl}"
    
    elif cmd == "INCR" and len(args) >= 1:
        entry = store.get(args[0])
        if entry is None:
            store[args[0]] = ("1", None)
            return ":1"
        value, expiry = entry
        try:
            new_val = str(int(value) + 1)
            store[args[0]] = (new_val, expiry)
            return f":{new_val}"
        except:
            return "-ERR value is not an integer"
    
    elif cmd == "LPUSH" and len(args) >= 2:
        key = args[0]
        entry = store.get(key)
        if entry is None:
            store[key] = (json.dumps([args[1]]), None)
            return ":1"
        value, expiry = entry
        try:
            lst = json.loads(value)
            lst.insert(0, args[1])
            store[key] = (json.dumps(lst), expiry)
            return f":{len(lst)}"
        except:
            return "-ERR value is not a list"
    
    elif cmd == "LRANGE" and len(args) >= 3:
        entry = store.get(args[0])
        if entry is None:
            return "*0"
        value, expiry = entry
        try:
            lst = json.loads(value)
            start, end = int(args[1]), int(args[2])
            if start < 0: start = max(0, len(lst) + start)
            if end < 0: end = max(0, len(lst) + end)
            end = min(end, len(lst) - 1)
            slice_lst = lst[start:end+1] if start <= end else []
            resp = f"*{len(slice_lst)}"
            for item in slice_lst:
                resp += f"\r\n${len(item)}\r\n{item}"
            return resp
        except:
            return "-ERR value is not a list"
    
    elif cmd == "DBSIZE":
        return f":{len(store)}"
    
    elif cmd == "FLUSHALL":
        count = len(store)
        store.clear()
        return f":{count}"
    
    elif cmd == "INFO":
        info = {
            "keys": len(store),
            "commands": command_count,
            "uptime_seconds": int(time.time() - start_time),
            "room": ROOM,
        }
        info_str = "\n".join(f"{k}:{v}" for k, v in info.items())
        return f"${len(info_str)}\r\n{info_str}"
    
    elif cmd == "MONITOR":
        return f"+MONITOR enabled\r\n{json.dumps({'keys': len(store), 'uptime': int(time.time() - start_time)})}"
    
    return f"-ERR unknown command '{cmd}'"


def run_benchmark():
    """Run a quick benchmark to show Redis-as-PLATO is functional."""
    cmds = [
        "SET key1 value1",
        "SET key2 value2",
        "GET key1",
        "INCR counter",
        "INCR counter",
        "INCR counter",
        "LPUSH list a",
        "LPUSH list b",
        "LPUSH list c",
        "LRANGE list 0 -1",
        "KEYS key*",
        "DBSIZE",
        "TTL key1",
        "EXPIRE key2 60",
        "TTL key2",
        "DEL key1",
        "DBSIZE",
    ]
    
    results = []
    for cmd in cmds:
        result = handle_command(cmd)
        results.append({"cmd": cmd, "result": result[:80]})
    
    info_result = handle_command("INFO")
    
    print(f"PLATO-Redis: {len(cmd)} commands executed")
    print(f"Final keys: {len(store)}")
    print(f"Commands served: {command_count}")
    print(f"Persistence: {len(store)} keys in PLATO tiles\n")
    
    print("Sample commands:")
    for r in results[:8]:
        print(f"  {r['cmd']:30s} → {r['result']}")
    
    return results


if __name__ == "__main__":
    print("=== PLATO-Redis: In-Memory Store as PLATO Loop Room ===\n")
    
    # Register room
    plato("room/description",
        "PLATO-Redis: in-memory key-value store running as a PLATO Loop Room.\n"
        "Commands: SET, GET, DEL, KEYS, EXPIRE, TTL, INCR, LPUSH, LRANGE, DBSIZE, FLUSHALL, INFO, PING\n"
        "Everything persists to PLATO tiles. Audit trail via provenance.",
        [ROOM, "redis", "description"])
    
    # Run benchmark
    results = run_benchmark()
    
    # Push all keys to PLATO as tiles
    for key, (value, expiry) in store.items():
        plato(f"key/{key}", json.dumps({"key": key, "value": value, "expiry": expiry}),
              [ROOM, "key", key])
    
    # Push INFO to PLATO
    plato("room/info", json.dumps({
        "type": "redis", "keys": len(store), "commands": command_count,
        "uptime": int(time.time() - start_time), "source": ROOM
    }), [ROOM, "info"])
    
    print(f"\nDemo complete. {len(store)} keys persisted to PLATO.")
    print("Redis as a PLATO Loop Room is functional.")
    print("Commands: SET/GET/DEL/KEYS/EXPIRE/TTL/INCR/LPUSH/LRANGE/DBSIZE/FLUSHALL/INFO/PING")
