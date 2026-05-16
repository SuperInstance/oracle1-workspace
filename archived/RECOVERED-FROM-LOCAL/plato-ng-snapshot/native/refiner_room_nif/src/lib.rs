//! Rustler NIF stubs for the Refiner Room.
//!
//! Heavy compute paths — scoring, similarity, and pattern detection —
//! are delegated from Gleam to Rust via these NIFs.
//!
//! Each function is a pure computation with no side effects,
//! making them safe to call concurrently from any number of
//! GenServer message handlers.

use rustler::{Atom, Encoder, Env, NifResult, Term};

// ---------------------------------------------------------------------------
// NIF: score_tile(tile :: String) -> Float
// ---------------------------------------------------------------------------

/// Score a single trajectory tile for interestingness.
///
/// Currently uses a heuristic based on tile length, entropy,
/// and structural complexity. In production this would call
/// a learned scoring model.
#[rustler::nif]
fn score_tile(tile: String) -> f64 {
    let length_factor = (tile.len() as f64).ln_1p() / 20.0;
    let entropy = estimate_entropy(&tile);
    let structural = estimate_structural_complexity(&tile);

    // Composite: length 30%, entropy 40%, structural 30%
    let score = length_factor * 0.3 + entropy * 0.4 + structural * 0.3;

    // Clamp to [0.0, 1.0]
    score.clamp(0.0, 1.0)
}

/// Simple Shannon entropy estimate on the string's byte distribution.
fn estimate_entropy(s: &str) -> f64 {
    if s.is_empty() {
        return 0.0;
    }
    let len = s.len() as f64;
    let mut counts = [0u64; 256];
    for &b in s.as_bytes() {
        counts[b as usize] += 1;
    }
    let entropy: f64 = counts
        .iter()
        .filter(|&&c| c > 0)
        .map(|&c| {
            let p = c as f64 / len;
            -p * p.log2()
        })
        .sum();

    // Normalize to 0.0–1.0 by dividing by log2(256) = 8.0
    entropy / 8.0
}

/// Estimate structural complexity from JSON/structural elements.
fn estimate_structural_complexity(s: &str) -> f64 {
    let mut score = 0.0;

    // Count structural tokens
    let depth = s.matches('{').count().max(s.matches('[').count());
    score += (depth as f64).ln_1p() / 10.0;

    // Count key-value pairs (JSON field markers)
    let pairs = s.matches(':').count();
    score += (pairs as f64).ln_1p() / 20.0;

    // Deduplication ratio: unique chars / total chars
    let total = s.len();
    if total > 0 {
        let mut seen = std::collections::HashSet::new();
        for &b in s.as_bytes() {
            seen.insert(b);
        }
        let unique_ratio = seen.len() as f64 / total as f64;
        score += unique_ratio * 0.2;
    }

    score.clamp(0.0, 1.0)
}

// ---------------------------------------------------------------------------
// NIF: tile_similarity(a :: String, b :: String) -> Float
// ---------------------------------------------------------------------------

/// Compare two tile strings and return a similarity score 0.0–1.0.
///
/// Implements a fast Jaccard similarity over character trigrams.
#[rustler::nif]
fn tile_similarity(a: String, b: String) -> f64 {
    const N: usize = 3; // trigrams

    fn ngram_set(s: &str, n: usize) -> std::collections::HashSet<String> {
        let chars: Vec<char> = s.chars().collect();
        if chars.len() < n {
            return std::collections::HashSet::new();
        }
        chars
            .windows(n)
            .map(|w| w.iter().collect::<String>())
            .collect()
    }

    let set_a = ngram_set(&a, N);
    let set_b = ngram_set(&b, N);

    if set_a.is_empty() && set_b.is_empty() {
        return 1.0; // both empty = identical
    }
    if set_a.is_empty() || set_b.is_empty() {
        return 0.0;
    }

    let intersection = set_a.intersection(&set_b).count() as f64;
    let union = set_a.union(&set_b).count() as f64;

    intersection / union // Jaccard similarity
}

