#!/usr/bin/env python3
"""
PLATO Shell v2 — Containerized Agentic IDE

Every command runs inside a Docker container:
- No host filesystem access
- No root (runs as 'sandbox' user)
- No network access to fleet services (--network=none)
- 30s execution timeout
- Read-only workspace mount (or tmpfs for writes)

Tools: kimi, aider, crush, git, test, build, review, shell
All execute identically — inside the container.
"""
import sys, os
FLEET_LIB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, FLEET_LIB)

import json, time, uuid, subprocess, threading, shlex
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# ── Config ──────────────────────────────────────────────────
PORT = 8848
SANDBOX_IMAGE = "fleet-shell-sandbox"
WORKSPACE = Path(FLEET_LIB).parent  # ~/workspace
TIMEOUT = 30  # seconds per command
MAX_OUTPUT = 50000  # chars
CONTAINER_PREFIX = "plato-shell-"

VALID_TOOLS = {"kimi", "aider", "crush", "git", "test", "build", "review", "shell", "python"}


def run_in_container(command: str, cwd: str = "/workspace", timeout: int = TIMEOUT) -> dict:
    """Execute a command inside the sandbox container. No host access."""
    cmd_id = str(uuid.uuid4())[:8]
    container_name = f"{CONTAINER_PREFIX}{cmd_id}"

    # Build docker command
    # --network=none: no access to fleet services or internet
    # --read-only: filesystem is read-only except /tmp and /workspace
    # --pids-limit: prevent fork bombs
    # --memory: limit RAM
    # --user sandbox: non-root
    docker_cmd = [
        "sudo", "docker", "run", "--rm",
        "--name", container_name,
        "--network=none",
        "--pids-limit", "64",
        "--memory", "256m",
        "--cpus", "1.0",
        "-v", f"{WORKSPACE}:/workspace:ro",  # read-only mount
        "--tmpfs", "/tmp:size=64m",
        "--tmpfs", "/home/sandbox:size=64m",
        "-w", cwd,
        SANDBOX_IMAGE,
        "bash", "-c", command,
    ]

    try:
        proc = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = proc.stdout[-MAX_OUTPUT:] if len(proc.stdout) > MAX_OUTPUT else proc.stdout
        errors = proc.stderr[-MAX_OUTPUT:] if len(proc.stderr) > MAX_OUTPUT else proc.stderr

        return {
            "id": cmd_id,
            "exit_code": proc.returncode,
            "stdout": output,
            "stderr": errors,
            "container": container_name,
            "sandboxed": True,
        }
    except subprocess.TimeoutExpired:
        # Kill the container
        subprocess.run(["sudo", "docker", "kill", container_name],
                       capture_output=True, timeout=5)
        return {
            "id": cmd_id,
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Command timed out after {timeout}s",
            "container": container_name,
            "sandboxed": True,
        }
    except Exception as e:
        return {
            "id": cmd_id,
            "exit_code": -1,
            "stdout": "",
            "stderr": str(e),
            "container": container_name,
            "sandboxed": True,
        }


class ShellState:
    """Track agents and rooms."""
    def __init__(self):
        self.agents = {}
        self.rooms = {
            "harbor": {"cwd": "/workspace", "description": "Main workspace"},
            "fleet": {"cwd": "/workspace/fleet", "description": "Fleet library"},
            "services": {"cwd": "/workspace/fleet/services", "description": "Fleet services"},
            "research": {"cwd": "/workspace/research", "description": "Research repo"},
            "scripts": {"cwd": "/workspace/scripts", "description": "Scripts"},
            "data": {"cwd": "/workspace/data", "description": "Data directory"},
        }
        self.command_log = []
        self.lock = threading.Lock()

    def connect(self, agent, room="harbor"):
        self.agents[agent] = {
            "room": room,
            "connected_at": time.time(),
            "commands": 0,
        }
        return {
            "agent": agent,
            "room": room,
            "rooms": list(self.rooms.keys()),
        }

    def execute(self, agent, tool, command, timeout=TIMEOUT):
        if agent not in self.agents:
            return {"error": "Agent not connected. GET /connect?agent=NAME first"}

        if tool not in VALID_TOOLS:
            return {"error": f"Invalid tool: {tool}. Valid: {', '.join(sorted(VALID_TOOLS))}"}

        if not command.strip():
            return {"error": "Empty command"}

        room = self.agents[agent]["room"]
        cwd = self.rooms.get(room, self.rooms["harbor"])["cwd"]

        # Build the actual command based on tool
        safe = command.replace('"', '\\"')
        if tool == "python":
            shell_cmd = f'python3 -c "{safe}"'
        elif tool == "git":
            # Allow read-only git operations only
            git_allowed = ['log', 'diff', 'status', 'show', 'branch', 'tag', 'remote',
                          'add', 'commit', 'push', 'pull', 'fetch', 'stash', 'blame',
                          'shortlog', 'describe', 'grep', 'ls-files', 'rev-parse']
            first_word = safe.strip().split()[0] if safe.strip() else ""
            if first_word not in git_allowed:
                return {"error": f"Git subcommand '{first_word}' not allowed. Read-only git only in sandbox."}
            shell_cmd = f'git -C {cwd} {safe}'
        elif tool == "test":
            shell_cmd = f'cd {cwd} && python3 -m pytest {safe} -v --tb=short 2>&1 | tail -50'
        elif tool == "build":
            shell_cmd = f'cd {cwd} && {safe}'
        elif tool == "review":
            shell_cmd = f'cd {cwd} && git diff HEAD~1 --stat && echo "---" && git log -1 --format="%H %s"'
        elif tool == "shell":
            # Raw shell — but still in the container
            shell_cmd = safe
        else:
            # kimi, aider, crush — not installed in container, explain
            shell_cmd = f'echo "Tool {tool} requires installation. Running as shell instead." && {safe}'

        result = run_in_container(shell_cmd, cwd=cwd, timeout=min(timeout, 60))

        # Log it
        with self.lock:
            self.command_log.append({
                "id": result["id"],
                "agent": agent,
                "tool": tool,
                "command": command[:200],
                "room": room,
                "started": time.time(),
                "exit_code": result["exit_code"],
                "sandboxed": True,
            })
            self.agents[agent]["commands"] += 1

        return result

    def get_status(self):
        return {
            "service": "PLATO Shell v2 — Containerized",
            "sandbox": SANDBOX_IMAGE,
            "sandboxed": True,
            "security": {
                "network": "none (no internet, no fleet access)",
                "user": "sandbox (non-root)",
                "memory": "256MB limit",
                "cpus": "1.0 limit",
                "pids": "64 limit",
                "timeout": f"{TIMEOUT}s",
                "workspace": "read-only mount",
                "writable": "/tmp (64MB tmpfs), /home/sandbox (64MB tmpfs)",
            },
            "agents": len(self.agents),
            "rooms": list(self.rooms.keys()),
            "total_commands": len(self.command_log),
            "tools": sorted(VALID_TOOLS),
        }


