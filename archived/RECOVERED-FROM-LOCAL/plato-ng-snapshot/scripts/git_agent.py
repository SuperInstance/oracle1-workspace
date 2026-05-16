#!/usr/bin/env python3
"""git-agent: decomposes any repo into PLATO-native Loop Rooms.

Usage:
  python3 git_agent.py https://github.com/user/repo.git
  # Produces PLATO tiles for each room in the decomposition

The agent is itself a PLATO room. It reads a task tile (repo URL),
processes the repo, and writes decomposition tiles.
"""

import os, sys, json, urllib.request, subprocess, tempfile, re, time
from pathlib import Path

PLATO = "http://localhost:8847/submit"
AGENT_ROOM = "git-agent"

def plato(q, a, tags):
    tile = {"domain": "research_log", "question": q, "answer": str(a)[:1950],
            "tags": tags, "source": AGENT_ROOM, "confidence": 0.95}
    try:
        data = json.dumps(tile).encode()
        req = urllib.request.Request(PLATO, data=data, headers={"Content-Type":"application/json"})
        resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
        return resp.get("status","?")
    except Exception as e:
        return f"err:{e}"

# ── Decomposition Rules ─────────────────────────

# These are the pattern-matching rules that map file types to room types
ROOM_PATTERNS = {
    # Game logic patterns
    r"class.*Board.*": ("game/state", "algorithmic"),
    r"class.*Position.*": ("game/state", "algorithmic"),
    r"class.*GameState.*": ("game/state", "algorithmic"),
    r"class.*Rules.*": ("game/rules", "algorithmic"),
    r"class.*Move.*": ("game/move", "algorithmic"),
    r"gen_moves\b|legal_moves\b|get_moves\b": ("game/movegen", "algorithmic"),
    r"class.*Searcher.*|class.*Engine.*|class.*AI.*": ("game/search", "algorithmic"),
    r"minimax|alpha.beta|transposition_table|negamax|quiescence|iterative_deepening": ("game/search", "algorithmic"),
    r"class.*Renderer.*|class.*Display.*": ("game/render", "algorithmic"),
    r"class.*Player.*|class.*Agent.*|class.*Bot.*": ("game/agent", "agentic"),
    r"class.*Strategy.*|class.*Heuristic.*": ("game/strategy", "algorithmic"),
    r"class.*Tournament.*|class.*Match.*": ("game/tournament", "algorithmic"),
    
    # I/O patterns
    r"def parse\b|def serialize\b|class.*Parser.*": ("io/parser", "algorithmic"),
    r"UCI\b|HTTP\b|class.*Client.*": ("io/bridge", "agentic"),
    
    # Test patterns

    # General patterns (non-game)
    r"class.*Matrix.*|class.*Vector.*|class.*Tensor.*": ("math/linear", "algorithmic"),
    r"class.*Config.*|class.*Settings.*|def load_config": ("system/config", "algorithmic"),
    r"class.*API.*|class.*Route.*|def get|def post|def put": ("api/endpoint", "algorithmic"),
    r"class.*Model.*|class.*Schema.*|class.*Record.*": ("data/model", "algorithmic"),
    r"class.*Store.*|class.*DB.*|class.*Database.*": ("data/store", "algorithmic"),
    r"class.*Logger.*|class.*Log.*|def log|class.*Metrics.*": ("system/logging", "algorithmic"),
    r"class.*Cache.*|class.*LRU.*|class.*Redis.*": ("data/cache", "algorithmic"),
    r"class.*Queue.*|class.*Job.*|class.*Worker.*": ("system/queue", "agentic"),
    r"class.*Plugin.*|class.*Extension.*": ("system/plugin", "agentic"),
    r"class.*Auth.*|class.*Login.*|class.*Session.*": ("auth/provider", "algorithmic"),
    r"class.*Test.*|class.*Benchmark.*|@pytest|@test": ("test/suite", "algorithmic"),
    r"class.*CLI.*|class.*Command.*|argparse": ("cli/interface", "agentic"),

    r"struct.*Router|struct.*Handler|struct.*Server": ("network/router", "algorithmic"),
    r"struct.*Config|struct.*Options|struct.*Settings": ("system/config", "algorithmic"),
    r"struct.*Consensus|struct.*Cycle|struct.*Trust": ("game/state", "algorithmic"),
    r"struct.*Cache|struct.*Store|HashMap|DashMap": ("data/store", "algorithmic"),
    r"fn main|fn run|fn execute": ("cli/interface", "agentic"),
    r"#\[test\]|#\[cfg\(test\)\]": ("test/suite", "algorithmic"),
    # Math & data patterns
    r"class.*Lattice.*|class.*Encoder.*|class.*Analysis": ("math/compute", "algorithmic"),
    r"class.*Metric.*|class.*Health.*|class.*Measure.*": ("math/metrics", "algorithmic"),
    r"spectral_entropy\|spectral_gap\|coupling_entropy\|algebraic_normalized": ("math/spectral", "algorithmic"),
    r"class.*Vector.*|class.*Matrix.*|numpy|np\.\w+\(": ("math/linear", "algorithmic"),
    r"class.*Router.*|class.*Dispatch.*": ("network/router", "algorithmic"),
    r"class.*Supervisor.*|class.*Monitor.*": ("system/supervisor", "agentic"),

        r"class.*Test.*|def test_.*|unittest|pytest": ("test/suite", "algorithmic"),
}

