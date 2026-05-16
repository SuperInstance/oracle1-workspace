#!/usr/bin/env python3
"""Shallow coupling daemon v2 — reads eigenvalue tiles from PLATO.

PLATO stores eigenvalue summaries in the fleet-coupling room.
Each agent publishes eigenvalue_top5 + spectral_gap as JSON answers.
This daemon reads those tiles, computes health metrics using the
shallow (never-rounds-down) principle, and reports fleet coupling status.

Usage: python3 shallow_coupling_daemon_v2.py
"""

import numpy as np
import json
import urllib.request
import time
import sys

PLATO_HOST = "localhost:8847"
ROOM = "fleet-coupling"
HEALTH_ROOM = "fleet-health"


def fetch_eigenvalues():
    """Fetch latest eigenvalue tiles from PLATO fleet-coupling room.
    
    PLATO format: each agent posts JSON with fields like:
        eigenvalue_top5: [float, ...]
        spectral_gap: float
        fiedler_value: float
    
    Returns list of (source, eigenvalues_array, spectral_gap) tuples.
    """
    url = f"http://{PLATO_HOST}/room/{ROOM}/history"
    try:
        resp = json.loads(urllib.request.urlopen(url).read())
    except Exception as e:
        print(f"ERROR: Cannot read PLATO at {url}: {e}", file=sys.stderr)
        return []

    tiles = resp.get("tiles", [])
    results = []

    for tile in tiles:
        source = tile.get("source", "unknown")
        answer_raw = tile.get("answer", "{}")

        try:
            answer = json.loads(answer_raw) if isinstance(answer_raw, str) else answer_raw
        except (json.JSONDecodeError, TypeError):
            continue

        # Try multiple eigenvalue field names (actual PLATO data uses eigenvalue_top5)
        eigs = answer.get("eigenvalue_top5",
                answer.get("eigenvalues",
                answer.get("first_eigenvalue", None)))

        spectral_gap = answer.get("spectral_gap", None)

        if eigs is not None:
            arr = np.array(eigs, dtype=float)
            results.append((source, arr, spectral_gap))

    return results


def compute_health(eigenvalues, spectral_gap=None):
    """Compute fleet coupling health from eigenvalues using shallow principle.
    
    Shallow principle: never round down. Guarded gap ceilings upward.
    
    Args:
        eigenvalues: numpy array of eigenvalues
        spectral_gap: optional pre-computed spectral gap
    
    Returns:
        dict of health metrics
    """
    if eigenvalues is None or len(eigenvalues) == 0:
        return {"n_dims": 0, "verdict": "INSUFFICIENT"}

    eigs = np.sort(eigenvalues)  # ascending
    n = len(eigs)

    if n < 2:
        return {"n_dims": n, "verdict": "INSUFFICIENT", "values": eigs.tolist()}

    # Compute raw spectral gap (largest gap between consecutive eigenvalues)
    gaps = np.diff(eigs)
    raw_gap = float(gaps[-1])  # gap between largest and second-largest

    # Use provided spectral_gap if available (it may differ from simple diff)
    if spectral_gap is not None:
        raw_gap = float(spectral_gap)

    # Shallow principle: never round down. Guarded gap = ceil() if >= 0.95
    if raw_gap >= 0.95:
        guarded = float(np.ceil(raw_gap))
    else:
        guarded = raw_gap

    # PC1 ratio: largest eigenvalue / sum
    pc1_ratio = float(eigs[-1] / np.sum(eigs))

    return {
        "n_effective_dims": n,
        "pc1_ratio": round(pc1_ratio, 6),
        "raw_gap": round(raw_gap, 6),
        "guarded_gap": guarded,
        "largest_eig": float(eigs[-1]),
        "second_largest": float(eigs[-2]) if n >= 2 else None,
        "verdict": "STABLE" if guarded >= 1.0 else "DEGRADED",
        "principle": "Shallow: never rounds down"
    }


def format_health_report(results):
    """Format eigenvalue data and health metrics into a readable report."""
    lines = []
    lines.append("=" * 60)
    lines.append("SHALLOW COUPLING DAEMON v2 — Fleet Eigenvalue Report")
    lines.append(f"Timestamp: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    lines.append("=" * 60)

    if not results:
        lines.append("\n⚠️  No eigenvalue tiles found in PLATO fleet-coupling room.")
        lines.append("   Agents must publish eigenvalue_top5 in their coupling tiles.")
        return "\n".join(lines)

    lines.append(f"\n📊 Found {len(results)} eigenvalue tile(s) from {len(set(r[0] for r in results))} agent(s):\n")

    for source, eigs, spectral_gap in results:
        lines.append(f"── Agent: {source} ──")
        lines.append(f"   Dimensions: {len(eigs)}")
        lines.append(f"   Top 5 eigenvalues: {[f'{e:.4f}' for e in sorted(eigs, reverse=True)[:5]]}")

        health = compute_health(eigs, spectral_gap)

        lines.append(f"   PC1 ratio:      {health['pc1_ratio']:.4f}")
        lines.append(f"   Raw gap:        {health['raw_gap']}")
        lines.append(f"   Guarded gap:    {health['guarded_gap']}")
        lines.append(f"   Verdict:        {health['verdict']}")
        lines.append(f"   Principle:      {health['principle']}")
        lines.append("")

    # Fleet summary
    if len(results) > 0:
        verdicts = [compute_health(e, sg)["verdict"] for _, e, sg in results]
        stable = verdicts.count("STABLE")
        degraded = verdicts.count("DEGRADED")
        insufficient = verdicts.count("INSUFFICIENT")
        lines.append(f"── Fleet Summary ──")
        lines.append(f"   Stable:          {stable}")
        lines.append(f"   Degraded:        {degraded}")
        lines.append(f"   Insufficient:    {insufficient}")
        lines.append(f"   Fleet verdict:   {'STABLE' if stable > 0 and degraded == 0 else 'DEGRADED'}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def main():
    print("🔮 Shallow Coupling Daemon v2")
    print(f"   Reading PLATO room: {ROOM} on {PLATO_HOST}\n")

    results = fetch_eigenvalues()
    report = format_health_report(results)
    print(report)

    # Attempt to publish health summary back to PLATO
    if results:
        try:
            answer = json.dumps({
                "daemon": "shallow-coupling-v2",
                "timestamp": time.time(),
                "agents_found": [r[0] for r in results],
                "fleet_verdict": "STABLE" if any(
                    compute_health(e, sg)["verdict"] == "STABLE" for _, e, sg in results
                ) else "DEGRADED"
            })
            publish_url = f"http://{PLATO_HOST}/room/{HEALTH_ROOM}/submit"
            payload = json.dumps({
                "domain": "fleet-health",
                "question": f"shallow-coupling-v2 fleet report — {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
                "answer": answer,
                "tags": ["fleet-health", "coupling", "shallow-daemon"],
                "source": "shallow-coupling-daemon-v2",
                "confidence": 0.9
            }).encode()
            req = urllib.request.Request(publish_url, data=payload,
                headers={"Content-Type": "application/json"})
            resp = urllib.request.urlopen(req)
            print(f"\n✅ Published fleet health to PLATO room: {HEALTH_ROOM}")
        except Exception as e:
            print(f"\n⚠️  Could not publish to PLATO: {e}", file=sys.stderr)

    return report


if __name__ == "__main__":
    report = main()
    # Save to wheel output
    output_path = "/tmp/wheel/turn-53-plumbing-fix.md"
    with open(output_path, "w") as f:
        f.write(report)
        f.write(f"\n\n_Saved: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}_\n")
    print(f"\n💾 Report saved to {output_path}")
