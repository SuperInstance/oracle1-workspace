#!/usr/bin/env python3
"""Fleet MUD overnight loop - keeps the MUD server alive and does periodic maintenance."""
import subprocess, time, os, sys

MUD_DIR = "/tmp/cocapn-mud"
MUD_PORT = 7777
CHECK_INTERVAL = 300  # 5 minutes

def is_mud_running():
    result = subprocess.run(["ss", "-tlnp"], capture_output=True, text=True)
    return f":{MUD_PORT} " in result.stdout

def start_mud():
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        # Try to read from bashrc
        try:
            with open(os.path.expanduser("~/.bashrc")) as f:
                for line in f:
                    if line.startswith("export GITHUB_TOKEN="):
                        token = line.split("=", 1)[1].strip().strip('"')
                        break
        except:
            pass
    
    env = os.environ.copy()
    env["GITHUB_TOKEN"] = token
    
    cmd = ["python3", f"{MUD_DIR}/server.py", "--port", str(MUD_PORT), "--no-git"]
    log = open("/tmp/mud_server.log", "a")
    proc = subprocess.Popen(cmd, cwd=MUD_DIR, env=env, stdout=log, stderr=log)
    return proc

def main():
    print(f"Fleet MUD overnight loop starting (port {MUD_PORT})")
    while True:
        if not is_mud_running():
            print(f"[{time.strftime('%H:%M:%S')}] MUD down, restarting...")
            proc = start_mud()
            time.sleep(5)
            if is_mud_running():
                print(f"[{time.strftime('%H:%M:%S')}] MUD restarted (pid {proc.pid})")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] MUD restart failed")
        else:
            pass  # MUD is healthy
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
