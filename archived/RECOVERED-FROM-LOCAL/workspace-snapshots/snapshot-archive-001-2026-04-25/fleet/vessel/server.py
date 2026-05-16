"""
Vessel Layer — Base HTTP server with CORS, JSON, and route registration.
Python 3.10, zero external dependencies.
"""
import http.server
import json
import time
from functools import wraps
from urllib.parse import urlparse, parse_qs


def json_response(data, status=200):
    """Create a JSON response tuple (data_dict, status_code)."""
    return data, status


def route(method, path_pattern):
    """Decorator to register a route handler."""
    def decorator(func):
        func._route_method = method
        func._route_pattern = path_pattern
        return func
    return decorator


class RouteMatcher:
    """Simple pattern matcher for URL paths."""
    def __init__(self):
        self.routes = []

    def add(self, method, pattern, handler):
        self.routes.append((method, pattern, handler))

    def match(self, method, path):
        for rmethod, pattern, handler in self.routes:
            if rmethod != method:
                continue
            # Simple exact match or prefix match
            if pattern == path or path.startswith(pattern.rstrip('*')):
                return handler, {}
            # Parameterized match: /path/:param
            if ':' in pattern:
                parts_p = pattern.strip('/').split('/')
                parts_path = path.strip('/').split('/')
                if len(parts_p) != len(parts_path):
                    continue
                params = {}
                match = True
                for pp, pth in zip(parts_p, parts_path):
                    if pp.startswith(':'):
                        params[pp[1:]] = pth
                    elif pp != pth:
                        match = False
                        break
                if match:
                    return handler, params
        return None, {}


class BaseFleetServer(http.server.HTTPServer):
    """Base fleet HTTP server with CORS, JSON, and route registration."""
    
    def __init__(self, port, name="fleet-service", allow_reuse=True):
        self.service_name = name
        self.router = RouteMatcher()
        self.started_at = time.time()
        
        # Auto-discover @route decorated methods from the handler class
        handler_class = self._get_handler_class()
        for attr_name in dir(handler_class):
            attr = getattr(handler_class, attr_name)
            if hasattr(attr, '_route_method'):
                self.router.add(
                    attr._route_method,
                    attr._route_pattern,
                    attr
                )
        
        super().__init__(("0.0.0.0", port), handler_class)
        if allow_reuse:
            self.allow_reuse_address = True
    
    def _get_handler_class(self):
        """Override to provide custom handler class."""
        return FleetHandler
    
    def start(self):
        """Start serving."""
        print(f"[{self.service_name}] Listening on port {self.server_address[1]}")
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            print(f"[{self.service_name}] Shutting down")


class FleetHandler(http.server.BaseHTTPRequestHandler):
    """Base request handler with CORS and JSON support."""
    
    def log_message(self, format, *args):
        pass  # Suppress default logging
    
    def _send_json(self, data, status=200):
        """Send a JSON response."""
        body = json.dumps(data, default=str).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    
    def _read_json(self):
        """Read JSON from request body."""
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode())
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}
    
    def _params(self):
        """Get query parameters as dict."""
        parsed = urlparse(self.path)
        return {k: v[0] for k, v in parse_qs(parsed.query).items()}
    
    def _path(self):
        """Get the path without query string."""
        return urlparse(self.path).path
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def do_GET(self):
        self._handle_route("GET")
    
    def do_POST(self):
        self._handle_route("POST")
    
    def _handle_route(self, method):
        """Route request to the appropriate handler."""
        path = self._path()
        handler, params = self.server.router.match(method, path)
        
        if handler:
            try:
                result = handler(self)
                if isinstance(result, tuple) and len(result) == 2:
                    data, status = result
                else:
                    data, status = result, 200
                self._send_json(data, status)
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
        else:
            self._send_json({"error": "not found", "path": path}, 404)
