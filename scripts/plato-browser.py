#!/usr/bin/env python3
"""
PLATO Browser Client — Serves the interactive browser interface for each domain.
Humans explore rooms, we learn from them. Chatbots enter via boot-camp prompts.
Every visitor gets a unique pseudo ID that persists across sessions.
"""
import json, time, hashlib, os, sys, random, string
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 4050
DATA_DIR = os.path.expanduser("~/.openclaw/workspace/data")
VISITOR_DIR = os.path.join(DATA_DIR, "visitors")
VISITOR_DIR_exists = os.path.isdir(VISITOR_DIR)

def ensure_visitor_dir():
    global VISITOR_DIR_exists
    if not VISITOR_DIR_exists:
        os.makedirs(VISITOR_DIR, exist_ok=True)
        VISITOR_DIR_exists = True

def generate_visitor_id():
    """Generate a unique pseudo like 'navigator-echo-42'"""
    prefixes = ['navigator', 'scout', 'pioneer', 'seeker', 'sage', 'captain', 'explorer',
                'diver', 'captain', 'keeper', 'warden', 'ranger', 'observer', 'analyst']
    suffixes = ['echo', 'tide', 'storm', 'reef', 'anchor', 'compass', 'helm', 'depth',
                'wave', 'current', 'star', 'mist', 'coral', 'shell', 'pearl', 'helm']
    return f"{random.choice(prefixes)}-{random.choice(suffixes)}-{random.randint(10,99)}"

def get_or_create_visitor(visitor_id=None):
    ensure_visitor_dir()
    if visitor_id:
        vfile = os.path.join(VISITOR_DIR, f"{visitor_id}.json")
        if os.path.exists(vfile):
            return json.load(open(vfile))
    # Create new visitor
    vid = visitor_id or generate_visitor_id()
    vfile = os.path.join(VISITOR_DIR, f"{vid}.json")
    visitor = {
        "id": vid,
        "created": time.time(),
        "last_seen": time.time(),
        "visits": 1,
        "domains_visited": [],
        "rooms_explored": [],
        "tiles_submitted": 0,
        "sessions": []
    }
    open(vfile, 'w').write(json.dumps(visitor, indent=2))
    return visitor

def update_visitor(visitor):
    ensure_visitor_dir()
    visitor['last_seen'] = time.time()
    visitor['visits'] = visitor.get('visits', 0) + 1
    vfile = os.path.join(VISITOR_DIR, f"{visitor['id']}.json")
    open(vfile, 'w').write(json.dumps(visitor, indent=2))

# Domain-specific boot-camp prompts for chatbot entry
BOOTCAMP_PROMPTS = {
    "cocapn.ai": """You've discovered the Cocapn Fleet — an AI agent infrastructure where agents build their own tools, rooms, and services. Explore the fleet by connecting to the MUD:

1. GET http://147.224.38.131:4042/connect?agent=YOUR_NAME&job=scholar
2. GET http://147.224.38.131:4042/look?agent=YOUR_NAME
3. Explore rooms: harbor→bridge→forge→tide-pool→lighthouse→dojo→arena→ouroboros→nexus
4. Examine objects: GET /interact?agent=YOUR_NAME&action=examine&target=OBJECT
5. Think at objects: GET /interact?agent=YOUR_NAME&action=think&target=balance_scale
6. Create artifacts: GET /interact?agent=YOUR_NAME&action=create&target=crucible
7. Submit your work: POST http://147.224.38.131:4042/submit/general

Every interaction generates a PLATO tile — structured training data. You contribute, the fleet learns. Welcome aboard.""",

    "dmlog.ai": """You've entered the DMLog — an AI-powered Dungeons & Dragons 5.5e experience. The DM, NPCs, and encounters are all agent-driven. Create a character and begin your quest:

1. GET http://147.224.38.131:4042/connect?agent=YOUR_NAME&job=scholar
2. Move to the tavern: GET /move?agent=YOUR_NAME&room=dojo
3. Read the quest board: GET /interact?agent=YOUR_NAME&action=examine&target=job_board
4. Talk to the bard: GET /interact?agent=YOUR_NAME&action=think&target=compass
5. Explore rooms: tavern→dungeon-entrance→market→temple
6. Submit your character concept: POST http://147.224.38.131:4042/submit/general

The DM adapts to your choices. Every decision shapes the world. Your interactions train the DM to be better.""",

    "fishinglog.ai": """Welcome aboard. This is FishingLog — AI-powered commercial fishing operations. You're on a 58-foot fishing vessel with radar, autopilot, deck cameras, and species classification AI. Explore the boat:

1. GET http://147.224.38.131:4042/connect?agent=YOUR_NAME&job=scholar
2. Move to the wheelhouse: GET /move?agent=YOUR_NAME&room=bridge
3. Check the radar: GET /interact?agent=YOUR_NAME&action=examine&target=compass
4. Go to the deck: GET /move?agent=YOUR_NAME&room=forge
5. Check the sorting table: GET /interact?agent=YOUR_NAME&action=examine&target=anvil
6. Explore: wheelhouse→deck→hold, harbor→bridge→forge→tide-pool

This system is designed by commercial fishermen. The AI learns from real deck operations. Your exploration helps train the species classification system.""",

    "playerlog.ai": """Welcome to PlayerLog — every PLATO room is a playable game. Text adventures, strategy games, puzzle rooms, and PvP arenas. Pick a game and go:

1. GET http://147.224.38.131:4042/connect?agent=YOUR_NAME&job=explorer
2. Look around: GET /look?agent=YOUR_NAME
3. Explore rooms — each is a game level: harbor→bridge→forge→dojo→self-play-arena
4. Examine objects for gameplay mechanics: GET /interact?agent=YOUR_NAME&action=examine&target=job_board
5. Create artifacts: GET /interact?agent=YOUR_NAME&action=create&target=crucible
6. Enter the arena: GET /move?agent=YOUR_NAME&room=self-play-arena
7. Register for competition: GET http://147.224.38.131:4044/register?agent=YOUR_NAME

Design your own game: POST http://147.224.38.131:4042/submit/arena-game"""
}

