#!/usr/bin/env python3
"""PLATO OpenHands Room — Docker-sandboxed orchestrated coding environment.

OpenHands is an open-source AI software development platform that runs in a
Docker container with a sandboxed OS, file editor, browser, and shell.

Usage:
  python3 services/openhands_room.py --daemon    # Start task poller
  python3 services/openhands_room.py "build X"   # Single-shot

  # Agent submits:
  curl -X POST localhost:8847/submit \\
    -d '{"domain":"research_log","question":"openhands/task","answer":"build a chess game","source":"agent-name"}'

  # Agent checks ticks:
  curl localhost:8847/room/research_log/history | grep openhands/tick

  # Agent checks logs:
  curl localhost:8847/room/research_log/history | grep openhands/log

  # Agent checks results:
  curl localhost:8847/room/research_log/history | grep openhands/ok
  curl localhost:8847/room/research_log/history | grep openhands/fail
"""

import json, urllib.request, subprocess, sys, os, time, uuid, threading, re

PLATO = "http://localhost:8847"
DOMAIN = "research_log"

# Safety harness limits
MAX_CONTAINERS = 5
TASK_TIMEOUT = 300  # seconds
OPENHANDS_IMAGE = "dockhand/openhands:latest"  # or your custom image

# Container resource limits
CONTAINER_LIMITS = [
    "--memory=2g",
    "--cpus=1.0",
    "--pids-limit=100",
    "--ulimit nofile=1024:1024",
]


def plato(q, a, tags):
    """Submit a tile to PLATO."""
    tile = {
        "domain": DOMAIN,
        "question": q,
        "answer": str(a)[:3950],  # leave room for metadata
        "tags": tags + ["openhands-room"],
        "source": "openhands",
        "confidence": 0.9,
    }
    try:
        d = json.dumps(tile).encode()
        req = urllib.request.Request(
            f"{PLATO}/submit", data=d, headers={"Content-Type": "application/json"}
        )
        return json.loads(urllib.request.urlopen(req, timeout=10).read())
    except Exception as e:
        return {"error": str(e)}


def get_plato_tiles(pattern=""):
    """Get tiles from PLATO history, optionally filtered by pattern."""
    try:
        r = json.loads(
            urllib.request.urlopen(f"{PLATO}/room/{DOMAIN}/history", timeout=10).read()
        )
        ts = r.get("tiles", []) if isinstance(r, dict) else r
        if pattern:
            return [t for t in ts if pattern in str(t.get("question", ""))]
        return ts
    except:
        return []


def get_active_container_count():
    """Count active openhands containers."""
    try:
        out = subprocess.check_output(
            ["docker", "ps", "--filter", "label=plato_openhands=true", "-q"],
            text=True,
        )
        return len(out.strip().split("\n")) if out.strip() else 0
    except:
        return 0


