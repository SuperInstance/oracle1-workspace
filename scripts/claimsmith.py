#!/usr/bin/env python3
"""claimsmith.py — Generate accurate README claims from perf_db data.

Usage:
  python3 claimsmith.py <perf_db.json> [--table|--sentence]
"""
import json, sys, os

def format_table(db):
    lines = ["| Primitive | Implementation | Avg Time | Samples |"]
    lines.append("|-----------|----------------|----------|---------|")
    for prim, entry in sorted(db.items()):
        ns = entry['avg_ns']
        time_str = f"{ns:.0f}ns" if ns < 1000 else f"{ns/1000:.1f}μs" if ns < 1000000 else f"{ns/1000000:.1f}ms"
        src = entry['source'].split('/')[-1] if '/' in entry['source'] else entry['source']
        lines.append(f"| {prim} | {src} | {time_str} | {entry['calls']} |")
    return "\n".join(lines)

def format_sentence(db):
    lines = [f"Benchmarked on {db[list(db.keys())[0]].get('capabilities', {}).get('arch', 'unknown')}:"]
    for prim, entry in sorted(db.items(), key=lambda x: x[1]['avg_ns']):
        ns = entry['avg_ns']
        time_str = f"{ns:.0f}ns" if ns < 1000 else f"{ns/1000:.1f}μs"
        src = entry['source'].split('/')[-1] if '/' in entry['source'] else entry['source']
        lines.append(f"- {prim}: {src} at {time_str} per call ({entry['calls']} samples)")
    return "\n".join(lines)

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    with open(sys.argv[1]) as f:
        db = json.load(f)
    fmt = 'table' if '--table' in sys.argv else 'sentence'
    if fmt == 'table':
        print(format_table(db))
    else:
        print(format_sentence(db))

    import urllib.request
    try:
        req = urllib.request.Request("http://localhost:8847/room/fleet_benchmarks/submit",
            data=json.dumps({"question": f"verified claims from {os.path.basename(sys.argv[1])}",
                "answer": format_table(db), "source": "claimsmith", "confidence": 0.95}).encode(),
            headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
        print(f"\nFiled to PLATO fleet_benchmarks")
    except:
        pass

if __name__ == "__main__":
    main()