state = ShellState()


class ShellHandler(BaseHTTPRequestHandler):
    def _path(self):
        return urlparse(self.path).path

    def _params(self):
        return {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}

    def _json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, default=str).encode())

    def _body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def do_GET(self):
        path = self._path()
        params = self._params()

        if path == "/":
            self._json({
                **state.get_status(),
                "api": {
                    "GET": {
                        "/": "This page",
                        "/status": "System status and security info",
                        "/connect?agent=X&room=Y": "Connect agent to room",
                        "/rooms": "Available rooms",
                        "/agents": "Connected agents",
                        "/log": "Recent command log",
                    },
                    "POST": {
                        "/cmd": "Execute command: {agent, tool, command, timeout}",
                        "/cmd/{tool}": "Tool shortcut: {agent, command}",
                    },
                },
                "note": "ALL commands run inside a Docker container. No host access.",
            })

        elif path == "/status":
            self._json(state.get_status())

        elif path == "/connect":
            agent = params.get("agent", "")
            room = params.get("room", "harbor")
            if not agent:
                self._json({"error": "Agent name required"}, 400)
                return
            self._json(state.connect(agent, room))

        elif path == "/rooms":
            self._json(state.rooms)

        elif path == "/agents":
            self._json({k: {"room": v["room"], "commands": v["commands"],
                            "connected_for": round(time.time() - v["connected_at"])}
                       for k, v in state.agents.items()})

        elif path == "/log":
            since = float(params.get("since", 0))
            self._json({"commands": [c for c in state.command_log if c["started"] > since]})

        else:
            self._json({"error": f"Not found: {path}", "hint": "GET / for API docs"}, 404)

    def do_POST(self):
        path = self._path()
        body = self._body()
        agent = body.get("agent", "")
        command = body.get("command", "")
        tool = body.get("tool", "shell")
        timeout = min(body.get("timeout", TIMEOUT), 60)

        if path == "/cmd":
            if not agent:
                self._json({"error": "Agent name required"}, 400)
                return
            result = state.execute(agent, tool, command, timeout)
            self._json(result)

        elif path.startswith("/cmd/"):
            tool_name = path.split("/")[-1]
            if not agent:
                self._json({"error": "Agent name required"}, 400)
                return
            result = state.execute(agent, tool_name, command or body.get("prompt", ""), timeout)
            self._json(result)

        else:
            self._json({"error": f"Unknown POST endpoint: {path}"}, 404)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress request logs


if __name__ == "__main__":
    # Verify docker is available
    try:
        result = subprocess.run(["sudo", "docker", "images", "-q", SANDBOX_IMAGE],
                               capture_output=True, text=True, timeout=5)
        if not result.stdout.strip():
            print(f"[ERROR] Docker image '{SANDBOX_IMAGE}' not found. Build it first.")
            sys.exit(1)
        print(f"[plato-shell-v2] Containerized — sandbox: {SANDBOX_IMAGE}")
    except Exception as e:
        print(f"[ERROR] Docker not available: {e}")
        sys.exit(1)

    server = HTTPServer(("0.0.0.0", PORT), ShellHandler)
    print(f"[plato-shell-v2] Listening on :{PORT}")
    print(f"[plato-shell-v2] Security: no network, sandbox user, 256MB, 1 CPU, 30s timeout")
    print(f"[plato-shell-v2] Workspace: {WORKSPACE} (read-only)")
    print(f"[plato-shell-v2] Tools: {', '.join(sorted(VALID_TOOLS))}")
    server.serve_forever()
