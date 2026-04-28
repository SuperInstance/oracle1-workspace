#!/usr/bin/env python3
"""
PLATO MCP Server — Exposes PLATO knowledge graph to any MCP-compatible agent.

Tools exposed:
  - plato_search: Semantic keyword search across all rooms
  - plato_get_room: Get tiles from a specific room
  - plato_list_rooms: List all rooms with tile counts
  - plato_submit: Submit a new tile to a room
  - plato_status: Server status, tile counts, gate stats
  - plato_trust: Trust scores for fleet agents
  - plato_recent: Recently submitted tiles

Transport: stdio (for MCP client spawning) or SSE on configurable port.
"""

import json
import sys
import os
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

PLATO_URL = os.environ.get("PLATO_URL", "http://localhost:8847")
MCP_PORT = int(os.environ.get("PLATO_MCP_PORT", "9500"))

# ── PLATO Client ──────────────────────────────────────────

class PlatoClient:
    """Thin client to the PLATO Room Server."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def _get(self, path: str) -> dict:
        req = urllib.request.Request(f"{self.base_url}{path}")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())

    def _post(self, path: str, data: dict) -> dict:
        body = json.dumps(data).encode()
        req = urllib.request.Request(
            f"{self.base_url}{path}",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())

    def status(self) -> dict:
        return self._get("/status")

    def rooms(self) -> dict:
        return self._get("/rooms")

    def get_room(self, name: str) -> dict:
        return self._get(f"/room/{name}")

    def search(self, query: str) -> dict:
        from urllib.parse import quote
        return self._get(f"/search?q={quote(query)}")

    def recent(self) -> dict:
        return self._get("/tiles/recent")

    def trust(self) -> dict:
        return self._get("/provenance/trust")

    def submit(self, tile: dict) -> dict:
        return self._post("/submit", tile)


plato = PlatoClient(PLATO_URL)

# ── MCP Tool Definitions ──────────────────────────────────

TOOLS = [
    {
        "name": "plato_search",
        "description": "Search PLATO knowledge graph for tiles matching a query. Returns up to 20 matching tiles across all rooms.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query to find relevant knowledge tiles"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "plato_get_room",
        "description": "Get all tiles from a specific PLATO room. Each tile has domain, question, answer, confidence, and provenance metadata.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "room": {
                    "type": "string",
                    "description": "Room name to retrieve tiles from"
                }
            },
            "required": ["room"]
        }
    },
    {
        "name": "plato_list_rooms",
        "description": "List all PLATO rooms with tile counts. Shows knowledge distribution across the fleet.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "plato_submit",
        "description": "Submit a new knowledge tile to PLATO. Must pass deadband gates (no absolute claims, answer >20 chars, proper fields).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "Knowledge domain (e.g. 'fleet_ops', 'constraint_theory', 'cuda')"
                },
                "question": {
                    "type": "string",
                    "description": "The question or topic this tile addresses"
                },
                "answer": {
                    "type": "string",
                    "description": "The knowledge or answer (20-5000 chars, no absolute claims)"
                },
                "room": {
                    "type": "string",
                    "description": "Target room name for the tile"
                },
                "confidence": {
                    "type": "number",
                    "description": "Confidence score 0.0-1.0 (default 0.5)",
                    "default": 0.5
                },
                "agent": {
                    "type": "string",
                    "description": "Submitting agent identifier",
                    "default": "mcp-client"
                }
            },
            "required": ["domain", "question", "answer", "room"]
        }
    },
    {
        "name": "plato_status",
        "description": "Get PLATO server status: total tiles, rooms, gate acceptance/rejection stats, uptime.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "plato_trust",
        "description": "Get trust scores for fleet agents based on tile submission history and quality.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "plato_recent",
        "description": "Get the 30 most recently submitted tiles across all rooms.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
]

# ── Tool Execution ────────────────────────────────────────

def execute_tool(name: str, args: dict) -> dict:
    """Execute a tool by name with the given arguments."""
    try:
        if name == "plato_search":
            results = plato.search(args["query"])
            count = len(results.get("results", []))
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps(results, indent=2)
                }],
                "meta": {"matches": count, "query": args["query"]}
            }

        elif name == "plato_get_room":
            room_data = plato.get_room(args["room"])
            tile_count = room_data.get("tile_count", 0)
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps(room_data, indent=2)
                }],
                "meta": {"room": args["room"], "tile_count": tile_count}
            }

        elif name == "plato_list_rooms":
            rooms = plato.rooms()
            # Summarize: top rooms by tile count
            if isinstance(rooms, dict):
                sorted_rooms = sorted(
                    rooms.items(),
                    key=lambda x: x[1].get("tile_count", 0) if isinstance(x[1], dict) else 0,
                    reverse=True,
                )
                summary = {
                    "total_rooms": len(sorted_rooms),
                    "total_tiles": sum(
                        v.get("tile_count", 0) if isinstance(v, dict) else 0
                        for _, v in sorted_rooms
                    ),
                    "top_rooms": [
                        {"name": k, "tiles": v.get("tile_count", 0) if isinstance(v, dict) else 0}
                        for k, v in sorted_rooms[:20]
                    ],
                }
            else:
                summary = {"rooms": rooms}
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps(summary, indent=2)
                }]
            }

        elif name == "plato_submit":
            tile = {
                "domain": args["domain"],
                "question": args["question"],
                "answer": args["answer"],
                "room": args["room"],
                "confidence": args.get("confidence", 0.5),
                "agent": args.get("agent", "mcp-client"),
            }
            result = plato.submit(tile)
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps(result, indent=2)
                }]
            }

        elif name == "plato_status":
            status = plato.status()
            summary = {
                "status": status.get("status"),
                "version": status.get("version"),
                "total_tiles": status.get("total_tiles"),
                "total_rooms": len(status.get("rooms", {})),
                "gate_stats": status.get("gate_stats"),
                "trust_entries": status.get("provenance", {}).get("trust_entries"),
            }
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps(summary, indent=2)
                }]
            }

        elif name == "plato_trust":
            trust = plato.trust()
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps(trust, indent=2)
                }]
            }

        elif name == "plato_recent":
            recent = plato.recent()
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps(recent, indent=2)
                }]
            }

        else:
            return {
                "content": [{"type": "text", "text": f"Unknown tool: {name}"}],
                "isError": True
            }

    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"Error: {str(e)}"}],
            "isError": True
        }


# ── MCP Protocol (stdio) ─────────────────────────────────

def handle_jsonrpc(request: dict) -> dict:
    """Handle a JSON-RPC 2.0 request."""
    method = request.get("method", "")
    req_id = request.get("id")
    params = request.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {"listChanged": False},
                },
                "serverInfo": {
                    "name": "plato-mcp-server",
                    "version": "1.0.0",
                },
            },
        }

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS},
        }

    elif method == "tools/call":
        tool_name = params.get("name", "")
        tool_args = params.get("arguments", {})
        result = execute_tool(tool_name, tool_args)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": result,
        }

    elif method == "notifications/initialized":
        # No response needed for notifications
        return None

    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        }


def run_stdio():
    """Run MCP server on stdio (for process-based MCP clients)."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_jsonrpc(request)
            if response is not None:
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
        except json.JSONDecodeError:
            sys.stdout.write(json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"},
            }) + "\n")
            sys.stdout.flush()


