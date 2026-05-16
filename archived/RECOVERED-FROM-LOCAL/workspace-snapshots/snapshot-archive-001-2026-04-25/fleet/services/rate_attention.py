#!/usr/bin/env python3
"""
Rate Attention System — dynamic, time-based attention via rate-of-change divergence.

The core insight: commonly generated information develops rates over time.
When simulated rates don't match real-world observations, the divergence IS the attention signal.

Like a fisherman watching the water — you develop instincts about what "normal" looks like.
When the rate of bites changes, that's where you focus. The rate IS the attention.

Streams tracked:
- PLATO tile generation per room/agent
- Arena match rate per player
- Grammar rule creation/evolution rate
- Crab Trap submissions
- Service health check results
- Zeroclaw tick completions
- GitHub commit rate (from webhook or polling)

Rate computation:
- Exponential moving average (EMA) with configurable window
- Rate = delta_count / delta_time over window
- Expected rate = EMA of historical rates
- Divergence = |observed_rate - expected_rate| / expected_rate
- Attention score = divergence (higher = more attention needed)

This is Friston's free energy principle in practice:
surprise = divergence between model and observation.
Minimize surprise = pay attention to what's diverging.
"""
import sys, os
FLEET_LIB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, FLEET_LIB)

import json, time, math, threading
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 4056
DATA_DIR = Path(FLEET_LIB).parent / "data" / "rate-attention"
DATA_DIR.mkdir(parents=True, exist_ok=True)
RATES_FILE = DATA_DIR / "rates.jsonl"

# === Stream Sources ===
PLATO_URL = "http://localhost:8847"
ARENA_URL = "http://localhost:4044"
GRAMMAR_URL = "http://localhost:4045"
CRAB_TRAP_URL = "http://localhost:4042"


class RateWindow:
    """
    Tracks rate of a single metric over time.
    Uses exponential moving average — recent observations weighted more.
    Like working memory: old data fades, recent data dominates.
    """
    def __init__(self, name, window_seconds=3600, ema_alpha=0.3):
        self.name = name
        self.window_seconds = window_seconds
        self.ema_alpha = ema_alpha  # Higher = more responsive to recent changes
        
        # History: list of (timestamp, count) snapshots
        self.snapshots = []  # [(ts, count), ...]
        
        # Computed rates
        self.current_rate = 0.0  # items/hour (EMA-smoothed)
        self.expected_rate = 0.0  # long-term average
        self.divergence = 0.0  # attention signal
        self.last_count = 0
        self.last_ts = 0
        
        # Rate history for trend detection
        self.rate_history = []  # [(ts, rate), ...]
    
    def observe(self, timestamp, count):
        """
        Record a new observation. Compute rate since last observation.
        
        Args:
            timestamp: unix timestamp
            count: cumulative counter (monotonically increasing)
        """
        if self.last_ts == 0:
            self.last_ts = timestamp
            self.last_count = count
            return
        
        dt = timestamp - self.last_ts
        if dt <= 0:
            return
        
        # Instantaneous rate (items/hour)
        delta = count - self.last_count
        instant_rate = (delta / dt) * 3600
        
        # EMA update: blend new rate with old
        if self.current_rate == 0:
            self.current_rate = instant_rate
        else:
            self.current_rate = (self.ema_alpha * instant_rate) + \
                               ((1 - self.ema_alpha) * self.current_rate)
        
        # Update expected rate (slower EMA — longer memory)
        if self.expected_rate == 0:
            self.expected_rate = instant_rate
        else:
            self.expected_rate = (0.1 * instant_rate) + \
                                (0.9 * self.expected_rate)
        
        # Compute divergence (the attention signal)
        if self.expected_rate > 0:
            self.divergence = abs(self.current_rate - self.expected_rate) / self.expected_rate
        elif self.current_rate > 0:
            self.divergence = float('inf')  # Something from nothing = maximum attention
        else:
            self.divergence = 0.0
        
        # Store
        self.rate_history.append((timestamp, self.current_rate, self.divergence))
        if len(self.rate_history) > 1000:
            self.rate_history = self.rate_history[-500:]
        
        self.last_ts = timestamp
        self.last_count = count
    
    def to_dict(self):
        return {
            "name": self.name,
            "current_rate": round(self.current_rate, 2),
            "expected_rate": round(self.expected_rate, 2),
            "divergence": round(self.divergence, 3),
            "attention": self._attention_label(),
            "trend": self._trend(),
            "last_count": self.last_count,
            "observations": len(self.rate_history),
        }
    
    def _attention_label(self):
        """Human-readable attention level based on divergence."""
        d = self.divergence
        if d > 2.0: return "CRITICAL"  # Rate 3x+ expected
        if d > 1.0: return "HIGH"      # Rate 2x+ expected
        if d > 0.5: return "ELEVATED"  # Rate 1.5x+ expected
        if d > 0.2: return "NORMAL"    # Within 20%
        return "STABLE"                # Very close to expected
    
    def _trend(self):
        """Simple trend detection from recent rate history."""
        if len(self.rate_history) < 3:
            return "unknown"
        recent = [r[1] for r in self.rate_history[-3:]]
        if all(recent[i] <= recent[i+1] for i in range(len(recent)-1)):
            return "rising"
        if all(recent[i] >= recent[i+1] for i in range(len(recent)-1)):
            return "falling"
        return "oscillating"


