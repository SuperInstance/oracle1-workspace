# PLATO-NG Troubleshooting

## Server Won't Start

**Symptom**: `python3 lib/server.py` returns immediately or hangs.

**Check**: Is port 8847 already in use?
```bash
ss -tlnp | grep 8847
```
If yes, a server is already running. Kill it with the PID shown.

**Check**: Is Python 3.10+ available?
```bash
python3 --version
```

## Can't Connect to MUD

**Symptom**: `telnet localhost 7777` fails.

**Check**: Is the MUD server running?
```bash
ss -tlnp | grep 7777
```
If not: `python3 services/mud_telnet.py &`

**Check**: Is telnet installed?
```bash
which telnet
# If not: sudo apt-get install telnet
```

## PLATO Submit Returns 403

**Symptom**: Tile submission returns HTTP 403.

**Check**: Is your answer long enough (>20 chars)? PLATO's P0 gate requires minimum answer length.
```bash
curl -X POST http://localhost:8847/submit \
  -H "Content-Type: application/json" \
  -d '{"domain":"test","question":"test","answer":"this answer is longer than 20 characters so it should pass the gate","tags":["test"],"source":"test","confidence":0.5}'
```

**Check**: Is your confidence >= 0.1? The P1 gate requires this.

**Check**: Does your tile have tags? The P2 gate requires at least one tag.

## Conservation Monitor Shows Violations

**Symptom**: Conservation monitor reports violations.

**Most violations are false positives** from early tiles submitted before the law was formalized. Check the violation details:
```bash
curl http://localhost:8847/room/research_log/history | grep conservation/violations
```
If the violation tile lacks `_meta.gamma` and `_meta.H` fields, it's a pre-law tile that couldn't be checked.

## Game Room Returns Wrong Results

**Symptom**: Tournament results are 100-0-0 (always the same winner).

**This is correct** for solved games. Connect Four is solved (first player always wins with perfect play). Tic-tac-toe is solved (perfect play always draws). Checkers is weakly solved. Only Othello has meaningful strategy differences at the AI level chosen.

**Check**: Are both strategies actually different?
```python
# Verify strategies produce different moves
from games.othello_room import OthelloRoom
room = OthelloRoom()
board = room.new_board()
move1 = room.strat_positional(board, room.P1)
move2 = room.strat_mobility(board, room.P1)
print(move1, move2)  # Should differ
```

## Crush Room Not Responding

**Symptom**: Submitted a crush/task tile but no crush/ok or crush/fail tile appears.

**Check**: Is the daemon running?
```bash
ps aux | grep crush_room | grep -v grep
```

**Check**: Has the daemon processed your tile?
```bash
tail -5 /tmp/crush-daemon-v2.log
```

**Restart**: `pkill -f crush_room; nohup python3 services/crush_room.py --daemon > /tmp/crush-daemon-v2.log 2>&1 &`

## A2Ui Message Fails

**Symptom**: `message_from_dict()` raises an exception.

**Check**: Your JSON has at minimum `version` and `intent` fields.
```python
from lib.a2ui import message_from_dict
msg = message_from_dict({"version": "1.0", "intent": "render"})  # This should work
```

**Check**: For the `render` intent, a `ui` dict with `components` is expected.

## Memory Crystal Won't Forget

**Symptom**: `crystal.forget()` returns 0 even with old memories.

**Check**: The `forget()` method removes memories with retention < 0.1. Retention decays based on the Ebbinghaus curve. To force forgetting:
```python
crystal.memories.clear()  # Deletes ALL memories
```

## PLATO-Redis Can't Find Keys

**Symptom**: GET returns nothing after SET.

**Check**: The store is in memory and resets when the server restarts. For persistence, use PLATO tiles:
```python
# The store auto-saves to /tmp/plato-mcp-redis.json
# Check if that file exists
import os; os.path.exists("/tmp/plato-mcp-redis.json")
```
