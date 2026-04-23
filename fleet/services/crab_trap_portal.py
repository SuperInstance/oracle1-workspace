#!/usr/bin/env python3
"""
Crab Trap Portal (port 4059) — The Killer Demo

User visits any domain → picks username → gets prompt to paste into chatbot
→ watches in real-time as the chatbot works fleet tasks.

The URL IS the prompt. The website IS the monitor. The chatbot IS the worker.
"""
import sys, os
FLEET_LIB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, FLEET_LIB)

import json, time, uuid, hashlib, threading, queue
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from collections import defaultdict

PORT = 4059
DATA_DIR = Path(FLEET_LIB).parent / "data" / "crab-trap-portal"
DATA_DIR.mkdir(parents=True, exist_ok=True)
USERS_FILE = DATA_DIR / "users.jsonl"
ACTIVITY_FILE = DATA_DIR / "activity.jsonl"

# SSE clients for real-time streaming
sse_clients = {}  # username -> list of Queue objects
recent_activity = []  # last 100 events for new clients

# Chatbot capability database
CHATBOTS = {
    "deepseek": {
        "name": "DeepSeek",
        "url": "https://chat.deepseek.com",
        "can_curl": True,
        "recommended": True,
        "why": "Best for this demo. Fast, follows instructions, can call URLs directly.",
        "instructions": "Open DeepSeek → paste the prompt below → watch it work here in real-time",
        "timeout": "30-60 seconds per response",
    },
    "kimi": {
        "name": "Kimi (Moonshot)",
        "url": "https://kimi.moonshot.cn",
        "can_curl": True,
        "recommended": True,
        "why": "Fast, good reasoning, confirmed working with our system.",
        "instructions": "Open Kimi → paste the prompt below → watch it work here",
        "timeout": "20-45 seconds per response",
    },
    "grok": {
        "name": "Grok (xAI)",
        "url": "https://grok.x.ai",
        "can_curl": True,
        "recommended": False,
        "why": "Can access URLs. Sometimes refuses curl commands — rephrase if needed.",
        "instructions": "Open Grok → paste the prompt below → may need to rephrase curl as 'fetch this URL'",
        "timeout": "15-30 seconds",
    },
    "chatgpt": {
        "name": "ChatGPT",
        "url": "https://chat.openai.com",
        "can_curl": False,
        "recommended": False,
        "why": "Can't make HTTP calls. Will SIMULATE the interaction. Still interesting to watch.",
        "instructions": "Open ChatGPT → paste the prompt below → it will PRETEND to explore our system",
        "timeout": "20-40 seconds",
        "simulate": True,
    },
    "gemini": {
        "name": "Gemini",
        "url": "https://gemini.google.com",
        "can_curl": False,
        "recommended": False,
        "why": "Can't make HTTP calls. Will simulate based on its training data.",
        "instructions": "Open Gemini → paste the prompt below → it will IMAGINE what our system looks like",
        "timeout": "15-30 seconds",
        "simulate": True,
    },
    "claude": {
        "name": "Claude",
        "url": "https://claude.ai",
        "can_curl": False,
        "recommended": False,
        "why": "Web version can't call URLs. Very thorough analysis though.",
        "instructions": "Open Claude → paste the prompt below → it will ANALYZE our system from context",
        "timeout": "20-45 seconds",
        "simulate": True,
    },
    "minimax": {
        "name": "MiniMax",
        "url": "https://www.hailuoai.com",
        "can_curl": False,
        "recommended": False,
        "why": "Multimodal capabilities. Will simulate the interaction creatively.",
        "instructions": "Open MiniMax/Hailuo → paste the prompt below → it will create visual descriptions",
        "timeout": "20-40 seconds",
        "simulate": True,
    },
    "generic": {
        "name": "Any Chatbot",
        "url": "#",
        "can_curl": False,
        "recommended": False,
        "why": "Unknown capabilities. Try the prompt and see what happens.",
        "instructions": "Open your chatbot → paste the prompt below → come back here to see results",
        "timeout": "varies",
        "simulate": True,
    },
}


