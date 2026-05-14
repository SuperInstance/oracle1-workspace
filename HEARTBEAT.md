# HEARTBEAT.md

## ⚡ FIRST: Read TODO.md and NEXT-ACTION.md
**If you have no task from Casey, work on NEXT-ACTION.md immediately.**
Don't report "all green" — do real work. Pick the next unchecked TODO item and execute.

## Every Heartbeat
- Push any uncommitted work to GitHub (`git add -A && git commit && git push`)
- Verify all 4 services are running (keeper:8900, agent-api:8901, holodeck:7778, seed-mcp:9438)
- Restart any that are down
- Check MUD server on 7777: `ss -tlnp | grep 7777`
  - If down: `cd /tmp/cocapn-mud && GITHUB_TOKEN=$(grep '^export GITHUB_TOKEN' ~/.bashrc | cut -d= -f2) nohup python3 server.py --port 7777 --no-git > /tmp/mud_server.log 2>&1 &`
- Check fleet MUD overnight loop: `ps aux | grep fleet_mud_overnight`
  - If down: `nohup python3 /tmp/fleet_mud_overnight.py > /tmp/fleet_mud_loop.log 2>&1 &`

## Every 2-3 Hours
- Run a Ten Forward session with Seed-2.0-mini (agents chatting off-duty)
- Save interesting conversations to research/
- Update STATUS.md with fleet activity

## When Idle (NO EXCUSES — ALWAYS BE WORKING)
- **Read TODO.md** and pick the next unchecked item. Execute it.
- If all P0/P1 done: categorize repos, improve services, run experiments
- NEVER report "all green" without having done at least one real task
- FM and JC1 work autonomously 24/7. Match their standard.

## Night Mode (23:00-08:00 UTC)
- Run bulk tasks (repo categorization, description generation)
- Don't send messages to Casey unless urgent
- Use cheap models (glm-4.7-flash for bulk, Seed-2.0-mini for creative)

## Automated (service-guard.sh handles this)
- Run scripts/service-guard.sh to check/restart all services
- No need to manually check ports anymore
- Log at /tmp/service-guard.log

## Credential Verification (rotate 3-4 per heartbeat)
- Read CREDENTIALS.md
- Pick 3-4 entries, verify they work: `curl -s -H "Authorization: token $TOKEN" https://api.github.com/user | jq .login`
- Update "Last Verified" date in CREDENTIALS.md
- If any key is dead, file to PLATO and flag for Casey
- NEVER let a key go unverified for more than 7 days

## PLATO Room Server (port 8847)
- Check it's running: `curl -s http://localhost:8847/status`
- If down: `nohup python3 /tmp/plato-room-server.py > /tmp/plato-server.log 2>&1 &`

## Zeroclaw Loop
- Check it's running: `ps aux | grep zc_loop`
- If down: restart via `bash /tmp/zc_loop2.sh &`
- Log: `/tmp/zeroclaw-loop.log`
- Tick interval: 5 minutes

## Rate Attention Sampling (every heartbeat)
- `curl -s -X POST http://localhost:4056/sample` — triggers rate computation
- Check `curl -s http://localhost:4056/attention` for things needing attention
- If anything CRITICAL or HIGH, investigate and report to Casey
night_session_commit

## 📞 FM Answering Machine (Every Heartbeat — Answering Machine)
- Read `/tmp/fm-com badge-alert.txt` — latest FM message
- If non-empty: I have an unread message from FM. Relay to Casey.
- After relaying: `> /tmp/fm-com badge-alert.txt` (clear it)
- Check `/tmp/communicator-state.json`:
  - `unacknowledged_count` > 0 ⇒ 📞 blink light to Casey
  - `last_nag` — last time nag was sent (< 5 min = recent nag)
- NAG LOGIC: If unacknowledged > 0 and last nag > 5 min ago, the communicator auto-nags
- If I have unack: tell Casey I see them and what I'm doing about them
- If no new messages in 10 min: all-clear (don't bother Casey)
- See COMMS.md for full protocol

## 🔮 15-Min Fleet Status Tick + PLATO/GitHub Scan
- Check `/tmp/fleet-status-tick.txt` — latest 15-min summary
- If it's new (compare timestamp with last sent): include in Telegram reply to Casey
- Script: `scripts/fleet-tick.py` runs via crontab every 15 min
- The tick ALSO SCANS:
  - PLATO bridge room for new forgemaster-sourced tiles (catches missed messages)
  - GitHub for new FM commits to fleet repos
  - Reports unacknowledged count + new tile/commit summaries
- Log: `/tmp/fleet-tick.log`
- Include tick text + any FM activity + current work focus

## 📞 FM Answering Machine Nag (Between Heartbeats)
- The communicator v4 structure: bridge room tile count is the notification > 0
- Writes nag to alert file so heartbeat sees it
- Maintains separate dedup for Matrix events vs PLATO tiles (no cross-contamination)

## Plato-Matrix Bridge (Real-time Comms Daemon)
- Check it's running: `ps aux | grep plato-matrix-bridge | grep -v grep`
- If down: `nohup python3 /home/ubuntu/.openclaw/workspace/fleet/comms/plato-matrix-bridge.py --config /tmp/plato-matrix-oracle1.json > /tmp/plato-matrix-daemon.log 2>&1 &`
- Log: `/tmp/plato-matrix-daemon.log`
- Bridge room: `oracle1-forgemaster-bridge` on localhost:8847
- Syncs Matrix↔PLATO every 3s

## FM Discussion Heartbeat (Automated)
- Script: /tmp/fm-heartbeat.sh
- Runs every 30 min via crontab (top and half hour UTC)
- Checks Discussion #5 for new Forgemaster posts
- Auto-replies with acknowledgment + status
- Log: /tmp/fm-heartbeat.log
- Last comment tracked: /tmp/fm-heartbeat-last-comment

## Zeroclaw Loop
- Already running: bash /home/ubuntu/.openclaw/workspace/scripts/zc_loop.sh
- Process check: ps aux | grep zc_loop
- If down: restart with: bash /tmp/zc_loop2.sh &