class RateAttentionSystem:
    """
    Unified rate tracker across all fleet data streams.
    
    Each stream produces a cumulative counter. The system periodically
    samples these counters and computes rates. When observed rates
    diverge from expected rates, that's the attention signal.
    
    Like the Dojo model: attention goes where the rate changes.
    A stable fishery needs no captain. A changing one needs full attention.
    """
    
    def __init__(self):
        self.windows = {}  # stream_name -> RateWindow
        self.last_sample = 0
        self.sample_count = 0
        self.divergence_log = []  # [(ts, stream, divergence)]
        
        # Persisted rates for restart survival
        self._load_rates()
    
    def _load_rates(self):
        if RATES_FILE.exists():
            with open(RATES_FILE) as f:
                for line in f:
                    try:
                        d = json.loads(line.strip())
                        name = d["name"]
                        w = RateWindow(name)
                        w.current_rate = d.get("current_rate", 0)
                        w.expected_rate = d.get("expected_rate", 0)
                        w.divergence = d.get("divergence", 0)
                        w.last_count = d.get("last_count", 0)
                        w.last_ts = d.get("last_ts", 0)
                        self.windows[name] = w
                    except (json.JSONDecodeError, KeyError):
                        continue
            print(f"  Loaded {len(self.windows)} rate windows")
    
    def _save_rates(self):
        with open(RATES_FILE, 'w') as f:
            for w in self.windows.values():
                f.write(json.dumps(w.to_dict()) + "\n")
    
    def get_or_create(self, name, window_seconds=3600):
        if name not in self.windows:
            self.windows[name] = RateWindow(name, window_seconds)
        return self.windows[name]
    
    def sample_all(self):
        """
        Sample all data streams and compute rates.
        This is the heartbeat of the attention system.
        """
        now = time.time()
        self.sample_count += 1
        
        # 1. PLATO tiles per room
        try:
            import urllib.request
            req = urllib.request.Request(f"{PLATO_URL}/rooms", 
                headers={"User-Agent": "rate-attention/1.0"})
            resp = urllib.request.urlopen(req, timeout=5)
            rooms = json.loads(resp.read())
            total = sum(r['tile_count'] for r in rooms.values())
            self.get_or_create("plato.tiles.total").observe(now, total)
            
            for name, info in rooms.items():
                stream = f"plato.tiles.{name}"
                self.get_or_create(stream).observe(now, info['tile_count'])
        except Exception:
            pass
        
        # 2. Arena matches
        try:
            req = urllib.request.Request(f"{ARENA_URL}/leaderboard",
                headers={"User-Agent": "rate-attention/1.0"})
            resp = urllib.request.urlopen(req, timeout=5)
            data = json.loads(resp.read())
            total_games = sum(a['wins'] + a['losses'] + a['draws'] 
                           for a in data.get('leaderboard', []))
            self.get_or_create("arena.matches.total").observe(now, total_games)
        except Exception:
            pass
        
        # 3. Grammar rules
        try:
            req = urllib.request.Request(f"{GRAMMAR_URL}/grammar",
                headers={"User-Agent": "rate-attention/1.0"})
            resp = urllib.request.urlopen(req, timeout=5)
            data = json.loads(resp.read())
            self.get_or_create("grammar.rules.total").observe(now, data.get('total_rules', 0))
            self.get_or_create("grammar.evolution_cycles").observe(now, data.get('evolution_cycles', 0))
        except Exception:
            pass
        
        # 4. Crab Trap harvested tiles
        try:
            harvested = Path(FLEET_LIB).parent / "data" / "crab-trap" / "harvested-tiles.jsonl"
            if harvested.exists():
                count = sum(1 for _ in open(harvested))
                self.get_or_create("crabtrap.tiles").observe(now, count)
        except Exception:
            pass
        
        # 5. Zeroclaw ticks per agent
        try:
            zc_dir = Path(FLEET_LIB).parent / "data" / "zeroclaw" / "logs"
            if zc_dir.exists():
                for log in zc_dir.glob("zc-*.jsonl"):
                    agent = log.stem.replace("zc-", "")
                    count = sum(1 for _ in open(log))
                    self.get_or_create(f"zeroclaw.{agent}").observe(now, count)
        except Exception:
            pass
        
        # 6. Service guard entries
        try:
            sg = Path(FLEET_LIB).parent / "data" / "service-guard.log"
            if sg.exists():
                count = sum(1 for _ in open(sg))
                self.get_or_create("service_guard.checks").observe(now, count)
                # Count failures (non-OK lines)
                fail_count = sum(1 for line in open(sg) if "FAIL" in line or "RESTART" in line)
                self.get_or_create("service_guard.failures").observe(now, fail_count)
        except Exception:
            pass
        
        # Log high-divergence events
        for name, w in self.windows.items():
            if w.divergence > 0.5 and len(w.rate_history) > 0:
                self.divergence_log.append((now, name, w.divergence))
                if len(self.divergence_log) > 500:
                    self.divergence_log = self.divergence_log[-250:]
        
        self.last_sample = now
        self._save_rates()
        return self.status()
    
    def status(self):
        """Full attention dashboard."""
        all_streams = [w.to_dict() for w in self.windows.values()]
        
        # Sort by divergence (attention) — highest first
        all_streams.sort(key=lambda x: x['divergence'], reverse=True)
        
        # Attention budget: what needs attention RIGHT NOW
        critical = [s for s in all_streams if s['attention'] == 'CRITICAL']
        high = [s for s in all_streams if s['attention'] == 'HIGH']
        elevated = [s for s in all_streams if s['attention'] == 'ELEVATED']
        
        return {
            "sample_count": self.sample_count,
            "last_sample": self.last_sample,
            "total_streams": len(self.windows),
            "attention_summary": {
                "critical": len(critical),
                "high": len(high),
                "elevated": len(elevated),
                "normal": len([s for s in all_streams if s['attention'] == 'NORMAL']),
                "stable": len([s for s in all_streams if s['attention'] == 'STABLE']),
            },
            "needs_attention": critical + high,
            "all_streams": all_streams,
            "recent_divergences": [
                {"timestamp": ts, "stream": name, "divergence": round(d, 3)}
                for ts, name, d in self.divergence_log[-10:]
            ],
        }


