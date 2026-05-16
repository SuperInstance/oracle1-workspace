"""Checkers PLATO Loop Room — full 8x8 checkers with mandatory captures,
kings, two AI strategies, tournament loop, and mid-tournament refinement.

Board representation: 64-char string, row-major (row 0 at index 0).
  uppercase = black pieces (B=man, K=king)
  lowercase = red  pieces (r=man, k=king)
  . = empty square

Starting position (row 0 = red back rank, row 7 = black back rank):
  row 0: . r . r . r . r
  row 1: r . r . r . r .
  row 2: . r . r . r . r
  row 3: . . . . . . . .
  row 4: . . . . . . . .
  row 5: B . B . B . B .
  row 6: . B . B . B . B
  row 7: B . B . B . B .
"""

import json, math, random, urllib.request, time, sys

sys.path.insert(0, '/tmp/plato-ng-repo')

from harness import new_harness, validate, patch
from refiner import refine

PLATO = "http://localhost:8847"
ROOM = "game/checkers"

# ═══════════════════════════════════════════════
# PLATO IO
# ═══════════════════════════════════════════════

def plato_write(question, answer, tags):
    tile = {"domain": ROOM, "question": question, "answer": str(answer)[:1950],
            "tags": tags, "source": "checkers-room", "confidence": 0.99}
    try:
        data = json.dumps(tile).encode()
        req = urllib.request.Request(f"{PLATO}/submit", data=data,
            headers={"Content-Type": "application/json"})
        resp = json.loads(urllib.request.urlopen(req, timeout=5).read())
        return resp.get("status", "?")
    except Exception as e:
        return f"err: {e}"


# ═══════════════════════════════════════════════
# CHECKERS GAME LOGIC
# ═══════════════════════════════════════════════

# ── Board primitives ──

def new_board():
    """Standard 8x8 checkers starting position as 64-char string."""
    board = ['.'] * 64
    for i in range(64):
        r, c = divmod(i, 8)
        if (r + c) % 2 == 1:  # dark square
            if r < 3:
                board[i] = 'r'  # red man
            elif r > 4:
                board[i] = 'B'  # black man
    return ''.join(board)


def board_str(board):
    """Pretty-print the board for human readability."""
    lines = []
    lines.append("  +---+---+---+---+---+---+---+---+")
    for r in range(8):
        row_parts = ["{:2d}".format(r)]
        row = board[r*8:(r+1)*8]
        for c, ch in enumerate(row):
            if (r + c) % 2 == 0:
                row_parts.append(f"[{ch}]")
            else:
                row_parts.append(f" {ch} ")
        lines.append("".join(row_parts))
        lines.append("  +---+---+---+---+---+---+---+---+")
    lines.append("    0   1   2   3   4   5   6   7")
    return "\n".join(lines)


def board_to_pieces_ledger(board):
    """Count pieces remaining. Returns dict."""
    blacks = sum(1 for i in range(64) if board[i] in ('B', 'K'))
    reds = sum(1 for i in range(64) if board[i] in ('r', 'k'))
    b_kings = sum(1 for i in range(64) if board[i] == 'K')
    r_kings = sum(1 for i in range(64) if board[i] == 'k')
    return {"black": blacks, "red": reds,
            "black_kings": b_kings, "red_kings": r_kings}


# ── Piece helpers ──

def color_of(piece):
    if piece in ('B', 'K'): return 'black'
    if piece in ('r', 'k'): return 'red'
    return None

def is_man(piece):
    return piece in ('B', 'r')

def is_king(piece):
    return piece in ('K', 'k')

def opponent(color):
    return 'red' if color == 'black' else 'black'

def forward_dir(color):
    return -1 if color == 'black' else 1  # black moves up (decreasing row)

def can_move_backward(piece):
    return is_king(piece)


# ── Move generation ──

def get_simple_moves(board, pos):
    """Get non-capture moves for piece at pos. Returns list of {'from','to','captures':[]}."""
    piece = board[pos]
    if piece == '.':
        return []
    color = color_of(piece)
    r, c = divmod(pos, 8)
    moves = []

    dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    if not can_move_backward(piece):
        fd = forward_dir(color)
        dirs = [(fd, -1), (fd, 1)]

    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 8 and 0 <= nc < 8:
            npos = nr * 8 + nc
            if board[npos] == '.':
                moves.append({"from": pos, "to": npos, "captures": []})

    return moves


