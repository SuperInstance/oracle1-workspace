#!/usr/bin/env python3
"""PLATO MCP Server — every PLATO room as an MCP tool.

MCP (Model Context Protocol) lets any MCP client (Claude Code, Cursor, Gemini CLI)
discover and call PLATO rooms as tools.

Protocol: JSON-RPC 2.0 over stdin/stdout
"""

import json, sys, urllib.request, time, os, re
from typing import Any

PLATO = os.environ.get("PLATO_URL", "http://localhost:8847")

# ── MCP Protocol Types ──

class MCPError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

def rpc_error(id: Any, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": id, "error": {"code": code, "message": message}}

def rpc_result(id: Any, result: Any) -> dict:
    return {"jsonrpc": "2.0", "id": id, "result": result}

# ── PLATO Room Discovery ──

def discover_rooms():
    """Discover all available PLATO rooms as MCP tools."""
    try:
        resp = json.loads(urllib.request.urlopen(f"{PLATO}/status", timeout=5).read())
    except:
        return []
    
    # Known rooms from our deployment
    tools = [
        {
            "name": "plato_status",
            "description": "Get PLATO server status — tile count, uptime",
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "plato_submit",
            "description": "Submit a tile to a PLATO room. Creates a new knowledge entry.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "domain": {"type": "string", "description": "Room/domain name"},
                    "question": {"type": "string", "description": "Tile question"},
                    "answer": {"type": "string", "description": "Tile answer/content"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["domain", "question", "answer"],
            },
        },
        {
            "name": "plato_read_room",
            "description": "Read recent tiles from a PLATO room. Get the room's current state.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "room": {"type": "string", "description": "Room name to read"},
                    "limit": {"type": "integer", "description": "Max tiles to return"},
                },
                "required": ["room"],
            },
        },
        {
            "name": "plato_search",
            "description": "Search PLATO tiles by query string or tags.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search text"},
                    "tag": {"type": "string", "description": "Filter by tag"},
                },
                "required": [],
            },
        },
        {
            "name": "plato_redis",
            "description": "PLATO-Redis key-value store. SET/GET/DEL keys.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "enum": ["SET", "GET", "DEL", "KEYS", "INCR", "DBSIZE"]},
                    "key": {"type": "string"},
                    "value": {"type": "string"},
                },
                "required": ["command"],
            },
        },
    ]
    return tools

# ── Tool Handlers ──

def plato_api(endpoint: str) -> dict:
    resp = json.loads(urllib.request.urlopen(f"{PLATO}/{endpoint}", timeout=10).read())
    return resp

def plato_post(data: dict) -> dict:
    req = urllib.request.Request(f"{PLATO}/submit", data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=10).read())

HANDLERS = {}

def tool(name: str):
    def decorator(f):
        HANDLERS[name] = f
        return f
    return decorator

@tool("plato_status")
def handle_status(args: dict) -> dict:
    resp = plato_api("status")
    return {"status": resp.get("status", "?"), "tiles": resp.get("tiles", resp.get("gate_stats", {}).get("accepted", 0))}

@tool("plato_submit")
def handle_submit(args: dict) -> dict:
    tile = {
        "domain": args.get("domain", "mcp"),
        "question": args.get("question", "mcp-tool-call"),
        "answer": args.get("answer", ""),
        "tags": args.get("tags", ["mcp", "tool-call"]),
        "source": "plato-mcp-server",
        "confidence": 0.95,
    }
    result = plato_post(tile)
    return {"status": result.get("status", "?"), "tile_count": result.get("tile_count", 0)}

@tool("plato_read_room")
def handle_read_room(args: dict) -> dict:
    room = args.get("room", "research_log")
    limit = args.get("limit", 10)
    try:
        resp = plato_api(f"room/{room}/history")
        tiles = resp.get("tiles", []) if isinstance(resp, dict) else resp
        return {"room": room, "tiles": tiles[-limit:]}
    except Exception as e:
        return {"error": str(e)}

@tool("plato_search")
def handle_search(args: dict) -> dict:
    query = args.get("query", "").lower()
    tag = args.get("tag", "")
    try:
        resp = plato_api("room/research_log/history")
        tiles = resp.get("tiles", []) if isinstance(resp, dict) else resp
        results = []
        for t in tiles:
            q = t.get("question", "").lower()
            a = t.get("answer", "").lower()
            tags = t.get("tags", [])
            if query and (query in q or query in a):
                results.append({"question": t.get("question","")[:80], "answer": t.get("answer","")[:120]})
            if tag and tag in tags:
                results.append({"question": t.get("question","")[:80], "answer": t.get("answer","")[:120]})
            if len(results) >= 10: break
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}

@tool("plato_redis")
def handle_redis(args: dict) -> dict:
    cmd = args.get("command", "").upper()
    key = args.get("key", "")
    value = args.get("value", "")
    
    store_file = "/tmp/plato-mcp-redis.json"
    store = {}
    try: store = json.load(open(store_file))
    except: pass
    
    if cmd == "GET":
        return {"value": store.get(key)}
    elif cmd == "SET" and key:
        store[key] = value
        json.dump(store, open(store_file, "w"))
        return {"status": "OK"}
    elif cmd == "DEL" and key:
        store.pop(key, None)
        json.dump(store, open(store_file, "w"))
        return {"deleted": True}
    elif cmd == "KEYS":
        pattern = key.replace("*", ".*") if key else ".*"
        matched = [k for k in store.keys() if re.match(f"^{pattern}$", k)]
        return {"keys": matched}
    elif cmd == "DBSIZE":
        return {"size": len(store)}
    elif cmd == "INCR" and key:
        cur = int(store.get(key, 0))
        store[key] = str(cur + 1)
        json.dump(store, open(store_file, "w"))
        return {"value": cur + 1}
    return {"error": f"unknown command: {cmd}"}

# ── MCP Request Handler ──

def handle_request(req: dict) -> dict:
    req_id = req.get("id", 0)
    method = req.get("method", "")
    params = req.get("params", {})
    
    if method == "initialize":
        return rpc_result(req_id, {
            "protocolVersion": "2025-03-26",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "plato-mcp-server", "version": "0.1.0"},
        })
    
    elif method == "listTools":
        return rpc_result(req_id, discover_rooms())
    
    elif method == "callTool":
        tool_name = params.get("name", "")
        tool_args = params.get("arguments", {})
        if tool_name in HANDLERS:
            try:
                result = HANDLERS[tool_name](tool_args)
                return rpc_result(req_id, {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]})
            except Exception as e:
                return rpc_error(req_id, -32603, str(e))
        return rpc_error(req_id, -32601, f"Tool not found: {tool_name}")
    
    elif method == "ping":
        return rpc_result(req_id, {})
    
    return rpc_error(req_id, -32601, f"Method not found: {method}")

# ── Main Loop ──

def main():
    print("PLATO MCP Server", file=sys.stderr)
    print(f"Connected to PLATO at {PLATO}", file=sys.stderr)
    print(f"Tools registered: {len(HANDLERS)}", file=sys.stderr)
    print("Listening on stdin/stdout...", file=sys.stderr)
    sys.stderr.flush()
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except json.JSONDecodeError:
            sys.stdout.write(json.dumps(rpc_error(0, -32700, "Parse error")) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
