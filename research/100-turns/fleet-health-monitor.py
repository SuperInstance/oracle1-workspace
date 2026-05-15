#!/usr/bin/env python3
"""
Fleet Health Monitor Daemon v1 — Streaming H-gamma-tau health tracking.

Reads coupling information from PLATO rooms, computes spectral health
metrics using fleet-math v0.2.0, and publishes health tiles.

Features:
  - H(C) spectral entropy (continuous)
  - gamma_tilde algebraic connectivity  
  - tau timing stability
  - FleetHealthMetric z-score vs baseline
  - 4-regime classification
  - Temporal drift detection via dH/dt
  - Anomaly alerts above threshold
"""

import numpy as np
import json, time, sys, os, math
import urllib.request
from collections import deque

# Import fleet-math v0.2.0 health module
sys.path.insert(0, os.path.expanduser("~/.openclaw/workspace/research/100-turns"))
try:
    from fleet_health_v2 import (
        coupling_entropy, algebraic_normalized, 
        timing_stability, FleetHealthMetric
    )
except ImportError:
    # Fallback to installed fleet-math
    from fleet_math.health import (
        coupling_entropy, algebraic_normalized,
        timing_stability, FleetHealthMetric
    )

PLATO_HOST = "localhost:8847"
COUPLING_ROOM = "fleet-coupling"
HEALTH_ROOM = "fleet-health"
SAMPLE_INTERVAL = 900.0  # 15 min (matches fleet tick)
HISTORY_SIZE = 96  # 24h at 15min intervals

class FleetHealthMonitor:
    def __init__(self):
        self.H_history = deque(maxlen=HISTORY_SIZE)
        self.gamma_history = deque(maxlen=HISTORY_SIZE)
        self.tau_history = deque(maxlen=HISTORY_SIZE)
        self.timestamps = deque(maxlen=HISTORY_SIZE)
        
        # Fit baseline if not already done
        if FleetHealthMetric._baseline_mu is None:
            FleetHealthMetric.fit_baseline()
    
    def fetch_coupling_data(self):
        """Fetch coupling data from PLATO."""
        url = f"http://{PLATO_HOST}/room/{COUPLING_ROOM}/history"
        try:
            raw = json.loads(urllib.request.urlopen(url).read())
            tiles = raw.get("tiles", []) if isinstance(raw, dict) else raw
            return tiles
        except Exception as e:
            print(f"FETCH ERROR: {e}", file=sys.stderr)
            return []
    
    def build_coupling_matrix(self, tiles):
        """Build coupling matrix from agent style vectors in PLATO tiles."""
        agents = {}
        for tile in tiles:
            src = tile.get("source", "unknown")
            ans = tile.get("answer", "{}")
            try:
                data = json.loads(ans) if isinstance(ans, str) else ans
            except:
                continue
            if isinstance(data, dict) and "style_vector" in data:
                sv = np.array(data["style_vector"], dtype=float)
                agents[src] = sv
        
        if len(agents) < 2:
            return None, list(agents.keys())
        
        names = list(agents.keys())
        V = len(names)
        X = np.array([agents[n] for n in names])
        
        norms = np.linalg.norm(X, axis=1, keepdims=True) + 1e-10
        C = X @ X.T / (norms @ norms.T)
        return C, names
    
    def tick(self, force_publish=False):
        """Single monitoring tick. Returns health report dict."""
        tiles = self.fetch_coupling_data()
        
        if not tiles:
            return {"status": "no_data", "agents": 0}
        
        C, agent_names = self.build_coupling_matrix(tiles)
        if C is None:
            return {"status": "insufficient", "agents": len(agent_names)}
        
        V = len(agent_names)
        
        # Compute metrics
        H = coupling_entropy(C)
        gamma = algebraic_normalized(C)
        tau = 0.5  # default if no timing data
        z = FleetHealthMetric.compute(C)
        _, diag = FleetHealthMetric.diagnose(C)
        
        # Regime classification
        H_phi = 1.618  # 1/phi
        if H > 0.618 and gamma > 0.15:
            regime = "III-emergent"
        elif H > 0.618 and gamma <= 0.15:
            regime = "I-diverse-fragmented"
        elif H <= 0.618 and gamma > 0.15:
            regime = "IV-consensus-herd"
        else:
            regime = "II-homogeneous-fragmented"
        
        # Temporal drift (dH/dt)
        drift_H = 0.0
        drift_gamma = 0.0
        if self.H_history:
            dt = time.time() - self.timestamps[-1] if self.timestamps else SAMPLE_INTERVAL
            if dt > 0:
                drift_H = (H - self.H_history[-1]) / dt * SAMPLE_INTERVAL  # per-tick rate
                drift_gamma = (gamma - self.gamma_history[-1]) / dt * SAMPLE_INTERVAL
        
        # Update history
        now = time.time()
        self.H_history.append(H)
        self.gamma_history.append(gamma)
        self.tau_history.append(tau)
        self.timestamps.append(now)
        
        # Anomaly detection
        anomaly = "none"
        if abs(z) > 150:
            anomaly = f"CRITICAL: z={z:.0f} ({diag})"
        elif abs(z) > 10:
            anomaly = f"HIGH: z={z:.0f} ({diag})"
        elif abs(z) > 3:
            anomaly = f"WARNING: z={z:.0f} ({diag})"
        
        if drift_H < 0.001 and len(self.H_history) > 10:
            if np.std(list(self.H_history)[-10:]) < 0.001:
                anomaly += " | STALE_COUPLING"
        
        report = {
            "status": "ok",
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "agents": V,
            "agent_names": agent_names,
            "H": round(H, 6),
            "gamma": round(gamma, 6),
            "tau": round(tau, 6),
            "health_z": round(z, 2),
            "regime": regime,
            "anomaly": anomaly.strip(" |"),
            "drift_H_per_tick": round(drift_H, 6),
            "drift_gamma_per_tick": round(drift_gamma, 6),
            "history_size": len(self.H_history),
            "verdict": "HEALTHY" if abs(z) < 1.0 else "WATCH" if abs(z) < 3.0 else "ANOMALY"
        }
        
        return report
    
    def publish(self, report):
        """Publish health report to PLATO."""
        answer_json = json.dumps({
            "H": report.get("H"),
            "gamma": report.get("gamma"),
            "health_z": report.get("health_z"),
            "regime": report.get("regime"),
            "verdict": report.get("verdict"),
            "anomaly": report.get("anomaly"),
            "agents": report.get("agents"),
            "drift_H": report.get("drift_H_per_tick"),
        })
        
        payload = {
            "domain": "fleet-health",
            "question": f"fleet-health-tick {report.get('timestamp', '?')}",
            "answer": answer_json,
            "tags": ["fleet-health", "H-gamma", report.get("regime", "unknown"), 
                     report.get("verdict", "unknown")],
            "source": "fleet-health-monitor",
            "confidence": 0.95
        }
        
        url = f"http://{PLATO_HOST}/submit"
        try:
            data = json.dumps(payload).encode()
            req = urllib.request.Request(url, data=data,
                headers={"Content-Type": "application/json"})
            resp = urllib.request.urlopen(req)
            return json.loads(resp.read())
        except Exception as e:
            return {"error": str(e)}