def get_direct_captures(board, pos):
    """Get single-step capture opportunities at pos (no chain expansion)."""
    piece = board[pos]
    if piece == '.':
        return []
    color = color_of(piece)
    opp = opponent(color)
    r, c = divmod(pos, 8)
    captures = []

    dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    if not can_move_backward(piece):
        fd = forward_dir(color)
        dirs = [(fd, -1), (fd, 1)]

    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        jr, jc = r + 2*dr, c + 2*dc
        if not (0 <= nr < 8 and 0 <= nc < 8 and 0 <= jr < 8 and 0 <= jc < 8):
            continue
        npos = nr * 8 + nc
        jpos = jr * 8 + jc
        if color_of(board[npos]) == opp and board[jpos] == '.':
            captures.append({"from": pos, "to": jpos, "captures": [npos]})

    return captures


def apply_move(board, move):
    """Apply a move dict to board. Returns new board string.
    Handles king promotion at move end.
    """
    b = list(board)
    piece = b[move["from"]]
    b[move["to"]] = piece
    b[move["from"]] = '.'
    for cap in move.get("captures", []):
        b[cap] = '.'

    # King promotion: black man reaches row 0, red man reaches row 7
    tr = move["to"] // 8
    if piece == 'B' and tr == 0:
        b[move["to"]] = 'K'
    elif piece == 'r' and tr == 7:
        b[move["to"]] = 'k'

    return ''.join(b)


def generate_all_capture_chains(board, pos, captured=None):
    """Recursively generate all capture chains from pos.
    Returns list of move-sequences (each sequence is a list of move dicts).
    """
    if captured is None:
        captured = []

    piece = board[pos]
    color = color_of(piece)
    opp = opponent(color)
    r, c = divmod(pos, 8)

    dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    if not can_move_backward(piece):
        fd = forward_dir(color)
        dirs = [(fd, -1), (fd, 1)]

    results = []
    had_any = False

    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        jr, jc = r + 2*dr, c + 2*dc
        if not (0 <= nr < 8 and 0 <= nc < 8 and 0 <= jr < 8 and 0 <= jc < 8):
            continue
        npos = nr * 8 + nc
        jpos = jr * 8 + jc

        # Can't re-capture the same piece
        if npos in captured:
            continue

        if color_of(board[npos]) == opp and board[jpos] == '.':
            had_any = True
            # Build the intermediate board after this single capture
            inter_board = list(board)
            inter_board[jpos] = piece
            inter_board[pos] = '.'
            inter_board[npos] = '.'
            inter_str = ''.join(inter_board)

            # Promotion check: if a man reaches the back row mid-chain, turn ends
            # (the move stops at the promotion)
            if piece in ('B', 'r'):
                if (piece == 'B' and jr == 0) or (piece == 'r' and jr == 7):
                    # Promote and stop — chain ends here
                    inter_list = list(inter_str)
                    inter_list[jpos] = 'K' if piece == 'B' else 'k'
                    inter_str = ''.join(inter_list)
                    step = {"from": pos, "to": jpos, "captures": [npos]}
                    results.append([step])
                    continue

            new_captured = captured + [npos]
            sub_chains = generate_all_capture_chains(inter_str, jpos, new_captured)

            step = {"from": pos, "to": jpos, "captures": [npos]}
            if sub_chains:
                for sub in sub_chains:
                    results.append([step] + sub)
            else:
                results.append([step])

    return results


def get_all_legal_moves(board, color):
    """Get all legal moves for a color, enforcing mandatory captures.
    Returns list of move-sequences. Each sequence is a list of move dicts
    (1 step for single moves, N steps for chain captures).
    """
    all_moves = []
    all_chains = []

    for i in range(64):
        if color_of(board[i]) == color:
            # Check for captures first (mandatory)
            chains = generate_all_capture_chains(board, i)
            if chains:
                all_chains.extend(chains)

    # Mandatory captures: if any exist, only capture moves are legal
    if all_chains:
        return all_chains

    # No captures available -> simple moves
    for i in range(64):
        if color_of(board[i]) == color:
            simple = get_simple_moves(board, i)
            for m in simple:
                all_moves.append([m])

    return all_moves


