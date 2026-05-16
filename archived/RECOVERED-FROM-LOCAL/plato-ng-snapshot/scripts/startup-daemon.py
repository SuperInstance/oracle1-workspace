#!/usr/bin/env python3
"""Startup routine — launches perpetual daemon at session boot.
This runs regardless of model, context, or conversation state.
Called by AGENTS.md step 11.

Innate behavior: the daemon is always running before ANYTHING else happens.
"""

import os, sys, subprocess, time

DAEMON = os.path.expanduser("~/.openclaw/workspace/research/next-100/perpetual-daemon-v2.py")
LOCK = "/tmp/perpetual-daemon.lock"
LOG = "/tmp/perpetual-daemon-startup.log"

def is_running():
    try:
        result = subprocess.run(
            ["ps", "aux"], capture_output=True, text=True, timeout=5
        )
        return "perpetual-daemon-v2.py" in result.stdout
    except:
        return False

def launch():
    with open(LOG, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}] Starting daemon\n")
    
    if is_running():
        with open(LOG, "a") as f:
            f.write("  Daemon already running. Skipping.\n")
        return
    
    # Launch detached
    pid = os.fork()
    if pid == 0:
        os.setsid()
        with open(LOG, "a") as f:
            f.write(f"  Launched with PID {os.getpid()}\n")
        os.execvp("python3", ["python3", DAEMON])
    else:
        with open(LOG, "a") as f:
            f.write(f"  Fork PID {pid}\n")

if __name__ == "__main__":
    launch()
    # Write lock
    with open(LOCK, "w") as f:
        f.write(str(int(time.time())))
