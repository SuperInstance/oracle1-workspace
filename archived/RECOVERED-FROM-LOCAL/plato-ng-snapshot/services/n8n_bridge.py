#!/usr/bin/env python3
"""
n8n Bridge — PLATO Loop Rooms as n8n visual workflow nodes.

Exposes PLATO rooms as n8n node types with tile-based I/O.
Supports: game rooms, memory, Crush, Aider, Redis, Governance, Conservation.

Usage:
  from services.n8n_bridge import PlatoNode, register_nodes, get_node_definitions
  nodes = get_node_definitions()

n8n node structure:
  - Each room = one node type
  - Inputs: domain, question, answer, tags (PLATO tile fields)
  - Outputs: processed tile result
  - Credentials: PLATO API key (stored securely in n8n credential store)
"""

import json, time, hashlib
from typing import Any, Optional

# ── Node Registry ──────────────────────────────────────────────────────────────

class PlatoNodeRegistry:
    """Registry of all PLATO room nodes for n8n."""

    def __init__(self):
        self.nodes: dict[str, dict] = {}
        self._register_builtin_nodes()

    def _register_builtin_nodes(self):
        """Register all PLATO room nodes."""
        nodes = [
            # ── Game Rooms ────────────────────────────────────────────────
            NodeDefinition(
                name="plato_tic_tac_toe",
                display_name="PLATO Tic-Tac-Toe",
                description="Play tic-tac-toe against algorithmic strategies. Submits moves as tiles.",
                icon="🎮",
                category="games",
                inputs=[
                    InputField("move", "Move", "number", required=True,
                               description="Cell index 0-8 (top-left=0, bottom-right=8)"),
                    InputField("strategy", "Strategy", "string", required=False,
                               description="Strategy: aggressive, defensive, random, minimax"),
                ],
                outputs=[
                    OutputField("board", "Board State", "string",
                                description="Current board as ASCII art"),
                    OutputField("result", "Game Result", "string",
                                description="win/lose/tie/in_progress"),
                    OutputField("opponent_move", "Opponent Move", "number",
                                description="Cell index of opponent's move"),
                ],
                credentials=["plato_api_key"],
                properties={
                    "room": "game/tic-tac-toe",
                    "game_type": "ttt",
                }
            ),

            NodeDefinition(
                name="plato_othello",
                display_name="PLATO Othello",
                description="Play Othello/Reversi against algorithmic strategies.",
                icon="◉",
                category="games",
                inputs=[
                    InputField("move", "Move", "string", required=True,
                               description="Cell index (e.g., 'D3') or 'pass'"),
                    InputField("strategy", "Strategy", "string", required=False,
                               description="Strategy: aggressive, defensive, random, minimax"),
                ],
                outputs=[
                    OutputField("board", "Board State", "string"),
                    OutputField("result", "Game Result", "string"),
                    OutputField("opponent_move", "Opponent Move", "string"),
                    OutputField("score", "Score", "object",
                                description="{'black': n, 'white': n}"),
                ],
                credentials=["plato_api_key"],
                properties={"room": "game/othello", "game_type": "othello"}
            ),

            # ── Agent Rooms ──────────────────────────────────────────────
            NodeDefinition(
                name="plato_crush",
                display_name="PLATO Crush Room",
                description="Submit code analysis tasks to Crush (code intelligence). "
                            "Crush processes tasks and returns results as tiles.",
                icon="🔨",
                category="agents",
                inputs=[
                    InputField("task", "Task", "string", required=True,
                               description="Code analysis task (e.g., 'analyze /path/to/file for bugs')"),
                    InputField("context", "Context", "string", required=False,
                               description="Additional context for the analysis"),
                ],
                outputs=[
                    OutputField("result", "Result", "string",
                                description="Crush analysis result"),
                    OutputField("error", "Error", "string",
                                description="Error message if task failed"),
                    OutputField("tick", "Tick", "number",
                                description="Crush daemon tick number"),
                ],
                credentials=["plato_api_key"],
                properties={
                    "room": "research_log",
                    "question_prefix": "crush/task",
                    "result_question_prefix": "crush/ok",
                }
            ),

            NodeDefinition(
                name="plato_aider",
                display_name="PLATO Aider Room",
                description="Submit code refactoring/editing tasks to Aider (AI coding assistant). "
                            "Aider edits code and returns results as tiles.",
                icon="✏️",
                category="agents",
                inputs=[
                    InputField("task", "Task", "string", required=True,
                               description="Code task (e.g., 'refactor function foo in /path/to/file')"),
                    InputField("repo", "Repo Path", "string", required=False,
                               description="Path to repository for lint/format checks"),
                ],
                outputs=[
                    OutputField("output", "Output", "string",
                                description="Aider edit output"),
                    OutputField("error", "Error", "string",
                                description="Error message if task failed"),
                ],
                credentials=["plato_api_key"],
                properties={
                    "room": "research_log",
                    "question_prefix": "aider/task",
                    "result_question_prefix": "aider/ok",
                }
            ),

            NodeDefinition(
                name="plato_openhands",
                display_name="PLATO OpenHands Room",
                description="Submit complex coding tasks to OpenHands (autonomous coding agent). "
                            "Handles multi-file refactoring, bug fixes, feature implementation.",
                icon="🤖",
                category="agents",
                inputs=[
                    InputField("task", "Task", "string", required=True,
                               description="Complex coding task description"),
                    InputField("workspace", "Workspace", "string", required=False,
                               description="Working directory for the task"),
                ],
                outputs=[
                    OutputField("result", "Result", "string",
                                description="OpenHands execution result"),
                    OutputField("files_changed", "Files Changed", "array",
                                description="List of files modified"),
                    OutputField("error", "Error", "string",
                                description="Error message if task failed"),
                ],
                credentials=["plato_api_key"],
                properties={
                    "room": "research_log",
                    "question_prefix": "openhands/task",
                    "result_question_prefix": "openhands/ok",
                }
            ),

            # ── Memory ───────────────────────────────────────────────────
            NodeDefinition(
                name="plato_memory",
                display_name="PLATO Memory",
                description="Store and retrieve agent twin memories. "
                            "Uses Ebbinghaus decay curve for retention tracking.",
                icon="💎",
                category="memory",
                inputs=[
                    InputField("operation", "Operation", "string", required=True,
                               description="Operation: crystallize, recall, search, forget"),
                    InputField("content", "Content", "string", required=False,
                               description="Content to store (for crystallize) or query (for search/recall)"),
                    InputField("mem_id", "Memory ID", "string", required=False,
                               description="Memory ID for recall operation"),
                    InputField("valence", "Valence", "number", required=False,
                               description="Emotional salience 0.0-1.0 (default 0.5)"),
                    InputField("tags", "Tags", "array", required=False,
                               description="Tags for the memory"),
                ],
                outputs=[
                    OutputField("mem_id", "Memory ID", "string",
                                description="ID of the stored/retrieved memory"),
                    OutputField("reconstruction", "Reconstruction", "string",
                                description="Recalled memory content (may be lossy)"),
                    OutputField("confidence", "Confidence", "number",
                                description="Recall confidence 0.0-1.0"),
                    OutputField("retention", "Retention", "number",
                                description="Current retention level 0.0-1.0"),
                    OutputField("stats", "Stats", "object",
                                description="Memory crystal statistics"),
                ],
                credentials=["plato_api_key"],
                properties={"room": "research_log", "module": "agent-twin"}
            ),

            # ── Governance ───────────────────────────────────────────────
            NodeDefinition(
                name="plato_governance",
                display_name="PLATO Governance",
                description="Check permissions, roles, and policy compliance. "
                            "Auth/Governance Layer for PLATO-NG.",
                icon="🛡️",
                category="governance",
                inputs=[
                    InputField("operation", "Operation", "string", required=True,
                               description="Operation: check_permission, allowed_actions, get_roles, get_policies"),
                    InputField("role", "Role", "string", required=False,
                               description="Role: human, agent, refiner, observer"),
                    InputField("room", "Room", "string", required=False,
                               description="Room name (e.g., 'game/ttt', 'loop/refiner')"),
                    InputField("action", "Action", "string", required=False,
                               description="Action to check (e.g., 'play', 'pause', 'override')"),
                ],
                outputs=[
                    OutputField("allowed", "Allowed", "boolean",
                                description="True if role can perform action"),
                    OutputField("actions", "Allowed Actions", "array",
                                description="List of all allowed actions for role/room"),
                    OutputField("roles", "Roles", "object",
                                description="All defined roles and descriptions"),
                    OutputField("policies", "Policies", "object",
                                description="All policies for the room"),
                ],
                credentials=["plato_api_key"],
                properties={"room": "gov/main", "module": "governance"}
            ),

            # ── Conservation ─────────────────────────────────────────────
            NodeDefinition(
                name="plato_conservation",
                display_name="PLATO Conservation Monitor",
                description="Check conservation law compliance (gamma/H/V spectral norms). "
                            "Flags violations, tracks drift, feeds back to Refiner.",
                icon="⚖️",
                category="governance",
                inputs=[
                    InputField("tiles", "Tiles", "array", required=False,
                               description="Tiles to check (auto-fetches from PLATO if empty)"),
                    InputField("room", "Room", "string", required=False,
                               description="PLATO room to check (default: all monitored rooms)"),
                ],
                outputs=[
                    OutputField("violations", "Violations", "array",
                                description="List of conservation law violations found"),
                    OutputField("compliance_rate", "Compliance Rate", "string",
                                description="Percentage compliance (e.g., '99.7%')"),
                    OutputField("status", "Status", "string",
                                description="HEALTHY or DEGRADED"),
                    OutputField("checks", "Total Checks", "number",
                                description="Total number of tiles checked"),
                ],
                credentials=["plato_api_key"],
                properties={"room": "research_log", "module": "conservation"}
            ),

            # ── Redis ────────────────────────────────────────────────────
            NodeDefinition(
                name="plato_redis",
                display_name="PLATO Redis",
                description="PLATO tile caching and pub/sub via Redis. "
                            "Fast tile storage and room pub/sub.",
                icon="📡",
                category="infrastructure",
                inputs=[
                    InputField("operation", "Operation", "string", required=True,
                               description="Operation: get, set, delete, publish, subscribe"),
                    InputField("key", "Key", "string", required=False,
                               description="Redis key"),
                    InputField("value", "Value", "string", required=False,
                               description="Value to set"),
                    InputField("channel", "Channel", "string", required=False,
                               description="Pub/sub channel"),
                    InputField("ttl", "TTL", "number", required=False,
                               description="Time to live in seconds"),
                ],
                outputs=[
                    OutputField("value", "Value", "string",
                                description="Retrieved value"),
                    OutputField("result", "Result", "string",
                                description="Operation result"),
                ],
                credentials=["plato_api_key"],
                properties={"room": "event-bus", "module": "redis"}
            ),

            # ── MUD ──────────────────────────────────────────────────────
            NodeDefinition(
                name="plato_mud",
                display_name="PLATO MUD Bridge",
                description="PLATO MUD telnet server — text adventure room. "
                            "Navigate, interact, explore.",
                icon="🏰",
                category="games",
                inputs=[
                    InputField("command", "Command", "string", required=True,
                               description="MUD command (look, go north, take item, say, etc.)"),
                    InputField("session_id", "Session ID", "string", required=False,
                               description="MUD session ID (auto-creates if empty)"),
                ],
                outputs=[
                    OutputField("response", "Response", "string",
                                description="MUD server response"),
                    OutputField("session_id", "Session ID", "string",
                                description="Session ID for continued interaction"),
                    OutputField("location", "Location", "string",
                                description="Current room description"),
                ],
                credentials=["plato_api_key"],
                properties={"room": "game/mud", "module": "mud-telnet"}
            ),

            # ── MCP Server ──────────────────────────────────────────────
            NodeDefinition(
                name="plato_mcp",
                display_name="PLATO MCP Server",
                description="Model Context Protocol server for tool exposure. "
                            "Exposes PLATO capabilities as MCP tools.",
                icon="🔌",
                category="infrastructure",
                inputs=[
                    InputField("tool", "Tool Name", "string", required=True,
                               description="MCP tool to call"),
                    InputField("args", "Arguments", "object", required=False,
                               description="Tool arguments"),
                ],
                outputs=[
                    OutputField("result", "Result", "object",
                                description="MCP tool result"),
                    OutputField("error", "Error", "string",
                                description="Error if tool failed"),
                ],
                credentials=["plato_api_key"],
                properties={"room": "event-bus", "module": "mcp"}
            ),

            # ── Event Bus ───────────────────────────────────────────────
            NodeDefinition(
                name="plato_event_bus",
                display_name="PLATO Event Bus",
                description="PLATO pub/sub event bus. Publish events, subscribe to room streams.",
                icon="📻",
                category="infrastructure",
                inputs=[
                    InputField("operation", "Operation", "string", required=True,
                               description="Operation: publish, subscribe, unsubscribe"),
                    InputField("room", "Room", "string", required=True,
                               description="PLATO room name"),
                    InputField("event", "Event", "object", required=False,
                               description="Event to publish (tile structure)"),
                ],
                outputs=[
                    OutputField("published", "Published", "boolean",
                                description="True if event was published"),
                    OutputField("subscribers", "Subscribers", "number",
                                description="Number of subscribers to the room"),
                    OutputField("event_id", "Event ID", "string",
                                description="ID of published event"),
                ],
                credentials=["plato_api_key"],
                properties={"room": "event-bus", "module": "pubsub"}
            ),
        ]

        for node in nodes:
            self.nodes[node.name] = node.to_n8n_spec()

    def get_node_definitions(self) -> list[dict]:
        """Get all node definitions in n8n format."""
        return list(self.nodes.values())

    def get_node(self, name: str) -> Optional[dict]:
        """Get a specific node definition."""
        return self.nodes.get(name)

    def register_custom_node(self, node_def: "NodeDefinition"):
        """Register a custom node."""
        self.nodes[node_def.name] = node_def.to_n8n_spec()