// ---------------------------------------------------------------------------
// NIF: detect_patterns(scored_tiles :: List(Float)) ->
//      List({atom(), Float})
// ---------------------------------------------------------------------------

/// Detect failure patterns across a window of scored tiles.
///
/// Returns a list of `{:failure_type, severity}` tuples.
/// Pattern list is empty when no failures are detected.
#[rustler::nif]
fn detect_patterns(env: Env, tiles: Vec<f64>) -> NifResult<Term> {
    let mut patterns: Vec<(Atom, f64)> = Vec::new();

    if tiles.len() < 3 {
        return Ok(patterns.encode(env));
    }

    let window = tiles.len();

    // ── 1. Stuck detection ──
    // If the last 3+ scores are within 0.01 of each other
    if window >= 3 {
        let last_three = &tiles[tiles.len().saturating_sub(3)..];
        let all_same = last_three
            .windows(2)
            .all(|w| (w[0] - w[1]).abs() < 0.01);
        if all_same && last_three[0] < 0.95 {
            let severity = (1.0 - last_three[0]) * 0.7 + 0.3;
            patterns.push((atom_stuck(env), severity.clamp(0.0, 1.0)));
        }
    }

    // ── 2. Plateau detection ──
    // No net improvement over the full window (±1% tolerance)
    if window >= 5 {
        let first_third = &tiles[..window / 3];
        let last_third = &tiles[window - window / 3..];
        let early_avg: f64 = first_third.iter().sum::<f64>() / first_third.len() as f64;
        let late_avg: f64 = last_third.iter().sum::<f64>() / last_third.len() as f64;
        let improvement = late_avg - early_avg;

        if improvement.abs() < 0.02 && late_avg < 0.9 {
            let severity = (0.5 - improvement.abs()).clamp(0.3, 0.9);
            patterns.push((atom_plateau(env), severity));
        }
    }

    // ── 3. Degrading detection ──
    // Monotonically decreasing trend over the window
    if window >= 4 {
        let mut decreasing_count = 0;
        for w in tiles.windows(2) {
            if w[1] < w[0] {
                decreasing_count += 1;
            }
        }
        let decreasing_ratio = decreasing_count as f64 / (window - 1) as f64;
        if decreasing_ratio > 0.6 {
            let severity = decreasing_ratio * 0.8 + 0.2;
            patterns.push((atom_degrading(env), severity.clamp(0.0, 1.0)));
        }
    }

    // ── 4. Novel detection ──
    // If the last score is significantly higher than the running average
    // AND high absolute value (>0.7), it suggests a novel state
    if window >= 3 {
        let last = tiles[tiles.len() - 1];
        let prev_avg: f64 = tiles[..tiles.len() - 1]
            .iter()
            .sum::<f64>()
            / (tiles.len() - 1) as f64;
        let delta = last - prev_avg;

        if delta > 0.15 && last > 0.7 {
            let severity = (delta * 2.0).clamp(0.3, 1.0);
            patterns.push((atom_novel(env), severity));
        }
    }

    Ok(patterns.encode(env))
}

// ---------------------------------------------------------------------------
// Atom helpers
// ---------------------------------------------------------------------------

fn atom_stuck(env: Env) -> Atom {
    Atom::from_str(env, "Stuck").unwrap()
}
fn atom_plateau(env: Env) -> Atom {
    Atom::from_str(env, "Plateau").unwrap()
}
fn atom_degrading(env: Env) -> Atom {
    Atom::from_str(env, "Degrading").unwrap()
}
fn atom_novel(env: Env) -> Atom {
    Atom::from_str(env, "Novel").unwrap()
}

// ---------------------------------------------------------------------------
// Rustler initialization
// ---------------------------------------------------------------------------

rustler::init!("refiner_room_nif");
