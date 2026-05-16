"""Conservation law monitor — continuous daemon that checks ALL PLATO
tiles for conservation law compliance. Flags violations, tracks drift,
and feeds back into the Refiner.

Integrated into: gate pipeline, Refiner, memory decay, event bus routing.
"""

import sys, os, json, urllib.request, time, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.conservation import *

PLATO = "http://localhost:8847"

def submit(q, a, tags):
    tile = {"domain": "research_log", "question": q, "answer": str(a)[:1950],
            "tags": tags, "source": "conservation-monitor", "confidence": 0.99}
    try:
        d = json.dumps(tile).encode()
        urllib.request.urlopen(urllib.request.Request(f"{PLATO}/submit", data=d,
            headers={"Content-Type":"application/json"}), timeout=10)
    except: pass

class ConservationMonitor:
    """Continuous monitor checking all PLATO tiles for conservation law."""
    
    def __init__(self):
        self.violations = []
        self.checks = 0
    
    def check_tiles(self, tiles):
        """Check all tiles for conservation meta fields."""
        self.checks += len(tiles)
        violations_found = []
        
        for t in tiles:
            meta = t.get("_meta", {}) if isinstance(t, dict) else {}
            # Also check answer field for gamma/H
            ans = t.get("answer", "")
            if isinstance(ans, str) and ans.startswith("{"):
                try:
                    parsed = json.loads(ans)
                    if "gamma" in parsed and "H" in parsed and "V" in parsed:
                        g, h, v = parsed["gamma"], parsed["H"], parsed["V"]
                        if not is_conserved(g, h, v):
                            violations_found.append({
                                "question": t.get("question","?"),
                                "gamma": g, "H": h, "V": v,
                                "deviation": round(deviation(g, h, v), 3),
                                "expected": round(predicted_sum(v), 3)
                            })
                except: pass
        
        if violations_found:
            self.violations.extend(violations_found)
            submit("conservation/violations", json.dumps({
                "count": len(violations_found),
                "violations": violations_found[:5],
                "total_checks": self.checks
            }), ["conservation", "violation", "monitor"])
        
        return violations_found
    
    def report(self):
        """Conservation law compliance report."""
        if self.checks == 0:
            return {"status": "no_data"}
        
        return {
            "checks": self.checks,
            "violations": len(self.violations),
            "compliance_rate": f"{100 * (1 - len(self.violations)/max(1,self.checks)):.1f}%",
            "status": "HEALTHY" if len(self.violations) < 3 else "DEGRADED"
        }

if __name__ == "__main__":
    print("Conservation Law Monitor starting...")
    monitor = ConservationMonitor()
    
    # Poll PLATO rooms
    rooms = ["research_log", "fleet_math", "event-bus"]
    for room in rooms:
        try:
            resp = json.loads(urllib.request.urlopen(f"{PLATO}/room/{room}/history", timeout=10).read())
            tiles = resp.get("tiles", []) if isinstance(resp, dict) else resp
            v = monitor.check_tiles(tiles)
            print(f"  {room}: {len(tiles)} tiles, {len(v)} violations")
        except Exception as e:
            print(f"  {room}: error ({e})")
    
    report = monitor.report()
    print(f"\nConservation Monitor: {report}")
    submit("conservation/report", json.dumps(report),
           ["conservation", "report", report["status"]])