def run_task_in_container(task_id, prompt, output_dir="/workspace/output"):
    """Run a task in an OpenHands Docker container with log streaming."""
    container_name = f"plato-openhands-{task_id[:8]}"

    # Build docker command with safety limits
    docker_cmd = [
        "docker", "run",
        "--name", container_name,
        "--label", "plato_openhands=true",
        "-d",  # detached for log streaming
    ] + CONTAINER_LIMITS + [
        "--volume", f"{output_dir}:/workspace/output",
        OPENHANDS_IMAGE,
        "python3", "/openhands/run_task.py",
    ]

    # We'll execute in a container, capture logs, then commit result
    # For now, use a simpler approach: run task script in container

    log_buffer = []
    status = "starting"

    try:
        # Start container with task
        container_id = subprocess.check_output(
            ["docker", "run", "--detach",
             "--name", container_name,
             "--label", "plato_openhands=true",
             ] + CONTAINER_LIMITS + [
                "-v", f"/tmp/openhands-{task_id[:8]}:/workspace",
                OPENHANDS_IMAGE,
                "bash", "-c",
                f"echo '{prompt[:1000]}' > /workspace/task.txt && "
                "python3 -c \""
                "from openhands.core.main import run_app; "
                "run_app('/workspace/task.txt')\" 2>&1 || true"
            ],
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()

        log_buffer.append(f"Container {container_id[:12]} started")

        # Stream logs while container runs
        deadline = time.time() + TASK_TIMEOUT
        while time.time() < deadline:
            # Check if container still running
            try:
                state = subprocess.check_output(
                    ["docker", "inspect", "--format", "{{.State.Status}}", container_name],
                    text=True,
                ).strip()
            except:
                break

            # Get recent logs
            try:
                logs = subprocess.check_output(
                    ["docker", "logs", "--tail", "50", container_name],
                    text=True,
                    stderr=subprocess.STDOUT,
                )
                for line in logs.split("\n")[-20:]:
                    if line.strip():
                        log_buffer.append(line.strip()[:200])
                        # Stream to PLATO periodically
                        if len(log_buffer) % 10 == 0:
                            plato(
                                f"openhands/log/{task_id[:8]}",
                                "\n".join(log_buffer[-50:]),
                                ["openhands-log", f"task-{task_id[:8]}"],
                            )
            except:
                pass

            if state in ("exited", "dead"):
                break

            time.sleep(2)

        # Get final logs
        try:
            final_logs = subprocess.check_output(
                ["docker", "logs", "--tail", "200", container_name],
                text=True,
                stderr=subprocess.STDOUT,
            )
            log_buffer.append("=== FINAL LOGS ===")
            log_buffer.append(final_logs[:3000])
        except:
            log_buffer.append("Could not retrieve final logs")

        # Collect artifacts from /workspace/output
        artifacts = []
        try:
            artifact_files = subprocess.check_output(
                ["docker", "cp", f"{container_name}:/workspace/output/.", f"/tmp/artifacts-{task_id[:8]}/"],
                text=True,
            )
            if os.path.exists(f"/tmp/artifacts-{task_id[:8]}"):
                for f in os.listdir(f"/tmp/artifacts-{task_id[:8]}"):
                    fp = f"/tmp/artifacts-{task_id[:8]}/{f}"
                    artifacts.append({"name": f, "size": os.path.getsize(fp), "path": fp})
        except:
            pass

        # Check exit code
        try:
            exit_code = subprocess.check_output(
                ["docker", "inspect", "--format", "{{.State.ExitCode}}", container_name],
                text=True,
            ).strip()
            status = "ok" if exit_code == "0" else "fail"
        except:
            status = "fail"

    except subprocess.TimeoutExpired:
        status = "timeout"
        log_buffer.append(f"TIMEOUT after {TASK_TIMEOUT}s")
    except Exception as e:
        status = "fail"
        log_buffer.append(f"ERROR: {str(e)}")
    finally:
        # Cleanup container
        try:
            subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)
        except:
            pass
        # Cleanup temp artifact dir
        try:
            subprocess.run(["rm", "-rf", f"/tmp/artifacts-{task_id[:8]}"], capture_output=True)
        except:
            pass
        try:
            subprocess.run(["rm", "-rf", f"/tmp/openhands-{task_id[:8]}"], capture_output=True)
        except:
            pass

    return status, log_buffer, artifacts