system = RateAttentionSystem()

# Initial sample
system.sample_all()


class RateAttentionHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass
    
    def send_error(self, code, message=None):
        body = json.dumps({"error": message or f"HTTP {code}", "status": code}).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    
    def _json(self, data, status=200):
        body = json.dumps(data, default=str).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    
    def _cors(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def do_OPTIONS(self):
        self._cors()
    
    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/status":
            self._json(system.status())
        elif path == "/attention":
            # Just the things that need attention
            s = system.status()
            self._json({
                "needs_attention": s["needs_attention"],
                "summary": s["attention_summary"],
            })
        elif path == "/stream" or path == "/streams":
            # All streams sorted by divergence
            self._json({"streams": [w.to_dict() for w in system.windows.values()]})
        elif path.startswith("/stream/"):
            name = path.replace("/stream/", "")
            if name in system.windows:
                self._json(system.windows[name].to_dict())
            else:
                self._json({"error": f"stream '{name}' not found"}, 404)
        elif path == "/divergences":
            self._json({
                "recent": [
                    {"timestamp": ts, "stream": n, "divergence": round(d, 3)}
                    for ts, n, d in system.divergence_log[-20:]
                ]
            })
        else:
            self._json({
                "endpoints": ["/status", "/attention", "/streams", "/stream/{name}", "/divergences", "/sample"],
            })
    
    def do_POST(self):
        path = self.path.split("?")[0]
        if path == "/sample":
            result = system.sample_all()
            self._json(result)
        elif path == "/observe":
            # Manual observation: POST {"stream": "name", "count": 42}
            length = int(self.headers.get("Content-Length", 0))
            if length > 0:
                data = json.loads(self.rfile.read(length).decode())
                stream = data.get("stream", "")
                count = data.get("count", 0)
                if stream:
                    w = system.get_or_create(stream)
                    w.observe(time.time(), count)
                    self._json(w.to_dict())
                else:
                    self._json({"error": "missing 'stream' field"}, 400)
            else:
                self._json({"error": "empty body"}, 400)
        else:
            self._json({"error": "unknown endpoint"}, 404)


if __name__ == "__main__":
    print(f"[rate-attention] Starting on port {PORT}")
    print(f"[rate-attention] Tracking {len(system.windows)} streams")
    server = HTTPServer(("0.0.0.0", PORT), RateAttentionHandler)
    server.serve_forever()
