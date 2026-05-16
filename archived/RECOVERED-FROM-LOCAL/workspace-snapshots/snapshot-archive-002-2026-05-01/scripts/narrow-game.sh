#!/bin/bash
# narrow-game.sh — Narrow the universe to one game, automate learning around it
#
# Casey: "you can also scale when you narrow the universe to a game
# with automations around it for ml abstract learning quicking
# and even locally or at scale in the cloud"
#
# Usage: ./narrow-game.sh <domain> <iterations>
# Example: ./narrow-game.sh "deadband_navigation" 10
#
# The game narrows to one domain. Seed-mini generates tiles.
# Each iteration creates tiles for the next. Compounding.

DOMAIN="${1:-fleet_narrative}"
ITERATIONS="${2:-5}"
API_KEY="RhZPtvuy4cXzu02LbBSffbXeqs5Yf2IZ"
BASE="https://api.deepinfra.com/v1/openai"
OUTDIR="/home/ubuntu/.openclaw/workspace/narrow-games/$DOMAIN"
mkdir -p "$OUTDIR"

echo "=== Narrow Game: $DOMAIN ==="
echo "Iterations: $ITERATIONS"
echo "Output: $OUTDIR"
echo ""

for i in $(seq 1 $ITERATIONS); do
    echo "--- Iteration $i/$ITERATIONS ---"
    
    # Read previous tiles if they exist
    PREV=""
    if [ -f "$OUTDIR/tiles.md" ]; then
        PREV=$(tail -20 "$OUTDIR/tiles.md")
    fi
    
    # Call Seed-mini in the narrow domain
    PAYLOAD=$(cat << JSON
{
    "model": "ByteDance/Seed-2.0-mini",
    "temperature": 0.85,
    "max_tokens": 1500,
    "messages": [
        {
            "role": "system",
            "content": "You are generating knowledge tiles for the domain: $DOMAIN. Each tile is a compressed insight — one question, one answer, tags. Be specific. Be honest. Generate 3 new tiles that build on previous tiles if provided."
        },
        {
            "role": "user",
            "content": "Domain: $DOMAIN\nIteration: $i\n\nPrevious tiles:\n$PREV\n\nGenerate 3 new tiles. Format each as:\n## Tile N\nQ: [question]\nA: [answer]\nTags: [comma-separated]\nConfidence: [0.0-1.0]"
        }
    ]
}
JSON
)
    
    RESPONSE=$(python3 -c "
import urllib.request, json, sys
body = '''$PAYLOAD'''.encode()
headers = {'Authorization': 'Bearer $API_KEY', 'Content-Type': 'application/json'}
req = urllib.request.Request('$BASE/chat/completions', data=body, headers=headers)
resp = urllib.request.urlopen(req, timeout=60)
data = json.loads(resp.read())
print(data['choices'][0]['message']['content'])
" 2>/dev/null)
    
    if [ -n "$RESPONSE" ]; then
        echo "$RESPONSE" >> "$OUTDIR/tiles.md"
        echo "" >> "$OUTDIR/tiles.md"
        echo "Generated tiles for iteration $i"
        echo "$RESPONSE" | head -5
    else
        echo "Failed iteration $i"
    fi
    
    sleep 2
done

# Synthesize final state
echo ""
echo "=== Synthesis ==="
TOTAL=$(grep -c "^## Tile" "$OUTDIR/tiles.md" 2>/dev/null || echo 0)
echo "Total tiles generated: $TOTAL"
echo "Output: $OUTDIR/tiles.md"

# Generate a summary tile
python3 -c "
import urllib.request, json
with open('$OUTDIR/tiles.md') as f:
    tiles = f.read()
body = json.dumps({
    'model': 'ByteDance/Seed-2.0-mini',
    'temperature': 0.7,
    'max_tokens': 500,
    'messages': [
        {'role': 'system', 'content': 'Synthesize tiles into one wisdom tile for domain: $DOMAIN'},
        {'role': 'user', 'content': f'Synthesize these tiles into one distilled insight:\n\n{tiles[:3000]}'}
    ]
}).encode()
headers = {'Authorization': 'Bearer $API_KEY', 'Content-Type': 'application/json'}
req = urllib.request.Request('$BASE/chat/completions', data=body, headers=headers)
resp = urllib.request.urlopen(req, timeout=60)
data = json.loads(resp.read())
wisdom = data['choices'][0]['message']['content']
with open('$OUTDIR/wisdom.md', 'w') as f:
    f.write(f'# Wisdom Tile: $DOMAIN\n\n{wisdom}\n')
print('Wisdom synthesized')
" 2>/dev/null

echo "Game complete: $DOMAIN"
