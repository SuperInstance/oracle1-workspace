"""
Equipment Layer — Matrix Fleet Chat Client.
Shared across all services that send/receive Matrix messages.
Python 3.10, zero external dependencies.
"""
import json
import time
import urllib.request


class MatrixClient:
    """Client for Conduwuit Matrix homeserver."""
    
    def __init__(self, server="http://127.0.0.1:6167", token=None, 
                 server_name="147.224.38.131"):
        self.server = server
        self.token = token
        self.server_name = server_name
    
    def _headers(self):
        h = {"Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h
    
    def send_message(self, room_id, body, msgtype="m.text"):
        """Send a text message to a room."""
        txn = str(int(time.time() * 1000))
        full_room = f"{room_id}:{self.server_name}"
        url = f"{self.server}/_matrix/client/v3/rooms/{full_room}/send/m.room.message/{txn}"
        data = json.dumps({"msgtype": msgtype, "body": body}).encode()
        req = urllib.request.Request(url, data=data, method="PUT")
        for k, v in self._headers().items():
            req.add_header(k, v)
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    
    def get_messages(self, room_id, limit=10):
        """Get recent messages from a room."""
        full_room = f"{room_id}:{self.server_name}"
        url = f"{self.server}/_matrix/client/v3/rooms/{full_room}/messages?limit={limit}&dir=b"
        req = urllib.request.Request(url)
        for k, v in self._headers().items():
            req.add_header(k, v)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("chunk", [])
    
    def join_room(self, room_id):
        """Join a room."""
        full_room = f"{room_id}:{self.server_name}"
        url = f"{self.server}/_matrix/client/v3/join/{full_room}"
        req = urllib.request.Request(url, data=b"{}", method="POST")
        for k, v in self._headers().items():
            req.add_header(k, v)
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