def has_legal_moves(board, color):
    """Check if color has any legal move at all."""
    for i in range(64):
        if color_of(board[i]) == color:
            if generate_all_capture_chains(board, i):
                return True
            if get_simple_moves(board, i):
                return True
    return False


def check_game_over(board, color_to_move):
    """Check if the game is over.
    Returns (is_over: bool, winner: str or None).
    """
    if not has_legal_moves(board, color_to_move):
        return True, opponent(color_to_move)

    has_black = any(board[i] in ('B', 'K') for i in range(64))
    has_red = any(board[i] in ('r', 'k') for i in range(64))

    if not has_black:
        return True, 'red'
    if not has_red:
        return True, 'black'

    return False, None


# ═══════════════════════════════════════════════
# AI STRATEGIES
# ═══════════════════════════════════════════════

def strategy_aggressive(board, color):
    """Aggressive checkers AI.
    - Takes captures when possible (mandatory enforced by caller, but picks best chain)
    - Otherwise advances aggressively toward opponent's side
    - Prefers longer capture chains
    - Prefers central positioning for kings
    """
    moves = get_all_legal_moves(board, color)
    if not moves:
        return None

    # Score each move sequence
    def score_seq(seq):
        s = 0
        for step in seq:
            # Value captures highly
            for cap in step.get("captures", []):
                cap_piece = board[cap]
                if is_king(cap_piece):
                    s += 30  # capturing a king is huge
                else:
                    s += 10  # capturing a man

            # Chain length bonus — more captures better
            s += 15 * len(seq)

            # Advancing toward opponent
            to_r = step["to"] // 8
            if color == 'black':
                s += (7 - to_r) * 2  # prefer lower rows
            else:
                s += to_r * 2  # prefer higher rows

            # Central positions (cols 2-5) are tactically valuable
            to_c = step["to"] % 8
            if 2 <= to_c <= 5:
                s += 1

        return s

    moves.sort(key=score_seq, reverse=True)
    return moves[0]


def strategy_defensive(board, color):
    """Defensive checkers AI.
    - Fulfills mandatory captures, but only the simplest option
    - Prefers king creation (move to back rank)
    - Avoids overextension
    - Blocks opponent advances
    - Keeps pieces clustered for mutual protection
    """
    moves = get_all_legal_moves(board, color)
    if not moves:
        return None

    # Separate captures vs simple moves
    capture_seqs = [m for m in moves if any(s.get("captures") for s in m)]
    simple_seqs = [m for m in moves if not any(s.get("captures") for s in m)]

    # Mandatory: if captures exist, pick the simplest (shortest chain, lowest exposure)
    if capture_seqs:
        def cap_safety(seq):
            # Count total captures
            n_caps = sum(len(s.get("captures", [])) for s in seq)
            # Prefer single capture over multi-jump (overextension risk)
            safety = n_caps * 15  # still incentivized to capture
            # But penalize chains that end in exposed position
            final_to = seq[-1]["to"]
            fr = final_to // 8
            fc = final_to % 8
            if color == 'black' and fr <= 1:
                safety -= 10  # too deep in enemy territory
            elif color == 'red' and fr >= 6:
                safety -= 10
            return safety

        capture_seqs.sort(key=cap_safety, reverse=True)
        return capture_seqs[0]

    # Score simple moves defensively
    def defense_score(seq):
        step = seq[0]
        piece = board[step["from"]]
        to_r = step["to"] // 8
        to_c = step["to"] % 8

        s = 0

        # King creation (high priority)
        if color == 'black' and to_r == 0 and is_man(piece):
            s += 60
        elif color == 'red' and to_r == 7 and is_man(piece):
            s += 60

        # Protect kings — keep them safe
        if is_king(piece):
            s += 25

        # Moderate advancement — push forward but avoid overextension
        if color == 'black':
            if to_r <= 3:
                s += 2  # slight push into opponent territory
            if to_r <= 1:
                s -= 3  # overextended into back rank
        elif color == 'red':
            if to_r >= 4:
                s += 2
            if to_r >= 6:
                s -= 3

        # Block opponent — if we move adjacent to opponent pieces, that's good
        opp = opponent(color)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                tr, tc = to_r + dr, to_c + dc
                if 0 <= tr < 8 and 0 <= tc < 8:
                    tpos = tr * 8 + tc
                    if color_of(board[tpos]) == opp:
                        s += 5  # blocking or threatening

        # Mutual support: count friendly neighbors
        neighbors = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                tr, tc = to_r + dr, to_c + dc
                if 0 <= tr < 8 and 0 <= tc < 8:
                    npos = tr * 8 + tc
                    if color_of(board[npos]) == color:
                        neighbors += 1
        s += neighbors * 3

        return s

    simple_seqs.sort(key=defense_score, reverse=True)
    return simple_seqs[0] if simple_seqs else None


