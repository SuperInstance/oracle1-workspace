"""A2Ui: Agent-to-User Interface Protocol.

The standard for agents to communicate UI state to frontend renderers.
Frontend is a dumb renderer — the agent controls everything through A2Ui messages.

Schema from APPLICATION-FIRST-ARCHITECTURE.md (Claude Code design).
"""

import json, time, uuid
from dataclasses import dataclass, field
from typing import Literal, Optional

# ── Core Types ──

@dataclass
class A2UiComponent:
    """A component in the UI layout tree."""
    type: str  # container, text, button, input, list, grid, canvas, custom
    id: str
    props: dict = field(default_factory=dict)
    children: list = field(default_factory=list)
    style: dict = field(default_factory=dict)
    stateKey: Optional[str] = None

@dataclass
class A2UiAction:
    """A valid user action."""
    id: str
    label: str
    trigger: str = "click"  # click, drag, input, submit
    target: str = ""

@dataclass
class A2UiLayout:
    """The full UI layout definition."""
    components: list  # list of A2UiComponent dicts
    state: dict = field(default_factory=dict)
    actions: list = field(default_factory=list)
    mode: str = "interactive"

@dataclass
class A2UiMessage:
    """A complete A2Ui message from agent to frontend."""
    version: str = "1.0"
    messageId: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    intent: str = "render"  # render, update, replace, stream
    ui: Optional[A2UiLayout] = None
    metadata: dict = field(default_factory=lambda: {"status": "ok"})
    timestamp: float = field(default_factory=time.time)

@dataclass
class A2UiEvent:
    """A user action flowing back to the agent."""
    messageId: str = ""
    actionId: str = ""
    payload: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

# ── Serialization ──

def message_to_dict(msg: A2UiMessage) -> dict:
    """Convert A2UiMessage to dict for JSON serialization."""
    return {
        "version": msg.version,
        "messageId": msg.messageId,
        "intent": msg.intent,
        "ui": {
            "components": msg.ui.components if msg.ui else [],
            "state": msg.ui.state if msg.ui else {},
            "actions": msg.ui.actions if msg.ui else [],
            "mode": msg.ui.mode if msg.ui else "interactive"
        } if msg.ui else None,
        "metadata": msg.metadata,
        "timestamp": msg.timestamp
    }

def message_from_dict(d: dict) -> A2UiMessage:
    """Create A2UiMessage from dict."""
    ui_data = d.get("ui")
    ui = None
    if ui_data:
        ui = A2UiLayout(
            components=ui_data.get("components", []),
            state=ui_data.get("state", {}),
            actions=ui_data.get("actions", []),
            mode=ui_data.get("mode", "interactive")
        )
    return A2UiMessage(
        version=d.get("version", "1.0"),
        messageId=d.get("messageId", uuid.uuid4().hex[:8]),
        intent=d.get("intent", "render"),
        ui=ui,
        metadata=d.get("metadata", {}),
        timestamp=d.get("timestamp", time.time())
    )

# ── Renderers ──

def render_to_text(msg: A2UiMessage) -> str:
    """Render an A2Ui message as displayable text (for MUD/terminal)."""
    if not msg.ui:
        return "[no UI]"
    
    lines = []
    status = msg.metadata.get("status", "ok")
    title = msg.metadata.get("title", "")
    
    if title:
        lines.append(f"=== {title} ===")
    if status != "ok":
        lines.append(f"[{status.upper()}]")
    
    # Walk component tree
    def render_component(comp, indent=0):
        prefix = "  " * indent
        ctype = comp.get("type", "unknown")
        cid = comp.get("id", "")
        props = comp.get("props", {})
        
        if ctype == "text":
            lines.append(f"{prefix}{props.get('content', '')}")
        elif ctype == "button":
            lines.append(f"{prefix}[{props.get('label', cid)}]")
        elif ctype == "input":
            lines.append(f"{prefix}input {cid}: {props.get('value', '')}")
        elif ctype == "custom":
            lines.append(f"{prefix}[{cid} custom view]")
        # container — just indent children
        for child in comp.get("children", []):
            render_component(child, indent + 1)
    
    for comp in msg.ui.components:
        render_component(comp)
    
    # Show available actions
    if msg.ui.actions:
        lines.append("")
        lines.append("Actions:")
        for action in msg.ui.actions:
            aid = action.get("id", "?")
            label = action.get("label", aid)
            lines.append(f"  /{aid} — {label}")
    
    return "\n".join(lines)


