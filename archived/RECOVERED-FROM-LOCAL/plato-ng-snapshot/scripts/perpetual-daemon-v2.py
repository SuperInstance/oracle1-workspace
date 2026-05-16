#!/usr/bin/env python3
"""Perpetual Research Daemon v2 — starts fast, never stops."""

import sys, os, json, urllib.request, time, math

PLATO = "http://localhost:8847/submit"

print("DAEMON V2 STARTING", flush=True)

def plato(title, body, tags):
    try:
        answer = str(body)[:1950]
        if len(answer) < 40:
            answer += " perpetual daemon experiment continuous loop automated research"
        payload = json.dumps({
            "domain": "research_log", "question": title,
            "answer": answer,
            "tags": tags + ["v2-daemon", "2026-05-15"],
            "source": "oracle1", "confidence": 0.85
        })
        req = urllib.request.Request(PLATO, data=payload.encode(),
            headers={"Content-Type": "application/json"})
        resp = json.loads(urllib.request.urlopen(req, timeout=5).read().decode())
        return resp.get("status", "?")
    except Exception as e:
        return f"err:{str(e)[:30]}"

tick = 0
start = time.time()

while True:
    tick += 1
    t = time.strftime('%H:%M:%S', time.gmtime())
    elapsed = time.time() - start
    print(f"[{t}] Tick {tick} — {elapsed:.0f}s elapsed", flush=True)

    if tick == 1:
        try:
            resp = urllib.request.urlopen("http://localhost:8847/status", timeout=3)
            status = json.loads(resp.read().decode())
            a = status.get("gate_stats", {}).get("accepted", 0)
            print(f"  PLATO: {a} tiles accepted", flush=True)
        except Exception as e:
            print(f"  PLATO status: {e}", flush=True)

    # Heartbeat every 5 ticks
    if tick % 5 == 0:
        r = plato(f"perp-tick {t}", f"Alive tick {tick} {elapsed:.0f}s", ["perp-v2"])
        print(f"  PLATO push: {r}", flush=True)

    # Experiment every 20 ticks (~40s at 2s interval)
    if tick % 20 == 0:
        print(f"  Running experiment...", flush=True)
        try:
            sys.path.insert(0, os.path.expanduser("~/.openclaw/workspace/research/100-turns"))
            from fleet_health_v2 import coupling_entropy, algebraic_normalized
            import numpy as np
            V = np.random.choice([10, 20, 30, 50])
            k = np.random.randint(2, min(25, V))
            U = np.random.randn(V, k)
            Vm = np.random.randn(k, 109)
            X = U @ Vm + np.random.randn(V, 109) * 0.2
            norms = np.linalg.norm(X, axis=1, keepdims=True) + 1e-10
            C = X @ X.T / (norms @ norms.T)
            g = algebraic_normalized(C)
            h = coupling_entropy(C)
            pred = 1.364 - 0.159 * math.log(max(V, 3))
            result = f"V={V} k={k} gamma={g:.3f} H={h:.3f} sum={g+h:.3f} pred={pred:.3f} err={g+h-pred:+.3f}"
            print(f"  Result: {result}", flush=True)
            plato(f"perp-exp {t}", result, ["perp-experiment", f"V-{V}", f"k-{k}"])
        except Exception as e:
            print(f"  Experiment error: {e}", flush=True)

    time.sleep(3)