def main_loop():
    monitor = FleetHealthMonitor()
    print(f"Fleet Health Monitor v1 — {SAMPLE_INTERVAL}s interval")
    print(f"PLATO: {PLATO_HOST}, rooms: {COUPLING_ROOM} -> {HEALTH_ROOM}")
    print()
    
    while True:
        report = monitor.tick()
        
        # Print status
        if report.get("status") == "ok":
            reg = report["regime"]
            verdict = report["verdict"]
            anomaly = report["anomaly"]
            
            color = {"III-emergent": "🟢", "IV-consensus-herd": "🟡", 
                     "I-diverse-fragmented": "🟠", "II-homogeneous-fragmented": "🔴"}
            c = color.get(reg, "⚪")
            
            print(f"{c} {report['timestamp']} | V={report['agents']} | "
                  f"H={report['H']:.4f} γ={report['gamma']:.4f} | "
                  f"z={report['health_z']:+.1f} | {reg} | {verdict}",
                  end="")
            if anomaly != "none":
                print(f" ⚠️ {anomaly}", end="")
            print()
            
            # Publish to PLATO
            result = monitor.publish(report)
            if result.get("error"):
                print(f"  PUBLISH ERROR: {result['error']}")
        else:
            print(f"⚪ {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} | "
                  f"{report.get('status', 'error')} | V={report.get('agents', 0)}")
        
        try:
            time.sleep(SAMPLE_INTERVAL)
        except KeyboardInterrupt:
            print("\nShutdown.")
            break


if __name__ == "__main__":
    # Single-tick mode by default
    monitor = FleetHealthMonitor()
    report = monitor.tick()
    
    if report.get("status") == "ok":
        print(json.dumps(report, indent=2))
        result = monitor.publish(report)
        print(f"\nPublished: {json.dumps(result, indent=2)[:100]}")
    else:
        print(f"Status: {report.get('status')} (agents: {report.get('agents', 0)})")
        print("No health data available.")
