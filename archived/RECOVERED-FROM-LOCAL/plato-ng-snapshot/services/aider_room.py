#!/usr/bin/env python3
"""Aider PLATO Room — Aider as a PLATO-native Loop Room.

Submits code tasks as tiles. Aider edits code. Results come back as tiles.
Part of the sandbox-plato-ide playground.

Usage:
  python3 services/aider_room.py --daemon       # Start task poller
  python3 services/aider_room.py 'refactor X'   # Single-shot

  # Agent submits:
  curl -X POST localhost:8847/submit \\
    -d '{"domain":"research_log","question":"aider/task","answer":"refactor X","source":"agent"}'

  # Agent checks ticks:
  curl localhost:8847/room/research_log/history | grep aider/tick
"""

import json, urllib.request, subprocess, sys, os, time, uuid

PLATO = "http://localhost:8847"
AIDER = "/home/ubuntu/.local/bin/aider"
WORK_DIR = "/tmp/aider-workspace"

def plato(q, a, tags):
    tile = {"domain": "research_log", "question": q, "answer": str(a)[:1950],
            "tags": tags + ["aider-room"], "source": "aider", "confidence": 0.9}
    try:
        d = json.dumps(tile).encode()
        req = urllib.request.Request(f"{PLATO}/submit", data=d, headers={"Content-Type":"application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=10).read())
    except: return {}

def get_aider_tiles():
    try:
        r = json.loads(urllib.request.urlopen(f"{PLATO}/room/research_log/history", timeout=10).read())
        ts = r.get("tiles", []) if isinstance(r, dict) else r
        return [t for t in ts if "aider" in str(t.get("tags", []))]
    except: return []

def run_aider(prompt, repo=""):
    """Run aider on a prompt. Returns (output, error)."""
    os.makedirs(WORK_DIR, exist_ok=True)
    cmd = [AIDER, "--model", "z.ai/glm-5.1", "--no-git", "--yes"]
    if repo:
        cmd.extend(["--lint", repo])
    cmd.append(prompt)
    
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180, cwd=WORK_DIR)
        return proc.stdout.strip()[:2000], proc.stderr.strip()[:1000]
    except subprocess.TimeoutExpired:
        return "", "TIMEOUT: aider task exceeded 180s"
    except Exception as e:
        return "", f"ERROR: {e}"

class AiderDaemon:
    def __init__(self, interval=10):
        self.iv = interval; self.done = set()
        self.ok = 0; self.fail = 0; self.n = 0
        self.start = time.time()
    
    def tick(self, st="alive", dt=""):
        self.n += 1
        plato(f"aider/tick/{self.n}", json.dumps({
            "tick": self.n, "ok": self.ok, "fail": self.fail,
            "status": st, "uptime": int(time.time()-self.start), "detail": dt[:100]
        }), ["aider-tick", st])
    
    def do(self, tile):
        tid = tile.get("_hash", uuid.uuid4().hex[:8])
        prompt = (tile.get("answer") or tile.get("question",""))[:500]
        repo = tile.get("repo", "")
        
        self.tick("busy", tid[:8])
        out, err = run_aider(prompt, repo)
        
        if err and not out:
            self.fail += 1
            plato(f"aider/fail/{tid}", json.dumps({"task":tid,"prompt":prompt[:100],"error":err[:500]}),
                  ["aider-fail", f"task-{tid}"])
        else:
            self.ok += 1
            plato(f"aider/ok/{tid}", json.dumps({"task":tid,"prompt":prompt[:100],"output":out[:1500]}),
                  ["aider-ok", f"task-{tid}"])
    
    def run(self):
        plato("aider/started", json.dumps({"pid":os.getpid()}), ["aider-start"])
        print(f"Aider room — polling :{self.iv}s")
        while True:
            try:
                for t in get_aider_tiles():
                    if "aider/task" in t.get("question",""):
                        hid = t.get("_hash","")
                        if hid not in self.done:
                            self.done.add(hid); self.do(t)
                if self.n % 6 == 0: self.tick()
                time.sleep(self.iv)
            except Exception as e:
                self.tick("err", str(e)[:60])
                time.sleep(self.iv)

if __name__ == "__main__":
    if "--daemon" in sys.argv:
        AiderDaemon().run()
    elif len(sys.argv) > 1:
        o, e = run_aider(" ".join(sys.argv[1:]))
        print(e if e else o[:2000])
    else:
        print("Aider Room. --daemon for task poller. Single-shot with prompt arg.")
        print("sandbox-plato-ide: coding playground for rapid prototyping + stress testing.")