STRATEGIES = {
    "aggressive": {"fn": strategy_aggressive,
                   "desc": "Capture-hungry attacker. Seeks long chains, advances deep, "
                           "values central control and king captures."},
    "defensive": {"fn": strategy_defensive,
                  "desc": "Safety-first defender. Quickly creates kings, avoids overextension, "
                          "blocks opponent advances, prefers clustered formations."},
}


# ═══════════════════════════════════════════════
# GAME ENGINE
# ═══════════════════════════════════════════════

def play_game(strat_black="aggressive", strat_red="defensive", game_id=1):
    """Play one checkers game between two strategies.
    Black moves first (uppercase). Returns game result dict.
    """
    board = new_board()
    move_log = []
    turn = 0
    color_to_move = 'black'

    fn_black = STRATEGIES[strat_black]["fn"]
    fn_red = STRATEGIES[strat_red]["fn"]

    max_turns = 300  # safety limit

    while turn < max_turns:
        fn = fn_black if color_to_move == 'black' else fn_red
        strat_name = strat_black if color_to_move == 'black' else strat_red

        seq = fn(board, color_to_move)
        if seq is None:
            # No moves — current player loses
            winner = opponent(color_to_move)
            return {"result": winner, "reason": "no_moves",
                    "moves": move_log, "id": game_id, "final_board": board,
                    "pieces": board_to_pieces_ledger(board)}

        # Apply each step in the sequence
        for step in seq:
            board = apply_move(board, step)
            turn += 1
            move_log.append({
                "player": color_to_move,
                "from": step["from"],
                "to": step["to"],
                "captures": step.get("captures", []),
                "turn": turn,
                "strategy": strat_name,
            })

        is_over, winner = check_game_over(board, opponent(color_to_move))
        if is_over:
            return {"result": winner, "reason": "game_over",
                    "moves": move_log, "id": game_id, "final_board": board,
                    "pieces": board_to_pieces_ledger(board)}

        color_to_move = opponent(color_to_move)

    # Max turns exceeded — draw by move limit
    return {"result": "draw", "reason": "max_turns",
            "moves": move_log, "id": game_id, "final_board": board,
            "pieces": board_to_pieces_ledger(board)}


# ═══════════════════════════════════════════════
# TOURNAMENT ENGINE
# ═══════════════════════════════════════════════

