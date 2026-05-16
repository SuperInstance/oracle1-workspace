#!/usr/bin/env python3
"""
PERPETUAL RESEARCH DAEMON — Never stops. Reports every 10 min.
Runs batches indefinitely. Spawned as nohup. Communicates with PLATO.
"""

import numpy as np, math, time, os, sys, json, urllib.request, subprocess

BATCH_DIR = os.path.expanduser("~/.openclaw/workspace/research/next-100")
sys.path.insert(0, os.path.expanduser("~/.openclaw/workspace/research/100-turns"))
from fleet_health_v2 import coupling_entropy, algebraic_normalized

PLATO_URL = "http://localhost:8847/submit"
np.random.seed()

def plato_msg(title, body, tags):
    try:
        payload = json.dumps({"domain":"research_log","question":title,"answer":body[:1950],"tags":tags+["perpetual-daemon","2026-05-15"],"source":"oracle1","confidence":0.9})
        req = urllib.request.Request(PLATO_URL, data=payload.encode(), headers={"Content-Type":"application/json"})
        return json.loads(urllib.request.urlopen(req).read()).get("status","?")
    except: return "err"

def run_experiment():
    """Run one research experiment. Returns result dict."""
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
    
    return {"V": V, "k": k, "gamma": round(g,4), "H": round(h,4), 
            "sum": round(g+h,4), "pred": round(pred,4), 
            "time": time.strftime('%H:%M:%S', time.gmtime())}

# Continuous loop — never stops
print("PERPETUAL RESEARCH DAEMON STARTED — never stops")
print(f"PID: {os.getpid()}")
print()

tick_count = 0
last_report = time.time()

while True:
    # Run one experiment
    result = run_experiment()
    tick_count += 1
    
    # Log
    r = result
    line = f"[{r['time']}] V={r['V']:2d} k={r['k']:2d} γ={r['gamma']:.3f} H={r['H']:.3f} Σ={r['sum']:.3f} pred={r['pred']:.3f} err={r['sum']-r['pred']:+.3f}"
    print(line)
    
    # Push every experiment to PLATO
    plato_msg(f"perp-tick {r['time']}", 
              f"V={r['V']} k={r['k']} gamma={r['gamma']} H={r['H']} sum={r['sum']} pred={r['pred']}",
              ["perp-tick", f"V-{r['V']}", f"k-{r['k']}"])
    
    # Every 10 minutes: check in with Casey via PLATO summary
    elapsed = time.time() - last_report
    if elapsed >= 600:  # 10 minutes
        plato_msg(f"PERP TICK {tick_count} experiments run",
                  f"Perpetual daemon: {tick_count} experiments in {(elapsed/60):.0f} min. Last: V={r['V']} k={r['k']} sum={r['sum']} pred={r['pred']}.",
                  ["perp-report", f"tick-{tick_count}"])
        last_report = time.time()
        tick_count = 0  # reset counter for next window
    
    time.sleep(30)  # 30 seconds between experiments