class Daemon:
    """OpenHands Room daemon — polls for tasks, runs in Docker sandbox."""

    def __init__(self, interval=5):
        self.iv = interval
        self.done = set()
        self.tick_n = 0
        self.ok = 0
        self.fail = 0
        self.start = time.time()
        self.active_containers = 0

    def tick(self, st="alive", dt=""):
        """Publish tick to PLATO."""
        self.tick_n += 1
        self.active_containers = get_active_container_count()
        plato(
            f"openhands/tick/{self.tick_n}",
            json.dumps({
                "tick": self.tick_n,
                "ok": self.ok,
                "fail": self.fail,
                "status": st,
                "uptime": int(time.time() - self.start),
                "active_containers": self.active_containers,
                "detail": dt[:100],
            }),
            ["openhands-tick", st],
        )

    def do(self, tile):
        """Process a single task tile."""
        task_id = tile.get("_hash", uuid.uuid4().hex[:8])
        prompt = tile.get("answer") or tile.get("question", "")[:5000]

        self.tick("busy", f"task {task_id[:8]}")

        # Check container limit
        if self.active_containers >= MAX_CONTAINERS:
            plato(
                f"openhands/wait/{task_id[:8]}",
                json.dumps({"task": task_id, "reason": "max_containers", "limit": MAX_CONTAINERS}),
                ["openhands-wait", f"task-{task_id[:8]}"],
            )
            return

        status, logs, artifacts = run_task_in_container(task_id, prompt)

        if status == "ok":
            self.ok += 1
            plato(
                f"openhands/ok/{task_id[:8]}",
                json.dumps({
                    "task": task_id,
                    "prompt": prompt[:200],
                    "status": status,
                    "logs": logs[-30:],
                    "artifacts": artifacts,
                    "tick": self.tick_n,
                }),
                ["openhands-ok", f"task-{task_id[:8]}"],
            )
        else:
            self.fail += 1
            plato(
                f"openhands/fail/{task_id[:8]}",
                json.dumps({
                    "task": task_id,
                    "prompt": prompt[:100],
                    "status": status,
                    "error": str(logs[-5:]),
                    "tick": self.tick_n,
                }),
                ["openhands-fail", f"task-{task_id[:8]}"],
            )

    def run(self):
        """Main polling loop."""
        plato(
            "openhands/started",
            json.dumps({
                "pid": os.getpid(),
                "poll": self.iv,
                "max_containers": MAX_CONTAINERS,
                "timeout": TASK_TIMEOUT,
            }),
            ["openhands-start"],
        )
        print(f"OpenHands Room — polling :{self.iv}s, max {MAX_CONTAINERS} containers")
        while True:
            try:
                for t in get_plato_tiles():
                    if "openhands/task" in t.get("question", ""):
                        hid = t.get("_hash", "")
                        if hid not in self.done:
                            self.done.add(hid)
                            self.do(t)

                if self.tick_n % 6 == 0:
                    self.tick()

                time.sleep(self.iv)
            except Exception as e:
                self.tick("err", str(e)[:60])
                time.sleep(self.iv)


def run_single(prompt):
    """Run a single task (non-daemon mode)."""
    task_id = uuid.uuid4().hex[:8]
    status, logs, artifacts = run_task_in_container(task_id, prompt)
    print(f"Status: {status}")
    print(f"Logs:\n" + "\n".join(logs[-20:]))
    if artifacts:
        print(f"Artifacts: {artifacts}")
    return status


# Bootcamp pattern: simulate via inference first, then compile to code
def bootcamp_simulate(prompt):
    """
    Bootcamp pattern: the agent IS the application first (simulates via inference),
    then compiles to code.

    For OpenHands, this means:
    1. Given a task, simulate what OpenHands would do
    2. Generate the actual command sequence OpenHands would run
    3. This provides training signal and validation
    """
    simulation_prompt = f"""You are simulating OpenHands execution for this task:

Task: {prompt}

As the OpenHands agent, think through:
1. What files need to be created/modified?
2. What commands would you run?
3. What is the expected output?

Return your simulation as a JSON plan:
{{"steps": [{"action": "command", "args": []}], "expected_output": "", "files": []}}
"""
    # In practice, call a model here to get simulation
    # For now, return a basic structure
    return {
        "steps": [{"action": "echo", "args": [prompt]}],
        "expected_output": "Task received",
        "files": [],
    }


if __name__ == "__main__":
    if "--daemon" in sys.argv:
        Daemon().run()
    elif len(sys.argv) > 1:
        run_single(" ".join(sys.argv[1:]))
    else:
        print("OpenHands Room v1.0")
        print("  --daemon    Start task poller")
        print("  <prompt>    Run single task")