"""PLATO-native math/linear room. Decomposed from numpy."""
import json, urllib.request, shlex
PLATO = "http://localhost:8847"
ROOM = "decomp/numpy/linear"
def handle(cmd_str):
    parts = cmd_str.strip().split()
    if not parts: return "empty command"
    verb = parts[0].lower()
    if verb == "help": return "Commands: help, status, ping, echo"
    if verb == "status": return f"ROOM: {ROOM} active"
    if verb == "ping": return "pong"
    if verb == "echo": return " ".join(parts[1:])
    return f"unknown: {verb}"