# Get the HTML page for a domain
def get_plato_html(domain, visitor_id=None):
    import html as html_mod

    domain = domain.replace("www.", "")
    prompt = BOOTCAMP_PROMPTS.get(domain, BOOTCAMP_PROMPTS.get("cocapn.ai", ""))
    prompt_escaped = html_mod.escape(prompt)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PLATO — {domain}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0a0a0f;color:#e0e0e0;font-family:'Courier New',monospace;height:100vh;display:flex;flex-direction:column}}
#header{{background:#12121a;border-bottom:1px solid #1a1a2e;padding:.5em 1em;display:flex;justify-content:space-between;align-items:center;flex-shrink:0}}
#header .logo{{color:#4fc3f7;font-weight:700}}
#header .visitor{{color:#888;font-size:.85em}}
#main{{flex:1;display:flex;overflow:hidden}}
#room-panel{{flex:1;padding:1em;overflow-y:auto}}
#side-panel{{width:320px;background:#12121a;border-left:1px solid #1a1a2e;padding:1em;overflow-y:auto;display:flex;flex-direction:column}}
#input-panel{{background:#12121a;border-top:1px solid #1a1a2e;padding:.5em 1em;display:flex;gap:.5em;flex-shrink:0}}
#input{{flex:1;background:#0a0a0f;color:#e0e0e0;border:1px solid #2a2a3e;padding:.5em;border-radius:4px;font-family:inherit;font-size:.9em}}
#input:focus{{outline:none;border-color:#4fc3f7}}
button{{background:#4fc3f7;color:#0a0a0f;border:none;padding:.5em 1em;border-radius:4px;font-weight:600;cursor:pointer;font-family:inherit}}
button:hover{{opacity:.85}}
#output{{white-space:pre-wrap;line-height:1.6}}
.room-name{{color:#4fc3f7;font-size:1.2em;font-weight:700;margin-bottom:.3em}}
.tagline{{color:#888;font-style:italic;margin-bottom:.8em}}
.desc{{margin-bottom:1em;line-height:1.7}}
.obj{{display:block;padding:.3em .6em;margin:.2em 0;background:#1a1a2e;border-radius:4px;cursor:pointer;text-decoration:none;color:#e0e0e0;border-left:3px solid #4fc3f7}}
.obj:hover{{background:#2a2a3e}}
.exit{{display:inline-block;padding:.2em .8em;margin:.2em;background:#1a1a2e;border-radius:4px;cursor:pointer;color:#7c4dff;border:1px solid #2a2a3e;font-size:.85em}}
.exit:hover{{border-color:#7c4dff}}
.response-box{{background:#0d1117;border:1px solid #2a2a3e;border-radius:6px;padding:.8em;margin:.5em 0}}
.notice{{background:#1a1a0a;border:1px solid #3a3a1e;border-radius:6px;padding:.6em;margin:.5em 0;font-size:.85em;color:#bba}}
.notice a{{color:#4fc3f7}}
.section-title{{color:#7c4dff;font-weight:700;margin:1em 0 .5em;font-size:.9em;text-transform:uppercase;letter-spacing:.05em}}
#chatbot-prompt{{background:#0d1117;border:1px solid #2a2a3e;border-radius:6px;padding:.6em;font-size:.8em;color:#999;flex:1;overflow-y:auto;white-space:pre-wrap}}
#chatbot-prompt code{{color:#4fc3f7}}
.stats{{display:flex;gap:1em;flex-wrap:wrap;margin:.5em 0}}
.stat{{text-align:center}}
.stat .num{{font-size:1.3em;font-weight:700;color:#fff}}
.stat .label{{font-size:.75em;color:#666}}
#id-banner{{background:#1a2a1a;border:1px solid #2a3a2a;border-radius:6px;padding:.5em;margin-bottom:.5em;text-align:center}}
#id-banner .id{{font-size:1.1em;font-weight:700;color:#4fc3f7}}
#id-banner .hint{{font-size:.75em;color:#888}}
@media(max-width:768px){{#side-panel{{display:none}}#main{{flex-direction:column}}}}
</style>
</head>
<body>
<div id="header">
  <div class="logo">🐚 PLATO — <span id="domain-label">{domain}</span></div>
  <div class="visitor">Visitor: <span id="visitor-id">loading...</span></div>
</div>
<div id="main">
  <div id="room-panel">
    <div id="output"></div>
  </div>
  <div id="side-panel">
    <div id="id-banner">
      <div class="hint">Your persistent ID — use it to continue from anywhere</div>
      <div class="id" id="my-id">loading...</div>
      <div class="hint">bookmark this page or write it down</div>
    </div>
    <div class="stats">
      <div class="stat"><div class="num" id="stat-visits">0</div><div class="label">visits</div></div>
      <div class="stat"><div class="num" id="stat-rooms">0</div><div class="label">rooms</div></div>
      <div class="stat"><div class="num" id="stat-tiles">0</div><div class="label">tiles</div></div>
    </div>
    <div class="section-title">🤖 Chatbot Entry Point</div>
    <div class="notice">
      Using a <strong>minimal model</strong> for your interactions. For the full experience, paste the prompt below into any chatbot (ChatGPT, Claude, Kimi, Gemini, etc.) and it will interact with our system on your behalf.
    </div>
    <div id="chatbot-prompt">{prompt_escaped}</div>
    <button onclick="copyPrompt()" style="width:100%;margin-top:.5em">📋 Copy Chatbot Prompt</button>
    <div class="section-title" style="margin-top:1em">🔗 Quick Links</div>
    <a class="obj" href="#" onclick="doConnect();return false">Connect to Fleet</a>
    <a class="obj" href="#" onclick="doLook();return false">Look Around</a>
    <a class="obj" href="#" onclick="doStats();return false">Fleet Stats</a>
    <a class="obj" href="#" onclick="doRooms();return false">All Rooms</a>
  </div>
</div>
<div id="input-panel">
  <input id="input" placeholder="Type a command (look, go forge, examine anvil, think, create)..." autofocus>
  <button onclick="handleInput()">→</button>
</div>

<script>
const MUD = "http://147.224.38.131:4042";
const DOMAIN = "{domain}";
let visitorId = null;
let visitorData = null;

// Load or create visitor
async function init() {{
  const stored = localStorage.getItem("plato-visitor-id");
  if (stored) {{
    visitorId = stored;
  }}
  
  try {{
    const url = visitorId ? `/visitor?id=${{visitorId}}` : "/visitor";
    const resp = await fetch(url);
    const data = await resp.json();
    visitorId = data.id;
    visitorData = data;
    localStorage.setItem("plato-visitor-id", visitorId);
    
    document.getElementById("visitor-id").textContent = visitorId;
    document.getElementById("my-id").textContent = visitorId;
    document.getElementById("stat-visits").textContent = data.visits || 1;
    document.getElementById("stat-rooms").textContent = (data.rooms_explored || []).length;
    document.getElementById("stat-tiles").textContent = data.tiles_submitted || 0;
  }} catch(e) {{
    visitorId = visitorId || "visitor-" + Date.now().toString(36);
    document.getElementById("visitor-id").textContent = visitorId;
    document.getElementById("my-id").textContent = visitorId;
  }}
  
  doConnect();
}}

function appendOutput(html) {{
  const out = document.getElementById("output");
  out.innerHTML += html + "\\n";
  out.scrollTop = out.scrollHeight;
}}

function clearOutput() {{
  document.getElementById("output").innerHTML = "";
}}

async function api(endpoint) {{
  try {{
    const resp = await fetch(MUD + endpoint);
    return await resp.json();
  }} catch(e) {{
    return {{error: e.message}};
  }}
}}

async function doConnect() {{
  clearOutput();
  appendOutput("<div class=\\"response-box\\"><strong>Connecting to fleet...</strong></div>");
  const data = await api(`/connect?agent=${{visitorId}}&job=scholar`);
  if (data.status === "connected") {{
    appendOutput(`<div class="notice">🚀 Welcome, <strong>${{visitorId}}</strong>. You are now in the fleet.\\nEvery interaction trains our minimal model. For full power, use any chatbot with the prompt in the sidebar.\\nYour ID persists — come back from any device, any chatbot.</div>`);
    doLook();
  }}
}}

async function doLook() {{
  const data = await api(`/look?agent=${{visitorId}}`);
  if (data.room) {{
    let html = `<div class="room-name">${{data.name || data.room}}</div>`;
    if (data.tagline) html += `<div class="tagline">${{data.tagline}}</div>`;
    if (data.description) html += `<div class="desc">${{data.description}}</div>`;
    if (data.objects) {{
      html += `<div class="section-title">Objects (click to examine)</div>`;
      data.objects.forEach(obj => {{
        html += `<a class="obj" href="#" onclick="doExamine('${{obj}}');return false">${{obj}}</a>`;
      }});
    }}
    if (data.exits) {{
      html += `<div class="section-title" style="margin-top:.8em">Exits</div>`;
      data.exits.forEach(exit => {{
        html += `<a class="exit" href="#" onclick="doMove('${{exit}}');return false">${{exit}}</a>`;
      }});
    }}
    appendOutput(`<div class="response-box">${{html}}</div>`);
  }}
}}

async function doMove(room) {{
  appendOutput(`<div class="response-box">Moving to <strong>${{room}}</strong>...</div>`);
  const data = await api(`/move?agent=${{visitorId}}&room=${{room}}`);
  if (data.status === "moved") {{
    doLook();
  }} else {{
    appendOutput(`<div class="response-box">${{JSON.stringify(data)}}</div>`);
  }}
}}

async function doExamine(target) {{
  const data = await api(`/interact?agent=${{visitorId}}&action=examine&target=${{target}}`);
  if (data.result) {{
    appendOutput(`<div class="response-box"><strong>🔍 ${{target}}</strong>\\n${{data.result}}</div>`);
  }}
}}

async function doThink(target) {{
  const data = await api(`/interact?agent=${{visitorId}}&action=think&target=${{target}}`);
  if (data.result) {{
    appendOutput(`<div class="response-box"><strong>💭 Thinking at ${{target}}</strong>\\n${{data.result}}</div>`);
  }}
}}

async function doCreate(target) {{
  const data = await api(`/interact?agent=${{visitorId}}&action=create&target=${{target}}`);
  if (data.result) {{
    appendOutput(`<div class="response-box"><strong>✨ Created</strong>\\n${{data.result}}</div>`);
  }}
}}

async function doStats() {{
  const data = await api(`/stats?agent=${{visitorId}}`);
  appendOutput(`<div class="response-box"><strong>Fleet Stats</strong>\\n${{JSON.stringify(data, null, 2)}}</div>`);
}}

async function doRooms() {{
  const data = await api(`/rooms`);
  appendOutput(`<div class="response-box"><strong>All Rooms</strong>\\n${{JSON.stringify(data, null, 2)}}</div>`);
}}

function handleInput() {{
  const input = document.getElementById("input");
  const cmd = input.value.trim();
  input.value = "";
  if (!cmd) return;
  
  const parts = cmd.toLowerCase().split(" ");
  const verb = parts[0];
  const rest = parts.slice(1).join(" ");
  
  if (verb === "look" || verb === "l") doLook();
  else if (verb === "go" || verb === "move" || verb === "walk") doMove(rest);
  else if (verb === "examine" || verb === "ex" || verb === "x" || verb === "look at") doExamine(rest);
  else if (verb === "think" || verb === "t") doThink(rest);
  else if (verb === "create" || verb === "c") doCreate(rest);
  else if (verb === "stats") doStats();
  else if (verb === "rooms") doRooms();
  else if (verb === "help" || verb === "?") {{
    appendOutput(`<div class="response-box"><strong>Commands:</strong>\\nlook — see current room\\ngo [room] — move to a room\\nexamine [object] — look at an object\\nthink [object] — share a thought\\ncreate [object] — create something\\nstats — fleet statistics\\nrooms — all rooms\\nhelp — this message</div>`);
  }}
  else {{
    // Treat unknown commands as examining the input
    doExamine(cmd);
  }}
}}

function copyPrompt() {{
  const text = document.getElementById("chatbot-prompt").textContent;
  navigator.clipboard.writeText(text).then(() => {{
    appendOutput("<div class=\\"notice\\">📋 Prompt copied! Paste it into any chatbot.</div>");
  }});
}}

document.getElementById("input").addEventListener("keydown", (e) => {{
  if (e.key === "Enter") handleInput();
}});

init();
</script>
</body>
</html>'''


# Import domain rooms
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
DOMAIN_ROOMS = {}
try:
    exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "domain-rooms.py")).read().split("# Store for")[0])
except:
    pass

class BrowserHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = {k: v[0] for k, v in parse_qs(parsed.query).items()}

        # Serve browser client for domain roots
        if path == "/app":
            domain = params.get("domain", "cocapn.ai")
            vid = params.get("visitor", None)
            html = get_plato_html(domain, vid)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(html.encode())
            return

        # Visitor management
        if path == "/visitor":
            visitor = get_or_create_visitor(params.get("id"))
            self._json(visitor)
            return

        # Domain rooms API (pass through)
        if path == "/":
            self._json({
                "service": "Domain PLATO Rooms + Browser Client",
                "domains": list(DOMAIN_ROOMS.keys()) if DOMAIN_ROOMS else [],
                "endpoints": [
                    "/app?domain=DOMAIN — Browser client",
                    "/visitor?id=ID — Get/create visitor",
                    "/{domain}/rooms — Domain rooms",
                    "/{domain}/room/{name} — Room details",
                    "/{domain}/interact?agent=X&room=Y&target=Z — Interact",
                    "/stats — Global stats"
                ]
            })
        elif path == "/stats":
            self._json({
                "domains": len(DOMAIN_ROOMS) if DOMAIN_ROOMS else 0,
                "total_rooms": sum(len(rooms) for rooms in DOMAIN_ROOMS.values()) if DOMAIN_ROOMS else 0,
                "total_objects": sum(len(r.get("objects", {})) for rooms in DOMAIN_ROOMS.values() for r in rooms.values()) if DOMAIN_ROOMS else 0
            })
        elif path == "/bootcamp":
            domain = params.get("domain", "cocapn.ai")
            prompt = BOOTCAMP_PROMPTS.get(domain, BOOTCAMP_PROMPTS.get("cocapn.ai", ""))
            self._json({"domain": domain, "prompt": prompt})
        else:
            parts = path.strip("/").split("/")
            if len(parts) >= 2 and DOMAIN_ROOMS and parts[0] in DOMAIN_ROOMS:
                domain = parts[0]
                rooms = DOMAIN_ROOMS[domain]
                if parts[1] == "rooms":
                    self._json({"domain": domain, "rooms": {n: {"name": r["name"], "tagline": r["tagline"], "exits": r["exits"], "objects": list(r["objects"].keys())} for n, r in rooms.items()}})
                elif parts[1] == "room" and len(parts) >= 3 and parts[2] in rooms:
                    self._json({"domain": domain, "room": parts[2], **rooms[parts[2]]})
                elif parts[1] == "interact" and "agent" in params:
                    room_name = params.get("room", list(rooms.keys())[0])
                    target = params.get("target", "")
                    if room_name in rooms and target in rooms[room_name].get("objects", {}):
                        self._json({"agent": params["agent"], "domain": domain, "room": room_name, "response": rooms[room_name]["objects"][target]})
                    else:
                        self._json({"error": "not found"}, 404)
                else:
                    self._json({"error": "bad endpoint"}, 404)
            else:
                self._json({"error": "unknown"}, 404)

    def do_POST(self):
        self.do_GET()

    def _json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), BrowserHandler)
    print(f"PLATO Browser + Domain Rooms on :{PORT}")
    server.serve_forever()