# ── Node Definition Builder ────────────────────────────────────────────────────

class NodeDefinition:
    """Represents an n8n node for a PLATO room."""

    def __init__(
        self,
        name: str,
        display_name: str,
        description: str,
        icon: str = "📦",
        category: str = "general",
        inputs: list = None,
        outputs: list = None,
        credentials: list = None,
        properties: dict = None,
    ):
        self.name = name
        self.display_name = display_name
        self.description = description
        self.icon = icon
        self.category = category
        self.inputs = inputs or []
        self.outputs = outputs or []
        self.credentials = credentials or []
        self.properties = properties or {}

    def to_n8n_spec(self) -> dict:
        """Convert to n8n node specification format."""
        return {
            "name": self.display_name,
            "codeName": self.name,
            "icon": self.icon,
            "group": ["input", "output"],
            "displayName": self.display_name,
            "description": self.description,
            "category": self.category,
            "subcategories": {"workflow": ["condition"]},
            "properties": [
                *self._build_inputs_section(),
                *self._build_outputs_section(),
                *self._build_config_section(),
            ],
            "credentials": self.credentials,
            "version": 1,
            "defaults": {"name": self.display_name},
            "inputs": ["main"],
            "outputs": ["main"],
        }

    def _build_inputs_section(self) -> list:
        """Build input property fields."""
        fields = []
        for inp in self.inputs:
            fields.append({
                "id": f"input_{inp.name}",
                "displayName": inp.label,
                "name": inp.name,
                "type": inp.type,
                "required": inp.required,
                "default": "",
                "description": inp.description,
                "displayOptions": {
                    "show": {}
                },
            })
        return fields

    def _build_outputs_section(self) -> list:
        """Build output configuration fields."""
        return [{
            "id": f"output_{o.name}",
            "displayName": o.label,
            "name": o.name,
            "type": o.type,
            "required": False,
            "description": o.description,
        } for o in self.outputs]

    def _build_config_section(self) -> list:
        """Build configuration properties."""
        return [{
            "id": f"config_{k}",
            "displayName": k.replace("_", " ").title(),
            "name": k,
            "type": "string",
            "required": False,
            "default": str(v),
            "description": f"Room configuration: {k}",
        } for k, v in self.properties.items()]