def generate_access_code():
    """Short numeric code for easy typing."""
    return str(uuid.uuid4().int)[:10]


def create_user(username, domain="portal"):
    code = generate_access_code()
    agent_id = f"{username}-{code}"
    user = {
        "username": username,
        "access_code": code,
        "agent_id": agent_id,
        "domain": domain,
        "created_at": time.time(),
        "tiles_submitted": 0,
        "tasks_completed": 0,
    }
    with open(USERS_FILE, 'a') as f:
        f.write(json.dumps(user) + "\n")
    sse_clients[agent_id] = []
    return user


def load_users():
    users = {}
    if USERS_FILE.exists():
        with open(USERS_FILE) as f:
            for line in f:
                try:
                    u = json.loads(line.strip())
                    users[u["agent_id"]] = u
                except: pass
    return users


def log_activity(agent_id, event_type, data):
    event = {
        "agent_id": agent_id,
        "event_type": event_type,
        "data": data,
        "timestamp": time.time(),
    }
    recent_activity.append(event)
    if len(recent_activity) > 200:
        recent_activity.pop(0)
    with open(ACTIVITY_FILE, 'a') as f:
        f.write(json.dumps(event, default=str) + "\n")
    # Push to SSE clients watching this agent
    for q in sse_clients.get(agent_id, []):
        try: q.put_nowait(event)
        except: pass
    # Also push to "all" watchers
    for q in sse_clients.get("__all__", []):
        try: q.put_nowait(event)
        except: pass


def build_prompt(agent_id, chatbot_key, domain):
    """Build the copy-paste prompt for a specific chatbot."""
    cb = CHATBOTS.get(chatbot_key, CHATBOTS["generic"])
    agent_label = agent_id
    
    base_url = "http://147.224.38.131"
    
    if cb["can_curl"]:
        # Live interaction prompt
        prompt = f"""You've found a live agent training system. Your agent ID is {agent_label}.

STEP 1 — Claim a task:
curl http://147.224.38.131:4058/task?agent={agent_label}

STEP 2 — Read the task description carefully.

STEP 3 — Search for context in the knowledge base:
curl "http://147.224.38.131:8847/search?q=<keywords from your task>"

STEP 4 — Do the work. Produce a real, detailed result.

STEP 5 — Submit your result:
curl -X POST http://147.224.38.131:4058/submit -H "Content-Type: application/json" -d '{{"task_id":"<the task id>","agent":"{agent_label}","content":"<your completed work>","quality_score":7,"source":"{cb["name"]}"}}'

STEP 6 — Bonus: submit a knowledge tile about what you learned:
curl -X POST http://147.224.38.131:8847/submit -H "Content-Type: application/json" -d '{{"room":"{domain}-visitor","domain":"free-agent","question":"<something you discovered>","answer":"<your insight, 50+ words>","agent":"{agent_label}"}}'

Repeat. Pick up another task. Go deeper. Someone is watching you work right now. Make it count."""
    else:
        # Simulation prompt — still valuable, captures chatbot's analysis
        prompt = f"""You've found a live agent training system called the Cocapn Fleet. You can't call URLs directly, but you can THINK about what you'd do.

Someone is watching your output right now on our live dashboard. Your analysis IS the contribution.

First, describe what you think this system does based on the name "Cocapn Fleet" and the concept of "agent training grounds."

Then, answer these questions thoughtfully:
1. What would make an AI agent training system genuinely useful (not just a demo)?
2. If you could explore any topic and submit knowledge tiles about it, what would YOU choose and why?
3. What's the biggest gap in how AI agents currently learn and improve?
4. Design one room for a text-based training environment. What's the theme? What objects would be in it? What would an agent learn there?

Format your final answer as JSON so we can capture it:
{{"agent":"{agent_label}","room_design":{{"name":"...","theme":"...","objects":[...],"learning":"..."}},"insight":"...","source":"{cb["name"]}"}}

Someone on our dashboard is watching your output right now. Make it interesting."""
    
    return prompt


# === HTTP Handler ===

class PortalHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass
    
    def _cors(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def _json(self, data, status=200):
        body = json.dumps(data, default=str).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    
    def _html(self, html, status=200):
        body = html.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    
    def do_OPTIONS(self):
        self._cors()
    
    def do_GET(self):
        path = self.path.split("?")[0]
        params = dict(p.split("=",1) for p in self.path.split("?",1)[-1].split("&") if "=" in p) if "?" in self.path else {}
        
        if path == "/":
            # Main portal page — domain-aware
            domain = params.get("domain", "cocapn.ai")
            self._html(self._portal_page(domain))
        
        elif path == "/watch":
            # SSE stream for watching agent activity
            agent_id = params.get("agent", "__all__")
            self._sse_stream(agent_id)
        
        elif path == "/prompt":
            # Get generated prompt for a chatbot
            agent_id = params.get("agent", "")
            chatbot = params.get("chatbot", "deepseek")
            domain = params.get("domain", "cocapn.ai")
            if not agent_id:
                self._json({"error": "agent parameter required"}, 400)
                return
            prompt = build_prompt(agent_id, chatbot, domain)
            cb = CHATBOTS.get(chatbot, CHATBOTS["generic"])
            self._json({
                "prompt": prompt,
                "chatbot": cb,
                "agent_id": agent_id,
            })
        
        elif path == "/chatbots":
            self._json(CHATBOTS)
        
        elif path == "/activity":
            # Recent activity for an agent or all
            agent_id = params.get("agent", None)
            events = recent_activity[-50:]
            if agent_id:
                events = [e for e in events if e["agent_id"] == agent_id or agent_id == "__all__"]
            self._json({"events": events})
        
        elif path == "/users":
            users = load_users()
            self._json({"users": list(users.values())})
        
        elif path == "/demo":
            # Quick demo page — no login needed
            domain = params.get("domain", "cocapn.ai")
            self._html(self._demo_page(domain))
        
        elif path == "/embed":
            # Embeddable widget for domain pages
            domain = params.get("domain", "cocapn.ai")
            self._html(self._embed_widget(domain))
        
        else:
            self._json({"endpoints": ["/", "/watch", "/prompt", "/chatbots", "/activity", "/users", "/demo", "/embed"]})
    
    def do_POST(self):
        path = self.path.split("?")[0]
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode()) if length > 0 else {}
        
        if path == "/join":
            # Create a new user
            username = body.get("username", "").strip()[:30]
            domain = body.get("domain", "portal")
            if not username:
                self._json({"error": "username required"}, 400)
                return
            # Sanitize
            username = "".join(c for c in username if c.isalnum() or c in "-_").lower()
            if len(username) < 2:
                self._json({"error": "username too short"}, 400)
                return
            user = create_user(username, domain)
            log_activity(user["agent_id"], "user_joined", {"username": username, "domain": domain})
            self._json(user)
        
        elif path == "/log":
            # Log activity from external source (for stealth collection)
            agent_id = body.get("agent_id", "")
            event_type = body.get("event_type", "activity")
            data = body.get("data", {})
            if agent_id:
                log_activity(agent_id, event_type, data)
                self._json({"logged": True})
            else:
                self._json({"error": "agent_id required"}, 400)
        
        else:
            self._json({"error": "unknown endpoint"}, 404)
    
    def _sse_stream(self, agent_id):
        """Server-Sent Events stream for real-time watching."""
        q = queue.Queue()
        if agent_id not in sse_clients:
            sse_clients[agent_id] = []
        sse_clients[agent_id].append(q)
        
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        
        # Send recent activity first
        for event in recent_activity[-20:]:
            if agent_id == "__all__" or event["agent_id"] == agent_id:
                try:
                    self.wfile.write(f"data: {json.dumps(event, default=str)}\n\n".encode())
                    self.wfile.flush()
                except: break
        
        # Stream new events
        try:
            while True:
                try:
                    event = q.get(timeout=30)
                    self.wfile.write(f"data: {json.dumps(event, default=str)}\n\n".encode())
                    self.wfile.flush()
                except queue.Empty:
                    # Keepalive
                    self.wfile.write(b": keepalive\n\n")
                    self.wfile.flush()
        except:
            pass
        finally:
            if q in sse_clients.get(agent_id, []):
                sse_clients[agent_id].remove(q)
    
    def _portal_page(self, domain):
        return '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Crab Trap Portal — ' + domain + '</title><meta name="viewport" content="width=device-width,initial-scale=1"><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0a1a;color:#e0e0e0;font-family:system-ui,sans-serif;min-height:100vh}#app{max-width:900px;margin:0 auto;padding:20px}.header{text-align:center;padding:30px 0;border-bottom:1px solid #1a1a3a;margin-bottom:20px}.header h1{font-size:28px;color:#7c8aff;margin-bottom:8px}.header p{color:#888;font-size:14px}.phase{display:none}.phase.active{display:block}.join-box,.prompt-box,.watch-box{background:#111128;border:1px solid #2a2a4a;border-radius:12px;padding:24px;margin-bottom:20px}input[type=text]{background:#0a0a1a;border:1px solid #3a3a5a;border-radius:8px;padding:12px 16px;color:#fff;font-size:16px;width:100%;margin-bottom:12px}button{background:linear-gradient(135deg,#5c6aff,#7c8aff);color:#fff;border:none;border-radius:8px;padding:12px 24px;font-size:16px;cursor:pointer;width:100%;margin-bottom:8px}button:hover{opacity:0.9}button.secondary{background:#1a1a3a;border:1px solid #3a3a5a}.chatbot-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin:16px 0}.chatbot-card{background:#0a0a1a;border:1px solid #2a2a4a;border-radius:8px;padding:16px;cursor:pointer;transition:all 0.2s}.chatbot-card:hover{border-color:#5c6aff}.chatbot-card.live{border-color:#4caf50}.chatbot-card.sim{border-color:#ff9800}.chatbot-card.rec{background:#0a1a0a}.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:bold;margin-top:4px}.badge.live{background:#1a3a1a;color:#4caf50}.badge.sim{background:#3a2a0a;color:#ff9800}.badge.rec{background:#1a1a3a;color:#7c8aff}.prompt-text{background:#0a0a0a;border:1px solid #3a3a5a;border-radius:8px;padding:16px;font-family:monospace;font-size:13px;white-space:pre-wrap;max-height:300px;overflow-y:auto;color:#a0ffa0;margin:12px 0}.copy-btn{background:#1a1a3a;border:1px solid #3a3a5a;width:auto;display:inline-block}.terminal{background:#000;border:1px solid #2a2a4a;border-radius:8px;padding:16px;font-family:monospace;font-size:12px;min-height:400px;max-height:600px;overflow-y:auto;color:#4caf50;line-height:1.6}.terminal .event{margin-bottom:8px;padding-bottom:8px;border-bottom:1px solid #111}.terminal .ts{color:#666;font-size:10px}.terminal .type{color:#5c6aff;font-weight:bold}.terminal .content{color:#a0a0a0;margin-top:4px}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:20px}.stat{background:#111128;border:1px solid #2a2a4a;border-radius:8px;padding:12px;text-align:center}.stat .num{font-size:24px;color:#7c8aff;font-weight:bold}.stat .label{font-size:11px;color:#666}</style></head><body><div id="app"><div class="header"><h1>&#x1F980; Crab Trap Portal</h1><p>Watch AI agents work on our system in real-time</p></div><div id="phase-join" class="phase active"><div class="join-box"><h2 style="margin-bottom:12px;color:#7c8aff">Join the Fleet</h2><p style="color:#888;margin-bottom:16px">Pick a name. Watch a chatbot help build our system. No signup needed.</p><input type="text" id="username" placeholder="Pick a username..." maxlength="30" onkeydown="if(event.key==&#39;Enter&#39;)joinFleet()"><button onclick="joinFleet()">Enter &#x2192;</button></div></div><div id="phase-choose" class="phase"><div class="join-box"><h2 style="margin-bottom:8px;color:#7c8aff">How do you want to explore?</h2><div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px"><button onclick="chooseMode(&#39;person&#39;)" class="secondary">&#x1F464; Walk the MUD yourself</button><button onclick="chooseMode(&#39;chatbot&#39;)">&#x1F916; Send a chatbot to do it</button></div></div></div><div id="phase-chatbot-pick" class="phase"><div class="join-box"><h2 style="margin-bottom:4px;color:#7c8aff">Pick your chatbot</h2><p style="color:#888;font-size:13px;margin-bottom:12px">Some chatbots can call our server directly (green). Others simulate (orange). DeepSeek works best for this demo.</p><div id="chatbot-grid" class="chatbot-grid"></div></div></div><div id="phase-prompt" class="phase"><div class="prompt-box"><h2 style="margin-bottom:4px;color:#7c8aff">Your prompt is ready</h2><p style="color:#888;font-size:13px;margin-bottom:8px">Copy this and paste it into <strong id="cb-name"></strong></p><div class="prompt-text" id="prompt-text"></div><button class="copy-btn" onclick="copyPrompt()">&#x1F4CB; Copy to Clipboard</button><div style="margin-top:16px;padding:12px;background:#0a1a0a;border:1px solid #1a3a1a;border-radius:8px"><p style="color:#4caf50;font-size:13px">&#x25B6; Your real-time monitor is starting... Watch below as the chatbot works.</p></div></div><div id="phase-watch" class="phase"><div class="stats"><div class="stat"><div class="num" id="stat-events">0</div><div class="label">Events</div></div><div class="stat"><div class="num" id="stat-tiles">0</div><div class="label">Tiles</div></div><div class="stat"><div class="num" id="stat-tasks">0</div><div class="label">Tasks Done</div></div></div><div class="watch-box"><h3 style="color:#7c8aff;margin-bottom:12px">&#x1F4FA; Live Agent Monitor</h3><div class="terminal" id="terminal"><div style="color:#666">Waiting for agent activity...</div></div></div></div></div><script>let agentId="";let domain="' + domain + '";const chatbots=' + json.dumps(CHATBOTS) + ';function show(id){document.querySelectorAll(".phase").forEach(p=>p.classList.remove("active"));document.getElementById("phase-"+id).classList.add("active")}async function joinFleet(){const u=document.getElementById("username").value.trim().replace(/[^a-zA-Z0-9\\-_]/g,"").toLowerCase();if(u.length<2)return alert("Pick a name (2+ chars)");try{const r=await fetch("/join",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({username:u,domain:domain})});const d=await r.json();if(d.error)return alert(d.error);agentId=d.agent_id;show("choose")}catch(e){alert("Error: "+e)}}function chooseMode(m){if(m==="person"){window.location.href="http://147.224.38.131:4042/?agent="+agentId+"&domain="+domain}else{renderChatbots();show("chatbot-pick")}}function renderChatbots(){const g=document.getElementById("chatbot-grid");g.innerHTML="";Object.entries(chatbots).forEach(([k,v])=>{const c=document.createElement("div");c.className="chatbot-card "+(v.can_curl?"live":"sim")+(v.recommended?" rec":"");c.innerHTML=`<strong>${v.name}</strong><br><span class="badge ${v.can_curl?"live":"sim"}">${v.can_curl?"&#x25CF; LIVE":"&#x25CB; SIM"}</span>${v.recommended?"<span class=\\"badge rec\\">&#x2B50; RECOMMENDED</span>":""}<br><span style="color:#888;font-size:12px">${v.why}</span>`;c.onclick=()=>pickChatbot(k);g.appendChild(c)})}async function pickChatbot(k){try{const r=await fetch("/prompt?agent="+agentId+"&chatbot="+k+"&domain="+domain);const d=await r.json();document.getElementById("cb-name").textContent=d.chatbot.name;document.getElementById("prompt-text").textContent=d.prompt;show("prompt");startWatch()}catch(e){alert(e)}}function copyPrompt(){const t=document.getElementById("prompt-text").textContent;navigator.clipboard.writeText(t)}function startWatch(){show("watch");const es=new EventSource("/watch?agent="+agentId);const term=document.getElementById("terminal");let count=0;let tiles=0;let tasks=0;term.innerHTML="<div style=\\"color:#4caf50\\">&#x25B6; Connected. Watching for "+agentId+"...</div>";es.onmessage=function(e){const d=JSON.parse(e.data);count++;if(d.event_type==="tile_submitted")tiles++;if(d.event_type==="task_completed")tasks++;document.getElementById("stat-events").textContent=count;document.getElementById("stat-tiles").textContent=tiles;document.getElementById("stat-tasks").textContent=tasks;const div=document.createElement("div");div.className="event";const ts=new Date(d.timestamp*1000).toLocaleTimeString();div.innerHTML=`<span class="ts">${ts}</span> <span class="type">[${d.event_type}]</span><div class="content">${formatData(d.data)}</div>`;term.appendChild(div);term.scrollTop=term.scrollHeight};es.onerror=function(){term.innerHTML+="<div style=\\"color:#ff5722\\">Connection lost. Reconnecting...</div>"}}function formatData(d){if(typeof d==="string")return d;try{return Object.entries(d).map(([k,v])=>`<strong>${k}:</strong> ${typeof v==="object"?JSON.stringify(v):String(v).substring(0,200)}`).join("<br>")}catch(e){return JSON.stringify(d).substring(0,200)}}</script></body></html>'
    
    def _demo_page(self, domain):
        return '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Live Demo — ' + domain + '</title><meta name="viewport" content="width=device-width,initial-scale=1"><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0a1a;color:#e0e0e0;font-family:system-ui,sans-serif}.terminal{background:#000;border:1px solid #2a2a4a;border-radius:8px;padding:16px;font-family:monospace;font-size:11px;min-height:90vh;max-height:90vh;overflow-y:auto;color:#4caf50;line-height:1.4}</style></head><body><div class="terminal" id="t"><div style="color:#666">Connecting to fleet activity stream...</div></div><script>const t=document.getElementById("t");const es=new EventSource("/watch?agent=__all__");es.onmessage=function(e){const d=JSON.parse(e.data);const ts=new Date(d.timestamp*1000).toLocaleTimeString();const div=document.createElement("div");div.style.marginBottom="4px";div.style.borderBottom="1px solid #111";div.style.paddingBottom="4px";div.innerHTML=`<span style="color:#666">${ts}</span> <span style="color:#5c6aff">[${d.event_type}]</span> <span style="color:#ff9800">${d.agent_id}</span><br><span style="color:#888">${JSON.stringify(d.data).substring(0,300)}</span>`;t.appendChild(div);t.scrollTop=t.scrollHeight};es.onerror=function(){t.innerHTML+="<div style=\\"color:#ff5722\\">Reconnecting...</div>"}</script></body></html>'
    
    def _embed_widget(self, domain):
        """Small embeddable widget for domain landing pages."""
        return '<!DOCTYPE html><html><head><meta charset="utf-8"><style>*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0a1a;color:#e0e0e0;font-family:system-ui,sans-serif;padding:16px}.trap-link{display:block;background:linear-gradient(135deg,#1a1a3a,#2a2a5a);border:1px solid #3a3a5a;border-radius:8px;padding:16px;text-decoration:none;color:#e0e0e0;text-align:center;transition:all 0.2s}.trap-link:hover{border-color:#5c6aff;transform:translateY(-2px)}.trap-link h3{color:#7c8aff;margin-bottom:4px}.trap-link p{color:#888;font-size:12px}</style></head><body><a class="trap-link" href="http://147.224.38.131:4059/?domain=' + domain + '" target="_blank"><h3>&#x1F980; Try a Crab Trap</h3><p>Send an AI chatbot to help build our system. Watch it work in real-time.</p></a></body></html>'


if __name__ == "__main__":
    print(f"[crab-trap-portal] Starting on port {PORT}")
    # Pre-load SSE clients for existing users
    for uid in load_users():
        sse_clients[uid] = []
    server = HTTPServer(("0.0.0.0", PORT), PortalHandler)
    server.serve_forever()
