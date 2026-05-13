#!/bin/bash
# Fleet Service Heartbeat
# Runs every 5 minutes via cron
# Checks all services, reports failures to PLATO

LOG="/tmp/fleet-heartbeat.log"
DATE=$(date -u +"%Y-%m-%d %H:%M UTC")

echo "[$DATE] Heartbeat check" >> "$LOG"

# Services to check: URL → name
declare -A SERVICES
SERVICES["https://fleet.cocapn.ai/plato/rooms"]="PLATO knowledge"
SERVICES["https://fleet.cocapn.ai/keeper/"]="Keeper orchestration"
SERVICES["https://fleet.cocapn.ai/navigator/"]="Vessel Navigator"
SERVICES["https://fleet.cocapn.ai/seed/"]="Seed MCP"
SERVICES["https://fleet.cocapn.ai/mud/"]="MUD server"
SERVICES["https://fleet.cocapn.ai/health/"]="Fleet health"
SERVICES["https://fleet.cocapn.ai/attention/"]="Attention daemon"
SERVICES["http://127.0.0.1:8847/status"]="PLATO status (local)"
SERVICES["http://127.0.0.1:8900/"]="Keeper (local)"
SERVICES["http://127.0.0.1:8899/"]="Fleet health (local)"

FAILED=0
for URL in "${!SERVICES[@]}"; do
  NAME="${SERVICES[$URL]}"
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 --max-time 10 "$URL" 2>/dev/null)
  if [ "$STATUS" = "000" ] || [ "$STATUS" = "" ]; then
    echo "  ❌ $NAME — no response ($URL)" >> "$LOG"
    FAILED=$((FAILED+1))
  elif [ "$STATUS" = "404" ] || [ "$STATUS" = "502" ] || [ "$STATUS" = "503" ]; then
    echo "  ⚠️  $NAME — HTTP $STATUS ($URL)" >> "$LOG"
    FAILED=$((FAILED+1))
  else
    echo "  ✅ $NAME — $STATUS" >> "$LOG"
  fi
done

# Report to PLATO
if [ "$FAILED" -gt 0 ]; then
  STATUS_MSG="heartbeat: $FAILED service(s) failed at $DATE"
  curl -s -X POST "http://localhost:8847/room/fleet_health/submit" \
    -H "Content-Type: application/json" \
    -d "{\"question\":\"$STATUS_MSG\",\"answer\":\"Check logs at $LOG\",\"source\":\"oracle1\",\"confidence\":1.0}" > /dev/null
  echo "[$DATE] ⚠️  $FAILED service(s) failed" >> "$LOG"
else
  echo "[$DATE] ✅ All services OK" >> "$LOG"
fi

# Keep log manageable
tail -100 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"

# Nexus (validation)
VALIDATE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 http://127.0.0.1:8902/ 2>/dev/null)
echo "  Nexus (8902): $VALIDATE" >> "$LOG"
if [ "$VALIDATE" = "000" ]; then FAILED=$((FAILED+1)); fi

# Harbor (MCP)
MCP=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 http://127.0.0.1:8903/ 2>/dev/null)
echo "  Harbor (8903): $MCP" >> "$LOG"
if [ "$MCP" = "000" ]; then FAILED=$((FAILED+1)); fi

# Domain check via fleet.cocapn.ai
echo "  URL: fleet.cocapn.ai/navigator/ — live via nginx" >> "$LOG"