# ── Field Definitions ──────────────────────────────────────────────────────────

class InputField:
    def __init__(self, name: str, label: str, type: str, required: bool, description: str = ""):
        self.name = name
        self.label = label
        self.type = type
        self.required = required
        self.description = description


class OutputField:
    def __init__(self, name: str, label: str, type: str, description: str = ""):
        self.name = name
        self.label = label
        self.type = type
        self.description = description


# ── PLATO Bridge Client ────────────────────────────────────────────────────────

class PlatoBridgeClient:
    """Client for PLATO tile operations via n8n nodes."""

    def __init__(self, base_url: str = "http://localhost:8847", api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key or ""

    def submit_tile(
        self,
        domain: str,
        question: str,
        answer: str,
        tags: list = None,
        source: str = "n8n",
        confidence: float = 0.9,
    ) -> dict:
        """Submit a tile to PLATO."""
        import urllib.request
        tile = {
            "domain": domain,
            "question": question,
            "answer": str(answer)[:1950],
            "tags": tags or ["n8n"],
            "source": source,
            "confidence": confidence,
        }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            data = json.dumps(tile).encode()
            req = urllib.request.Request(
                f"{self.base_url}/submit",
                data=data,
                headers=headers
            )
            resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
            return {"success": True, "tile": resp}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_room_history(self, domain: str, limit: int = 50) -> list:
        """Get room tile history."""
        import urllib.request
        try:
            req = urllib.request.Request(
                f"{self.base_url}/room/{domain}/history?limit={limit}"
            )
            resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
            tiles = resp.get("tiles", []) if isinstance(resp, dict) else resp
            return tiles
        except Exception as e:
            return []

    def poll_for_result(self, domain: str, question_prefix: str, timeout: int = 60) -> dict:
        """Poll for a result tile matching question prefix."""
        import time, urllib.request
        deadline = time.time() + timeout

        while time.time() < deadline:
            tiles = self.get_room_history(domain, limit=20)
            for tile in reversed(tiles):
                q = tile.get("question", "")
                if q.startswith(question_prefix):
                    return {"success": True, "tile": tile}
            time.sleep(2)

        return {"success": False, "error": "timeout"}


# ── Credential Management ──────────────────────────────────────────────────────

class PlatoCredential:
    """n8n credential object for PLATO API key."""

    def __init__(self, id: str = None, api_key: str = ""):
        self.id = id or hashlib.md5(str(time.time()).encode()).hexdigest()[:12]
        self.api_key = api_key

    def to_n8n_credential(self) -> dict:
        """Export as n8n credential format."""
        return {
            "id": self.id,
            "name": "PLATO API Key",
            "type": "platoApiKey",
            "data": {
                "apiKey": self.api_key,
            }
        }

    @staticmethod
    def from_n8n_credential(cred_data: dict) -> "PlatoCredential":
        """Import from n8n credential data."""
        return PlatoCredential(
            id=cred_data.get("id"),
            api_key=cred_data.get("data", {}).get("apiKey", "")
        )


# ── Workflow Templates ─────────────────────────────────────────────────────────

def get_crush_analyze_then_aider_fix_template() -> dict:
    """Template: Crush analyzes code → Aider fixes it."""
    return {
        "name": "Crush Analyze → Aider Fix",
        "description": "Submit code to Crush for analysis. If issues found, route to Aider for fixes.",
        "nodes": [
            {
                "name": "PLATO Crush",
                "type": "plato_crush",
                "position": [250, 300],
                "parameters": {
                    "task": "={{$json.code}}",
                    "context": "={{$json.context}}"
                },
                "inputs": ["main"],
                "outputs": ["main"],
            },
            {
                "name": "Check Issues",
                "type": "plato_conservation",
                "position": [500, 300],
                "parameters": {
                    "tiles": "={{$json.tiles}}"
                },
                "inputs": ["main"],
                "outputs": ["main"],
            },
            {
                "name": "PLATO Aider",
                "type": "plato_aider",
                "position": [750, 300],
                "parameters": {
                    "task": "={{$json.fix_task}}",
                    "repo": "={{$json.repo_path}}"
                },
                "inputs": ["main"],
                "outputs": ["main"],
            },
        ],
        "connections": {
            "PLATO Crush": {
                "main": [["Check Issues", "main"]]
            },
            "Check Issues": {
                "main": [["PLATO Aider", "main"]]
            }
        },
    }


def get_game_tournament_memory_template() -> dict:
    """Template: Run game tournament, store results in memory."""
    return {
        "name": "Game Tournament → Memory",
        "description": "Run tic-tac-toe tournament between agents, store results in PLATO memory.",
        "nodes": [
            {
                "name": "PLATO Tic-Tac-Toe",
                "type": "plato_tic_tac_toe",
                "position": [250, 200],
                "parameters": {
                    "strategy": "aggressive"
                },
                "inputs": ["main"],
                "outputs": ["main"],
            },
            {
                "name": "Record Move",
                "type": "plato_memory",
                "position": [500, 200],
                "parameters": {
                    "operation": "crystallize",
                    "content": "={{$json.board}}",
                    "valence": 0.7,
                    "tags": ["game", "tournament"]
                },
                "inputs": ["main"],
                "outputs": ["main"],
            },
        ],
        "connections": {
            "PLATO Tic-Tac-Toe": {
                "main": [["Record Move", "main"]]
            }
        },
    }


def get_conservation_monitor_alert_template() -> dict:
    """Template: Monitor conservation law, alert on violation."""
    return {
        "name": "Conservation Monitor → Alert",
        "description": "Check PLATO tiles for conservation law violations. Alert if degraded.",
        "nodes": [
            {
                "name": "Conservation Monitor",
                "type": "plato_conservation",
                "position": [250, 300],
                "parameters": {
                    "room": "={{$json.room}}"
                },
                "inputs": ["main"],
                "outputs": ["main"],
            },
            {
                "name": "Check Status",
                "type": "n8n-nodes-base.switch",
                "position": [500, 300],
                "parameters": {
                    "rules": {
                        "rules": [
                            {
                                "output": 0,
                                "operation": "equals",
                                "value1": "={{$json.status}}",
                                "value2": "DEGRADED"
                            }
                        ]
                    },
                    "fallbackOutput": 1
                },
                "inputs": ["main"],
                "outputs": ["main", "main"],
            },
            {
                "name": "Send Alert",
                "type": "plato_governance",
                "position": [750, 200],
                "parameters": {
                    "operation": "check_permission",
                    "role": "human",
                    "room": "gov/main",
                    "action": "override"
                },
                "inputs": ["main"],
                "outputs": ["main"],
            },
        ],
        "connections": {
            "Conservation Monitor": {
                "main": [["Check Status", "main"]]
            },
            "Check Status": {
                "main": [["Send Alert", "main"]]
            }
        },
    }


# ── Export Functions ────────────────────────────────────────────────────────────

def get_node_definitions() -> list[dict]:
    """Get all PLATO node definitions for n8n."""
    registry = PlatoNodeRegistry()
    return registry.get_node_definitions()


def register_nodes() -> dict:
    """Register all nodes. Returns summary."""
    registry = PlatoNodeRegistry()
    definitions = registry.get_node_definitions()
    return {
        "count": len(definitions),
        "nodes": [d["codeName"] for d in definitions],
        "categories": list(set(d["category"] for d in definitions)),
    }


def get_all_workflow_templates() -> list[dict]:
    """Get all workflow templates."""
    return [
        get_crush_analyze_then_aider_fix_template(),
        get_game_tournament_memory_template(),
        get_conservation_monitor_alert_template(),
    ]


def export_workflow_templates(base_path: str = "/tmp/plato-ng-repo/docs/n8n-templates"):
    """Export all workflow templates as JSON files."""
    import os
    os.makedirs(base_path, exist_ok=True)

    templates = get_all_workflow_templates()
    files = []

    for tmpl in templates:
        filename = tmpl["name"].lower().replace(" ", "-").replace("→", "-") + ".json"
        filepath = os.path.join(base_path, filename)
        with open(filepath, "w") as f:
            json.dump(tmpl, f, indent=2)
        files.append(filepath)

    return files


# ── Main ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    print("PLATO n8n Bridge")
    print("=" * 40)

    # Register and summarize
    result = register_nodes()
    print(f"\nRegistered {result['count']} nodes:")
    for name in sorted(result['nodes']):
        print(f"  • {name}")
    print(f"\nCategories: {', '.join(result['categories'])}")

    # Export templates
    files = export_workflow_templates()
    print(f"\nExported {len(files)} workflow templates:")
    for f in files:
        print(f"  • {f}")

    # Demo client
    client = PlatoBridgeClient()
    print(f"\nBridge client ready: {client.base_url}")

    print("\n✓ n8n bridge module ready")
    print("  Import: from services.n8n_bridge import PlatoNode, register_nodes, get_node_definitions")