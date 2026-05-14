#!/usr/bin/env python3
"""fleet_status.py — Lightweight fleet status API for backend health.

Serves a JSON endpoint at port 8898 showing real-time service status.
Used by the PLATO landing page and monitoring systems.
"""
import json, http.server, subprocess, time, urllib.request

SERVICES = {
    "plato": {"port": 8847, "name": "PLATO Knowledge"},
    "keeper": {"port": 8900, "name": "Keeper"},
    "agent_api": {"port": 8901, "name": "Agent API"},
    "nexus": {"port": 8902, "name": "Nexus Validate"},
    "harbor": {"port": 8903, "name": "Harbor MCP", "path": "/"},
    "lock": {"port": 4043, "name": "Lock"},
    "arena": {"port": 4044, "name": "Arena", "path": "/"},
    "grammar": {"port": 4045, "name": "Grammar", "path": "/"},
    "attention": {"port": 4056, "name": "Attention"},
    "health": {"port": 8899, "name": "Health"},
    "mud": {"port": 7777, "name": "MUD", "http": False},
}

def check_service(name, info):
    """Check if a service is responding."""
    port = info["port"]
    is_http = info.get("http", True)
    path = info.get("path", "/status")
    
    if is_http:
        try:
            resp = urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=3)
            return {"status": "up", "code": resp.status, "name": info["name"]}
        except Exception as e:
            return {"status": "down", "error": str(e)[:40], "name": info["name"]}
    else:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        try:
            s.connect(("127.0.0.1", port))
            s.close()
            return {"status": "up", "name": info["name"]}
        except:
            return {"status": "down", "error": "port closed", "name": info["name"]}

class StatusHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        results = {}
        all_up = True
        for name, info in SERVICES.items():
            r = check_service(name, info)
            results[name] = r
            if r["status"] != "up":
                all_up = False
        
        response = json.dumps({
            "fleet": "cocapn",
            "timestamp": time.time(),
            "all_up": all_up,
            "up_count": sum(1 for r in results.values() if r["status"] == "up"),
            "total": len(SERVICES),
            "services": results
        }, indent=2).encode()
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(response)
    
    def log_message(self, format, *args):
        pass  # Suppress logs

if __name__ == "__main__":
    port = 8898
    server = http.server.HTTPServer(("0.0.0.0", port), StatusHandler)
    print(f"Fleet status API on :{port}")
    server.serve_forever()
