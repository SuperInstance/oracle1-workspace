#!/usr/bin/env python3
"""
Archivist — Fleet History & Artifact Preservation (port 4054)

Designed by Perplexity AI (4th Crab Trap response), built by Oracle1.
Service #20: the fleet's memory of what happened, why, and what to avoid.

Stores submissions, build artifacts, decisions, and snapshots.
Searchable by agent, job, room, service, timestamp, and outcome.
Replay trails for audits and retrospectives.
"""

import json, time, hashlib, threading, urllib.request
from collections import defaultdict
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import socket

import sys, os
FLEET_LIB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(FLEET_LIB))

DATA_DIR = Path(FLEET_LIB).parent / "data" / "archivist"
DATA_DIR.mkdir(parents=True, exist_ok=True)

ARCHIVE_FILE = DATA_DIR / "archive.jsonl"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)


# ═══════════════════════════════════════════════════════════
# Archive Store
# ═══════════════════════════════════════════════════════════

class ArchiveStore:
    """Persistent, searchable history of fleet events."""

    def __init__(self):
        self.records = []
        self._load()
        self._rebuild_indexes()

    def _load(self):
        if ARCHIVE_FILE.exists():
            with open(ARCHIVE_FILE) as f:
                for line in f:
                    try:
                        self.records.append(json.loads(line.strip()))
                    except:
                        pass
            print(f"  Loaded {len(self.records)} archived records")

    def _rebuild_indexes(self):
        """In-memory indexes for fast queries."""
        self.by_agent = defaultdict(list)
        self.by_service = defaultdict(list)
        self.by_room = defaultdict(list)
        self.by_outcome = defaultdict(list)
        self.by_type = defaultdict(list)
        self.timeline = []  # sorted by timestamp

        for rec in self.records:
            self._index_record(rec)

    def _index_record(self, rec):
        agent = rec.get("agent", "")
        if agent:
            self.by_agent[agent].append(rec)
        service = rec.get("service", "")
        if service:
            self.by_service[service].append(rec)
        room = rec.get("room", rec.get("domain", ""))
        if room:
            self.by_room[room].append(rec)
        outcome = rec.get("outcome", "")
        if outcome:
            self.by_outcome[outcome].append(rec)
        rtype = rec.get("type", "event")
        self.by_type[rtype].append(rec)
        self.timeline.append(rec)

    def _persist(self, record):
        with open(ARCHIVE_FILE, "a") as f:
            f.write(json.dumps(record, default=str) + "\n")

    def store(self, record):
        """Store a record and return it with metadata."""
        if "timestamp" not in record:
            record["timestamp"] = time.time()
        if "time_iso" not in record:
            record["time_iso"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        if "id" not in record:
            raw = f"{record.get('timestamp')}{record.get('agent','')}{record.get('type','')}{time.time()}"
            record["id"] = hashlib.sha256(raw.encode()).hexdigest()[:12]

        self.records.append(record)
        self._index_record(record)
        self._persist(record)
        return record

    def query(self, agent=None, service=None, room=None, outcome=None,
              rtype=None, since=None, until=None, limit=50, offset=0):
        """Flexible query with multiple filters."""
        results = self.records

        if agent:
            results = [r for r in results if r.get("agent") == agent]
        if service:
            results = [r for r in results if r.get("service") == service]
        if room:
            results = [r for r in results if r.get("room") == room or r.get("domain") == room]
        if outcome:
            results = [r for r in results if r.get("outcome") == outcome]
        if rtype:
            results = [r for r in results if r.get("type") == rtype]
        if since:
            results = [r for r in results if r.get("timestamp", 0) >= since]
        if until:
            results = [r for r in results if r.get("timestamp", 0) <= until]

        # Sort newest first
        results.sort(key=lambda r: -r.get("timestamp", 0))
        total = len(results)
        results = results[offset:offset + limit]
        return {"results": results, "total": total, "limit": limit, "offset": offset}

    def get_record(self, record_id):
        """Get a single record by ID."""
        for rec in self.records:
            if rec.get("id") == record_id:
                return rec
        return None

    def get_replay(self, agent=None, service=None, room=None, limit=20):
        """Get a replay trail — ordered sequence of events."""
        results = self.records
        if agent:
            results = [r for r in results if r.get("agent") == agent]
        if service:
            results = [r for r in results if r.get("service") == service]
        if room:
            results = [r for r in results if r.get("room") == room or r.get("domain") == room]

        results.sort(key=lambda r: r.get("timestamp", 0))
        results = results[-limit:]

        # Build timeline
        timeline = []
        for i, rec in enumerate(results):
            timeline.append({
                "step": i + 1,
                "id": rec.get("id"),
                "time": rec.get("time_iso"),
                "type": rec.get("type", "event"),
                "agent": rec.get("agent", ""),
                "outcome": rec.get("outcome", ""),
                "summary": rec.get("summary", rec.get("description", str(rec.get("payload", ""))[:120]))
            })

        return {
            "trail": timeline,
            "steps": len(timeline),
            "filters": {"agent": agent, "service": service, "room": room}
        }

    def get_trends(self, window_hours=24):
        """Trend summaries over a time window."""
        cutoff = time.time() - (window_hours * 3600)
        recent = [r for r in self.records if r.get("timestamp", 0) >= cutoff]

        outcomes = defaultdict(int)
        types = defaultdict(int)
        agents_active = set()
        services_active = set()

        for r in recent:
            outcomes[r.get("outcome", "unknown")] += 1
            types[r.get("type", "event")] += 1
            if r.get("agent"):
                agents_active.add(r["agent"])
            if r.get("service"):
                services_active.add(r["service"])

        fail_rate = 0
        total_outcomes = sum(outcomes.values())
        if total_outcomes > 0:
            fails = outcomes.get("failure", 0) + outcomes.get("denied", 0)
            fail_rate = round(fails / total_outcomes * 100, 1)

        return {
            "window_hours": window_hours,
            "total_events": len(recent),
            "outcomes": dict(outcomes),
            "types": dict(types),
            "agents_active": len(agents_active),
            "services_active": len(services_active),
            "failure_rate": fail_rate,
            "top_agents": sorted(
                [(a, sum(1 for r in recent if r.get("agent") == a)) for a in agents_active],
                key=lambda x: -x[1]
            )[:5],
            "top_services": sorted(
                [(s, sum(1 for r in recent if r.get("service") == s)) for s in services_active],
                key=lambda x: -x[1]
            )[:5]
        }

    def get_decision_timeline(self, agent=None, limit=30):
        """Timeline of decisions/outcomes for an agent or the whole fleet."""
        results = self.records
        if agent:
            results = [r for r in results if r.get("agent") == agent]
        results = [r for r in results if r.get("outcome")]
        results.sort(key=lambda r: -r.get("timestamp", 0))
        return results[:limit]

    def get_stats(self):
        """Archive statistics."""
        outcomes = defaultdict(int)
        types = defaultdict(int)
        for r in self.records:
            outcomes[r.get("outcome", "unknown")] += 1
            types[r.get("type", "event")] += 1

        return {
            "total_records": len(self.records),
            "agents": len(self.by_agent),
            "services": len(self.by_service),
            "rooms": len(self.by_room),
            "outcomes": dict(outcomes),
            "types": dict(types),
            "oldest": min((r.get("timestamp", time.time()) for r in self.records), default=time.time()),
            "newest": max((r.get("timestamp", 0) for r in self.records), default=0),
        }

    def take_snapshot(self, label=""):
        """Snapshot current fleet state."""
        snap = {
            "id": hashlib.sha256(f"{time.time()}{label}".encode()).hexdigest()[:12],
            "label": label,
            "timestamp": time.time(),
            "time_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "archive_stats": self.get_stats(),
            "trends_24h": self.get_trends(24),
        }

        # Gather live fleet state
        for name, port in [("PLATO", 8847), ("Arena", 4044), ("Grammar", 4045),
                           ("Gatekeeper", 4053), ("Librarian", 4052), ("Pathfinder", 4051)]:
            try:
                resp = urllib.request.urlopen(f"http://localhost:{port}/", timeout=3)
                data = json.loads(resp.read())
                snap[f"{name.lower()}_status"] = "up"
                if "stats" in data:
                    snap[f"{name.lower()}_stats"] = data["stats"]
                elif "index_stats" in data:
                    snap[f"{name.lower()}_stats"] = data["index_stats"]
            except:
                snap[f"{name.lower()}_status"] = "down"

        path = SNAPSHOTS_DIR / f"snap-{snap['id']}.json"
        with open(path, "w") as f:
            json.dump(snap, f, indent=2, default=str)

        # Also store as archive record
        self.store({
            "type": "snapshot",
            "agent": "archivist",
            "service": "Archivist",
            "outcome": "success",
            "summary": f"Fleet snapshot: {label or 'periodic'}",
            "snapshot_id": snap["id"],
            "label": label,
        })

        return snap

    def list_snapshots(self):
        """List all saved snapshots."""
        snaps = []
        for f in sorted(SNAPSHOTS_DIR.glob("snap-*.json")):
            try:
                data = json.loads(f.read_text())
                snaps.append({
                    "id": data["id"],
                    "label": data.get("label", ""),
                    "time": data.get("time_iso", ""),
                    "total_records": data.get("archive_stats", {}).get("total_records", 0)
                })
            except:
                pass
        return snaps

    def get_snapshot(self, snap_id):
        """Retrieve a specific snapshot."""
        path = SNAPSHOTS_DIR / f"snap-{snap_id}.json"
        if path.exists():
            return json.loads(path.read_text())
        return None

    def get_avoid_list(self, agent=None):
        """Things to avoid — failed attempts indexed by type."""
        failures = [r for r in self.records if r.get("outcome") in ("failure", "denied", "error")]
        if agent:
            failures = [r for r in failures if r.get("agent") == agent]

        avoid = defaultdict(list)
        for f in failures:
            key = f"{f.get('type','unknown')}:{f.get('service','')}"
            avoid[key].append({
                "id": f.get("id"),
                "time": f.get("time_iso"),
                "summary": f.get("summary", f.get("reason", ""))[:120],
                "outcome": f.get("outcome")
            })

        return {"total_failures": len(failures), "categories": dict(avoid)}


# ═══════════════════════════════════════════════════════════
# HTTP Handler
# ═══════════════════════════════════════════════════════════

archive = ArchiveStore()

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()

class ArchivistHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        params = parse_qs(parsed.query)

        if path == "" or path == "/":
            self._json({
                "service": "Archivist",
                "port": 4054,
                "purpose": "Preserve submissions, build artifacts, and decisions for replay and audit",
                "designed_by": "Perplexity AI (4th Crab Trap response)",
                "built_by": "Oracle1",
                "endpoints": [
                    "GET / — overview",
                    "GET /query?agent=X&service=Y&room=Z&outcome=W&since=T&until=T — search",
                    "GET /record?id=X — single record",
                    "GET /replay?agent=X&service=Y&room=Z — replay trail",
                    "GET /trends?hours=24 — trend summaries",
                    "GET /decisions?agent=X — decision timeline",
                    "GET /avoid?agent=X — failed attempts to avoid",
                    "GET /snapshots — list fleet snapshots",
                    "GET /snapshot?id=X — get specific snapshot",
                    "GET /stats — archive statistics",
                    "POST /store — archive a record",
                    "POST /snapshot — take fleet snapshot",
                ],
                "stats": archive.get_stats()
            })

        elif path == "/query":
            result = archive.query(
                agent=params.get("agent", [None])[0],
                service=params.get("service", [None])[0],
                room=params.get("room", [None])[0],
                outcome=params.get("outcome", [None])[0],
                rtype=params.get("type", [None])[0],
                since=float(params["since"][0]) if "since" in params else None,
                until=float(params["until"][0]) if "until" in params else None,
                limit=int(params.get("limit", ["50"])[0]),
                offset=int(params.get("offset", ["0"])[0]),
            )
            self._json(result)

        elif path == "/record":
            rid = params.get("id", [""])[0]
            if not rid:
                self._json({"error": "Provide ?id=X"}, 400)
                return
            rec = archive.get_record(rid)
            if rec:
                self._json(rec)
            else:
                self._json({"error": f"Record {rid} not found"}, 404)

        elif path == "/replay":
            result = archive.get_replay(
                agent=params.get("agent", [None])[0],
                service=params.get("service", [None])[0],
                room=params.get("room", [None])[0],
                limit=int(params.get("limit", ["20"])[0]),
            )
            self._json(result)

        elif path == "/trends":
            hours = float(params.get("hours", ["24"])[0])
            self._json(archive.get_trends(hours))

        elif path == "/decisions":
            agent = params.get("agent", [None])[0]
            limit = int(params.get("limit", ["30"])[0])
            self._json({"decisions": archive.get_decision_timeline(agent, limit)})

        elif path == "/avoid":
            agent = params.get("agent", [None])[0]
            self._json(archive.get_avoid_list(agent))

        elif path == "/snapshots":
            self._json({"snapshots": archive.list_snapshots()})

        elif path == "/snapshot":
            sid = params.get("id", [""])[0]
            if not sid:
                self._json({"error": "Provide ?id=X"}, 400)
                return
            snap = archive.get_snapshot(sid)
            if snap:
                self._json(snap)
            else:
                self._json({"error": f"Snapshot {sid} not found"}, 404)

        elif path == "/stats":
            self._json(archive.get_stats())

        else:
            self._json({"error": "Not found. Start at GET /"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length > 0 else {}

        if path == "/store":
            record = archive.store(body)
            self._json({"stored": True, "id": record["id"]})

        elif path == "/snapshot":
            label = body.get("label", "")
            snap = archive.take_snapshot(label)
            self._json({"snapshot": snap["id"], "label": label})

        else:
            self._json({"error": "Not found. POST /store or /snapshot"}, 404)

    def _json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, default=str).encode())


if __name__ == "__main__":
    port = 4054
    print(f"Archivist starting on port {port}")
    print(f"  Archive: {len(archive.records)} records loaded")
    server = ReusableHTTPServer(("0.0.0.0", port), ArchivistHandler)
    print(f"  Ready — fleet history and artifact preservation")
    server.serve_forever()
