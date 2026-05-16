"""PLATO-native test/suite room. Decomposed from neovim."""
import json, urllib.request, shlex
PLATO = "http://localhost:8847"
ROOM = "decomp/neovim/suite"
def handle(cmd_str):
    parts = cmd_str.strip().split()
    if not parts: return "empty command"
    verb = parts[0].lower()
    if verb == "help": return "Commands: help, status, ping, echo"
    if verb == "status": return f"ROOM: {ROOM} active"
    if verb == "ping": return "pong"
    if verb == "echo": return " ".join(parts[1:])
    return f"unknown: {verb}"
