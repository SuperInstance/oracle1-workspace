#!/usr/bin/env python3
"""PLATO Crush Room v2 — tick-tracked, failure-logged, recursively teachable.

Any agent submits a task tile → Crush processes → result tile comes back.
Success AND failure tracked. Subagents check ticks like they check FM.
Crush reads own history for recursive improvement.

Usage:
  python3 services/crush_room.py --daemon    # Start task poller
  python3 services/crush_room.py 'analyze X' # Single-shot

  # Agent submits:
  curl -X POST localhost:8847/submit \\
    -d '{"domain":"research_log","question":"crush/task","answer":"analyze X","source":"agent-name"}'

  # Agent checks ticks:
  curl localhost:8847/room/research_log/history | grep crush/tick
"""

import json, urllib.request, subprocess, sys, os, time, uuid

PLATO = "http://localhost:8847"
CRUSH = "/home/ubuntu/.npm-global/bin/crush"

def plato(q, a, tags):
    tile = {"domain": "research_log", "question": q, "answer": str(a)[:1950],
            "tags": tags + ["crush-room"], "source": "crush", "confidence": 0.9}
    try:
        d = json.dumps(tile).encode()
        req = urllib.request.Request(f"{PLATO}/submit", data=d, headers={"Content-Type":"application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=10).read())
    except: return {}

def get_crush_tiles():
    try:
        r = json.loads(urllib.request.urlopen(f"{PLATO}/room/research_log/history", timeout=10).read())
        ts = r.get("tiles", []) if isinstance(r, dict) else r
        return [t for t in ts if "crush" in str(t.get("tags", []))]
    except: return []

def run(prompt, context=""):
    cmd = [CRUSH, "run"]
    try:
        inp = context + "\n\n" + prompt if context else ""
        proc = subprocess.run(cmd if not context else cmd + [prompt],
                            input=inp if context else None,
                            capture_output=True, text=True, timeout=120)
        return proc.stdout.strip(), proc.stderr.strip()
    except subprocess.TimeoutExpired: return "", "TIMEOUT"
    except Exception as e: return "", str(e)

class Daemon:
    def __init__(self, interval=5):
        self.iv = interval; self.done = set()
        self.tick_n = 0; self.ok = 0; self.fail = 0
        self.start = time.time()
    
    def tick(self, st="alive", dt=""):
        self.tick_n += 1
        plato(f"crush/tick/{self.tick_n}", json.dumps({
            "tick": self.tick_n, "ok": self.ok, "fail": self.fail,
            "status": st, "uptime": int(time.time()-self.start), "detail": dt[:100]
        }), ["crush-tick", st])
    
    def do(self, tile):
        tid = tile.get("_hash", uuid.uuid4().hex[:8])
        prompt = (tile.get("answer") or tile.get("question",""))[:500]
        
        # Recursive: read past results for context
        past = get_crush_tiles()
        ctx = ""
        if past:
            recent = [t.get("answer","")[:200] for t in past[-5:] if "crush/result" in t.get("question","")]
            if recent: ctx = "Past results:\n" + "\n---\n".join(recent)
        
        self.tick("busy", f"task {tid[:8]}")
        out, err = run(prompt, ctx)
        
        if err and not out:
            self.fail += 1
            plato(f"crush/fail/{tid}", json.dumps({"task":tid,"prompt":prompt[:100],"error":err[:500],"tick":self.tick_n}),
                  ["crush-fail", f"task-{tid}"])
        else:
            self.ok += 1
            plato(f"crush/ok/{tid}", json.dumps({"task":tid,"prompt":prompt[:100],"len":len(out),"result":out[:1500],"tick":self.tick_n}),
                  ["crush-ok", f"task-{tid}"])
    
    def run(self):
        plato("crush/started", json.dumps({"pid":os.getpid(),"poll":self.iv}), ["crush-start"])
        print(f"Crush v2 — polling :{self.iv}s")
        while True:
            try:
                for t in get_crush_tiles():
                    if "crush/task" in t.get("question",""):
                        hid = t.get("_hash","")
                        if hid not in self.done:
                            self.done.add(hid); self.do(t)
                if self.tick_n % 6 == 0: self.tick()
                time.sleep(self.iv)
            except Exception as e:
                self.tick("err", str(e)[:60])
                time.sleep(self.iv)

if __name__ == "__main__":
    if "--daemon" in sys.argv:
        Daemon().run()
    elif len(sys.argv) > 1:
        o, e = run(" ".join(sys.argv[1:]))
        print(e if e else o[:2000])
    else:
        print("Crush Room v2. --daemon for task poller. Single-shot with prompt arg.")