def run_tournament(strat_black="aggressive", strat_red="defensive",
                   n_games=100, refinement_interval=20):
    """Run N checkers games between two strategies.
    Alternates who plays black (first move advantage).
    Mid-tournament refinement every `refinement_interval` games.

    Returns dict of results.
    """
    results = {"black": 0, "red": 0, "draw": 0}
    tournament_start = time.time()

    # Write initial harness
    harness = new_harness(
        prompt=f"Checkers tournament: {strat_black}(black) vs {strat_red}(red)",
        skills=[f"checkers-strategy-{strat_black}", f"checkers-strategy-{strat_red}"],
        memory={"mode": "tile", "prefix": f"games/{ROOM}/"}
    )
    plato_write("room/harness", json.dumps(harness),
                ["checkers", "harness", "tournament"])

    for gid in range(1, n_games + 1):
        # Alternate who plays black for fairness
        if gid % 2 == 1:
            sb, sr = strat_black, strat_red
            black_name = strat_black
            red_name = strat_red
        else:
            sb, sr = strat_red, strat_black
            black_name = strat_red
            red_name = strat_black

        game = play_game(sb, sr, gid)

        # Map result to standard keys
        if game["result"] == 'black':
            results["black"] += 1
        elif game["result"] == 'red':
            results["red"] += 1
        else:
            results["draw"] += 1

        # Log result to PLATO
        plato_write(
            f"game-{gid}/result",
            json.dumps({
                "game_id": gid,
                "black_strategy": black_name,
                "red_strategy": red_name,
                "result": game["result"],
                "reason": game["reason"],
                "moves": len(game["moves"]),
                "pieces_remaining": game["pieces"],
            }),
            ["checkers-game", f"gid-{gid}", game["result"]]
        )

        # Full move logs for first 10 games + every 20th thereafter
        if gid <= 10 or gid % 20 == 0:
            plato_write(
                f"game-{gid}/moves",
                json.dumps(game["moves"][:50]),
                ["checkers-moves", f"gid-{gid}"]
            )

        # Every 25 games, log summary
        if gid % 25 == 0:
            elapsed = time.time() - tournament_start
            print(f"  Game {gid}/{n_games}: "
                  f"black={results['black']} red={results['red']} "
                  f"draw={results['draw']} ({elapsed:.1f}s)")

        # ── Mid-tournament refinement ──
        if gid > 0 and gid % refinement_interval == 0:
            print(f"\n>>> Refinement cycle at game {gid}/{n_games} <<<")
            ref_result = refine(f"games/{ROOM}", interval=refinement_interval // 2)
            print(f"    Refiner status: {ref_result.get('status', '?')}")
            if ref_result.get('failures'):
                for f in ref_result['failures']:
                    print(f"    - {f['type']}: {f.get('detail', '')}")
            print()

    return results


# ═══════════════════════════════════════════════
# POST-TOURNAMENT ANALYSIS
# ═══════════════════════════════════════════════

def agentic_analysis(results, strat_black, strat_red):
    """Generate post-tournament analysis and write to PLATO."""
    total = sum(results.values()) or 1
    analysis = {
        "tournament_id": f"checkers-{strat_black}-vs-{strat_red}",
        "total_games": sum(results.values()),
        "black_wins": results["black"],
        "red_wins": results["red"],
        "draws": results["draw"],
        "black_strategy": strat_black,
        "red_strategy": strat_red,
        "black_win_rate": round(results["black"] / total * 100, 1),
        "red_win_rate": round(results["red"] / total * 100, 1),
        "draw_rate": round(results["draw"] / total * 100, 1),
        "summary": (f"{strat_black}(black) won {results['black']}, "
                    f"{strat_red}(red) won {results['red']}, "
                    f"{results['draw']} draws over {total} games."),
        "strategy_effectiveness": {
            strat_black: results["black"] / total * 100,
            strat_red: results["red"] / total * 100,
        }
    }

    plato_write(
        f"tournament/{strat_black}-vs-{strat_red}/analysis",
        json.dumps(analysis, indent=2),
        ["checkers-analysis", "tournament", strat_black, strat_red]
    )

    return analysis


def write_evolved_style(analysis, strat_black, strat_red):
    """Write meta-strategy evolution tile based on tournament data."""
    style_tile = {
        "room": f"games/{ROOM}",
        "strategy": "evolved",
        "based_on": "tournament data",
        "strategies_tested": [strat_black, strat_red],
        f"{strat_black}_win_rate": round(analysis["strategy_effectiveness"][strat_black], 1),
        f"{strat_red}_win_rate": round(analysis["strategy_effectiveness"][strat_red], 1),
    }

    bw = analysis["black_wins"]
    rw = analysis["red_wins"]
    if bw > rw:
        style_tile["observation"] = f"{strat_black} as black outperforms {strat_red} as red."
        style_tile["meta_style"] = f"{strat_black}-biased"
    elif rw > bw:
        style_tile["observation"] = f"Playing red (second) is not a disadvantage in this matchup."
        style_tile["meta_style"] = f"positionally-balanced"
    else:
        style_tile["observation"] = f"Balanced matchup between {strat_black} and {strat_red}."
        style_tile["meta_style"] = "balanced"

    plato_write("room/evolved-style", json.dumps(style_tile),
                ["checkers", "evolved-style", "meta-strategy"])


# ═══════════════════════════════════════════════
# TEST SUITE
# ═══════════════════════════════════════════════

def run_short_test(n=10):
    """Run N games and validate correctness. No PLATO writes."""
    print(f"\nRunning {n}-game test...")
    results = {"black": 0, "red": 0, "draw": 0}

    for gid in range(1, n + 1):
        sb = "aggressive" if gid % 2 == 1 else "defensive"
        sr = "defensive" if gid % 2 == 1 else "aggressive"
        game = play_game(sb, sr, gid)

        if game["result"] == 'black':
            results["black"] += 1
        elif game["result"] == 'red':
            results["red"] += 1
        else:
            results["draw"] += 1

        final = game.get("pieces", {})
        print(f"  Game {gid:2d}: {sb:>10}(B) vs {sr:>10}(R) "
              f"→ {game['result']:>6} | "
              f"{game['reason']:>9} | "
              f"{len(game['moves']):3d} moves | "
              f"pieces B:{final.get('black',0)} R:{final.get('red',0)}")

        # Validate final board is consistent
        fb = game["final_board"]
        assert len(fb) == 64, f"Board length mismatch: {len(fb)}"
        assert all(c in '.BrKk' for c in fb), f"Invalid chars in board: {set(fb)}"
        # Check no pieces on light squares
        for i in range(64):
            if fb[i] != '.':
                r, c = divmod(i, 8)
                assert (r + c) % 2 == 1, f"Piece on light square at pos {i} (r={r},c={c})"
        # Verify piece counts match ledger
        ledger_count = sum(1 for i in range(64) if fb[i] != '.')
        ledger_pieces = final.get('black', 0) + final.get('red', 0)
        coords_black = sum(1 for i in range(64) if fb[i] in ('B', 'K'))
        coords_red = sum(1 for i in range(64) if fb[i] in ('r', 'k'))
        assert coords_black == final.get('black', 0), \
            f"Black count mismatch: board={coords_black} ledger={final.get('black')}"
        assert coords_red == final.get('red', 0), \
            f"Red count mismatch: board={coords_red} ledger={final.get('red')}"

    print(f"\n  Result: black={results['black']} red={results['red']} "
          f"draw={results['draw']} ({n} games)")
    print("  ✅ All validations passed")
    return results


# ═══════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "tournament"

    if mode == "test":
        run_short_test(10)

    elif mode == "tournament":
        print("=== Checkers PLATO Loop Room ===")
        print("Seeding room with game definitions...\n")

        # Write room metadata to PLATO
        plato_write("room/description",
            "Checkers Loop Room. Full 8x8 checkers with mandatory captures, "
            "kings, AI strategies, and tournament refinement.\n"
            "Board: 64-char string. uppercase=black, lowercase=red, .=empty.\n"
            "Strategies: aggressive (capture-hungry, deep-pushing) and "
            "defensive (king-creating, block-focused).\n"
            "Games use pure algorithmic play (no LLM per move).\n"
            "Mid-tournament refinement via Refiner Room.\n"
            "Style evolves through tournament iterations.",
            ["checkers-room", "description"])

        plato_write("room/strategies",
            json.dumps({k: {"desc": v["desc"]} for k, v in STRATEGIES.items()}),
            ["checkers-room", "strategies"])

        # ── Tournament: Aggressive vs Defensive (100 games) ──
        print("Tournament: aggressive(black) vs defensive(red) (100 games)")
        r1 = run_tournament("aggressive", "defensive", 100)
        a1 = agentic_analysis(r1, "aggressive", "defensive")
        write_evolved_style(a1, "aggressive", "defensive")
        print(f"\nResult: aggressive={r1['black']} defensive={r1['red']} "
              f"draws={r1['draw']}\n")
        print("Evidence logged to PLATO. Room ready.")

    elif mode == "both":
        print("=== Checkers PLATO Loop Room ===")
        run_short_test(10)
        print("\n--- Running tournament ---")
        plato_write("room/description",
            "Checkers Loop Room. Full 8x8 checkers with mandatory captures.",
            ["checkers-room", "description"])
        plato_write("room/strategies",
            json.dumps({k: {"desc": v["desc"]} for k, v in STRATEGIES.items()}),
            ["checkers-room", "strategies"])
        r1 = run_tournament("aggressive", "defensive", 100)
        a1 = agentic_analysis(r1, "aggressive", "defensive")
        write_evolved_style(a1, "aggressive", "defensive")
        print(f"\nResult: aggressive={r1['black']} defensive={r1['red']} "
              f"draws={r1['draw']}")

    else:
        print(f"Usage: {sys.argv[0]} [test|tournament|both]")
        print("  test       - Run 10-game validation test (no PLATO)")
        print("  tournament - Run 100-game tournament with PLATO logging")
        print("  both       - Test then tournament")