def build_chess_board(board_state: dict, valid_moves: list = None) -> A2UiMessage:
    """Build a chess board A2Ui message from state."""
    pieces = board_state.get("pieces", [])
    turn = board_state.get("turn", "white")
    
    components = [
        {"type": "text", "id": "status", "props": {"content": f"{turn}'s turn"}},
        {"type": "custom", "id": "chess-board", "props": {
            "pieces": pieces, "validMoves": valid_moves or []
        }}
    ]
    
    actions = [
        {"id": "select-square", "label": "Select a square", "trigger": "click", "target": "chess-board"},
        {"id": "make-move", "label": "Move piece", "trigger": "drag", "target": "chess-board"},
    ]
    
    layout = A2UiLayout(components=components, state=board_state, actions=actions)
    msg = A2UiMessage(intent="render", ui=layout, metadata={"title": "Chess"})
    return msg


def build_todo_app(todos: list) -> A2UiMessage:
    """Build a todo list A2Ui message."""
    items = []
    for t in todos:
        status = "✓" if t.get("done") else "○"
        items.append(f"{status} {t.get('task', '')}")
    
    components = [{"type": "text", "id": "title", "props": {"content": "Todo List"}}]
    
    if items:
        for item in items:
            components.append({"type": "text", "id": f"todo-{items.index(item)}", "props": {"content": item}})
    
    components.append({"type": "input", "id": "new-todo", "props": {"placeholder": "Add task..."}})
    components.append({"type": "button", "id": "add-btn", "props": {"label": "Add"}})
    
    actions = [{"id": "add-todo", "label": "Add task", "trigger": "click", "target": "add-btn"}]
    layout = A2UiLayout(components=components, state={"todos": todos}, actions=actions)
    return A2UiMessage(intent="render", ui=layout, metadata={"title": "Todo List"})


# ── Stream Parser ──

def stream_a2ui(agent_output: str):
    """Parse agent output into A2Ui messages.
    Looks for A2Ui: {...} blocks in the output."""
    import re
    for match in re.finditer(r'A2Ui:\s*(\{.*?\})(?:\n|$)', agent_output, re.DOTALL):
        try:
            d = json.loads(match.group(1))
            yield message_from_dict(d)
        except (json.JSONDecodeError, KeyError):
            continue


# ── Test ──

if __name__ == "__main__":
    import sys; sys.path.insert(0, "/tmp/plato-ng-repo")
    from lib.plato_client import submit
    
    # Test: build and render a chess board A2Ui message
    board_state = {
        "pieces": [
            ["r","n","b","q","k","b","n","r"],
            ["p"]*8, ["."]*8, ["."]*8, ["."]*8, ["."]*8,
            ["P"]*8, ["R","N","B","Q","K","B","N","R"]
        ],
        "turn": "white"
    }
    msg = build_chess_board(board_state)
    print("=== Chess Board (A2Ui text render) ===")
    print(render_to_text(msg))
    print()
    
    # Test: todo app
    todos = [{"task": "Build A2Ui protocol", "done": True}, {"task": "Ship plato-ng", "done": False}]
    msg2 = build_todo_app(todos)
    print("=== Todo List (A2Ui text render) ===")
    print(render_to_text(msg2))
    print()
    
    # Test: message serialization roundtrip
    d = message_to_dict(msg)
    msg_rt = message_from_dict(d)
    print(f"Roundtrip OK: version={msg_rt.version}, intent={msg_rt.intent}, messageId={msg_rt.messageId}")
    
    # Push to PLATO
    submit("research_log", "a2ui/protocol/registered", json.dumps({
        "version": "1.0", "schema": "A2UiMessage, A2UiComponent, A2UiEvent, A2UiLayout",
        "renderers": ["text/MUD", "web/HTML (render_to_text)"],
        "examples": ["chess_board", "todo_app"]
    }), ["a2ui", "protocol", "registered"])
    
    print("\nA2Ui protocol registered on PLATO.")