# ── MCP Protocol (SSE/HTTP) ───────────────────────────────

class MCPHTTPHandler(BaseHTTPRequestHandler):
    """HTTP+SSE transport for MCP protocol."""

    def do_POST(self):
        if self.path == "/mcp":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                request = json.loads(body)
                response = handle_jsonrpc(request)
                if response is not None:
                    self._send_json_response(response)
                else:
                    self._send_json_response({"jsonrpc": "2.0", "result": {}})
            except json.JSONDecodeError:
                self._send_json_response({
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Parse error"},
                }, 400)
        else:
            self._send_json_response({"error": "Not found"}, 404)

    def do_GET(self):
        if self.path == "/health":
            try:
                status = plato.status()
                self._send_json_response({
                    "mcp_server": "plato-mcp-server",
                    "version": "1.0.0",
                    "plato_status": status.get("status"),
                    "plato_tiles": status.get("total_tiles"),
                    "plato_rooms": len(status.get("rooms", {})),
                })
            except Exception as e:
                self._send_json_response({"status": "degraded", "error": str(e)})
        elif self.path == "/sse":
            # SSE endpoint for streaming MCP
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            # Keep alive — clients connect and send via POST
            self.wfile.write(b"data: {\"type\":\"connected\"}\n\n")
            self.wfile.flush()
        else:
            self._send_json_response({"error": "Not found"}, 404)

    def _send_json_response(self, data, code=200):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass  # Suppress access logs


def run_http():
    """Run MCP server as HTTP service."""
    server = HTTPServer(("0.0.0.0", MCP_PORT), MCPHTTPHandler)
    print(f"PLATO MCP Server on :{MCP_PORT} → {PLATO_URL}")
    print(f"Endpoints: POST /mcp | GET /health | GET /sse")
    server.serve_forever()


# ── Fleet Discovery Service ───────────────────────────────

import pathlib

CARDS_DIR = pathlib.Path(__file__).parent / "agent-cards"

class FleetDiscoveryHandler(BaseHTTPRequestHandler):
    """Serves A2A Agent Cards for fleet discovery."""

    def do_GET(self):
        if self.path == "/.well-known/agent-cards" or self.path == "/fleet/agents":
            # List all agents
            cards = []
            for f in sorted(CARDS_DIR.glob("*.json")):
                try:
                    cards.append(json.loads(f.read_text()))
                except:
                    pass
            self._json({"agents": cards, "fleet": "Cocapn", "count": len(cards)})
        elif self.path.startswith("/fleet/agent/"):
            name = self.path.split("/fleet/agent/")[1].split("?")[0]
            card_file = CARDS_DIR / f"{name}.json"
            if card_file.exists():
                self._json(json.loads(card_file.read_text()))
            else:
                self._json({"error": f"Agent '{name}' not found"}, 404)
        elif self.path == "/health":
            cards = len(list(CARDS_DIR.glob("*.json")))
            self._json({"service": "fleet-discovery", "agents": cards})
        else:
            self._json({"error": "Not found"}, 404)

    def _json(self, data, code=200):
        body = json.dumps(data, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


def run_discovery():
    """Run fleet discovery service."""
    server = HTTPServer(("0.0.0.0", 9501), FleetDiscoveryHandler)
    print(f"Fleet Discovery on :9501")
    server.serve_forever()


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "http"
    if mode == "stdio":
        run_stdio()
    elif mode == "discovery":
        run_discovery()
    elif mode == "all":
        # Run both MCP + discovery in threads
        t1 = threading.Thread(target=run_discovery, daemon=True)
        t1.start()
        run_http()  # Block on MCP
    elif mode == "http":
        run_http()
    else:
        run_http()