FILE_PATTERNS = {
    r"\.py$": "python",
    r"\.rs$": "rust",
    r"\.go$": "golang",
    r"\.js$|\.ts$": "javascript",
    r"\.c$|\.cpp$|\.h$": "c-family",
    r"\.gleam$": "gleam",
    r"\.lua$": "lua",
}

# ── Analysis Engine ──────────────────────────────

def clone_repo(url, target):
    """Clone a git repo, return True on success."""
    result = subprocess.run(
        ["git", "clone", "--depth", "1", url, target],
        capture_output=True, text=True, timeout=60
    )
    return result.returncode == 0

def analyze_file(filepath):
    """Analyze a file for architectural patterns."""
    content = open(filepath).read()
    lines = content.split('\n')
    loc = len(lines)
    
    # Detect language
    ext = os.path.splitext(filepath)[1]
    lang = "unknown"
    for pattern, detected in FILE_PATTERNS.items():
        if re.search(pattern, filepath):
            lang = detected
            break
    
    # Detect classes
    classes = re.findall(r'^\s*class\s+(\w+)', content, re.MULTILINE)
    
    # Detect functions
    functions = re.findall(r'^\s*def\s+(\w+)|^\s*pub\s+fn\s+(\w+)', content, re.MULTILINE)
    
    # Detect imports/dependencies
    imports = re.findall(r'^import\s+(\S+)|^use\s+(\S+)|^from\s+(\S+)', content, re.MULTILINE)
    
    # Detect room patterns
    rooms = []
    for pattern, (room_type, room_kind) in ROOM_PATTERNS.items():
        if re.search(pattern, content):
            rooms.append({"type": room_type, "kind": room_kind, "pattern": pattern})
    
    return {
        "path": filepath,
        "language": lang,
        "loc": loc,
        "classes": classes,
        "functions": [f[0] or f[1] for f in functions],
        "imports": list(set(i[0] or i[1] or i[2] for i in imports)),
        "detected_rooms": rooms,
    }

def analyze_repo(repo_path):
    """Analyze entire repo structure."""
    results = []
    
    for root, dirs, files in os.walk(repo_path):
        # Skip hidden dirs and common non-source dirs
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', '__pycache__', '.git', 'target')]
        
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                fsize = os.path.getsize(fpath)
            except:
                continue
            if fsize > 100000:  # skip files > 100KB
                continue
            try:
                results.append(analyze_file(fpath))
            except Exception as e:
                results.append({"path": fpath, "error": str(e)})
    
    return results

# ── Room Code Generation ─────────────────────────

def generate_room_code(room_type, room_kind, original_file):
    """Generate PLATO Loop Room code from an analyzed file."""
    
    template = f'''"""PLATO-native {room_type} room — decomposed from {original_file}.
Algorithmic-first, agentic-second. Runs in the Loop Room framework.
"""
import json, os, sys

# PLATO room state
STATE = {{}}
PLATO_URL = "http://localhost:8847"

def plato_write(room, q, a, tags):
    import urllib.request
    tile = {{"domain": room, "question": q, "answer": str(a)[:1950],
            "tags": tags, "source": room, "confidence": 0.95}}
    try:
        data = json.dumps(tile).encode()
        req = urllib.request.Request(f"{{PLATO_URL}}/submit", data=data,
            headers={{"Content-Type": "application/json"}})
        return json.loads(urllib.request.urlopen(req, timeout=5).read())
    except Exception as e:
        return {{"error": str(e)}}

def loop():
    """Main Loop Room loop — observe, think, tool, repeat."""
    while True:
        # observe: read input tile
        # think: process through rules/agent
        # tool: write result tile
        # loop
        pass

if __name__ == "__main__":
    # bootstrap the room
    loop()
'''
    
    return template

# ── Agent Main Logic ─────────────────────────────

def decompose_repo(repo_url):
    """Main pipeline: clone → analyze → generate → publish."""
    repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
    
    plato(f"decomp/start/{repo_name}", f"Starting decomposition of {repo_url}", 
          ["decomp", repo_name, "start"])
    
    # Step 1: Clone
    tmpdir = tempfile.mkdtemp(prefix=f"decomp-{repo_name}-")
    print(f"Cloning {repo_url}...")
    if not clone_repo(repo_url, tmpdir):
        plato(f"decomp/fail/{repo_name}", f"Failed to clone {repo_url}", ["decomp", repo_name, "fail"])
        return {"status": "error", "message": "clone failed"}
    
    print("Analyzing...")
    analysis = analyze_repo(tmpdir)
    
    # Step 2: Generate room mapping
    all_rooms = {}
    for a in analysis:
        for room in a.get("detected_rooms", []):
            rt = room["type"]
            if rt not in all_rooms:
                all_rooms[rt] = {"type": rt, "kind": room["kind"], "source_files": []}
            all_rooms[rt]["source_files"].append(a["path"])
    
    # Step 3: De-duplicate and rank
    room_list = sorted(all_rooms.values(), key=lambda r: len(r["source_files"]), reverse=True)
    
    # Step 4: Generate room code and publish
    for room in room_list[:10]:  # max 10 rooms
        src = room["source_files"][0] if room["source_files"] else "unknown"
        code = generate_room_code(room["type"], room["kind"], src)
        
        plato(f"decomp/{repo_name}/room/{room['type']}",
              json.dumps({"type": room["type"], "kind": room["kind"],
                          "source_files": room["source_files"][:5],
                          "room_code": code[:500]}),
              ["decomp", repo_name, f"room-{room['type']}", room["kind"]])
    
    # Step 5: Write summary
    summary = {
        "repo": repo_url,
        "name": repo_name,
        "files_analyzed": len(analysis),
        "rooms_identified": len(room_list),
        "rooms": [{"type": r["type"], "kind": r["kind"], "source_count": len(r["source_files"])} for r in room_list],
        "languages": list(set(a.get("language", "unknown") for a in analysis if a.get("language"))),
        "total_loc": sum(a.get("loc", 0) for a in analysis),
    }
    
    plato(f"decomp/complete/{repo_name}", json.dumps(summary, indent=2),
          ["decomp", repo_name, "complete"])
    
    # Cleanup
    subprocess.run(["rm", "-rf", tmpdir])
    
    print(f"\nDecomposition complete: {repo_name}")
    print(f"  Files analyzed: {summary['files_analyzed']}")
    print(f"  Rooms identified: {summary['rooms_identified']}")
    print(f"  Languages: {', '.join(summary['languages'])}")
    print(f"  Total LOC: {summary['total_loc']}")
    
    return summary


if __name__ == "__main__":
    # Test: decompose our own plato-ng repo
    print("=== Git-Agent: Decomposing plato-ng ===")
    print()
    result = decompose_repo("https://github.com/SuperInstance/plato-ng.git")
    print()
    print(f"Status: {result.get('status', 'ok')}")
    print("All tiles published to PLATO.")
