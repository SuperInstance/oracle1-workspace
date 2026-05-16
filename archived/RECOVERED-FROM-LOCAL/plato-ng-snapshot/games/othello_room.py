"""Othello/Reversi PLATO Loop Room — 8×8 reversible disc tournament."""
import json, random, urllib.request, time

PLATO = "http://localhost:8847"
ROOM = "game/othello"
TAG_PREFIX = "parralel-2026-05-15"

# ── Constants ──
EMPTY = "."
BLACK = "B"
WHITE = "W"

DIRECTIONS = [(-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1)]


def plato_write(question, answer, tags):
    tile = {"domain": ROOM, "question": question, "answer": answer,
            "tags": tags, "source": "othello-room", "confidence": 0.99}
    try:
        data = json.dumps(tile).encode()
        req = urllib.request.Request(f"{PLATO}/submit", data=data,
            headers={"Content-Type": "application/json"})
        resp = json.loads(urllib.request.urlopen(req, timeout=5).read())
        return resp.get("status", "?")
    except Exception as e:
        return f"err: {e}"


# ══════════════════════════════════════════════════════════════════════
#  Game Logic
# ══════════════════════════════════════════════════════════════════════

def new_board():
    """8×8 with standard Othello opening: B at d4/e5, W at e4/d5."""
    board = [[EMPTY]*8 for _ in range(8)]
    board[3][3] = WHITE; board[3][4] = BLACK
    board[4][3] = BLACK; board[4][4] = WHITE
    return board


def board_copy(board):
    return [row[:] for row in board]


def board_str(board):
    lines = ["  a b c d e f g h"]
    for i, row in enumerate(board):
        lines.append(f"{i+1} {' '.join(row)}")
    return "\n".join(lines)


def opponent(mark):
    return WHITE if mark == BLACK else BLACK


def in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8


def get_flips(board, r, c, mark):
    """Return list of (r,c) positions flipped if mark plays at (r,c)."""
    if not in_bounds(r, c) or board[r][c] != EMPTY:
        return []
    opp = opponent(mark)
    all_flips = []
    for dr, dc in DIRECTIONS:
        flips = []
        nr, nc = r + dr, c + dc
        while in_bounds(nr, nc) and board[nr][nc] == opp:
            flips.append((nr, nc))
            nr += dr; nc += dc
        if in_bounds(nr, nc) and board[nr][nc] == mark and flips:
            all_flips.extend(flips)
    return all_flips


def valid_moves(board, mark):
    """Return list of (r,c) valid moves — must capture ≥1 piece."""
    return [(r, c) for r in range(8) for c in range(8)
            if board[r][c] == EMPTY and get_flips(board, r, c, mark)]


def apply_move(board, r, c, mark):
    """Return new board after mark plays at (r,c)."""
    new_b = board_copy(board)
    for fr, fc in get_flips(board, r, c, mark):
        new_b[fr][fc] = mark
    new_b[r][c] = mark
    return new_b


def count_discs(board, mark):
    return sum(row.count(mark) for row in board)


def count_all_discs(board):
    return count_discs(board, BLACK), count_discs(board, WHITE)


def is_game_over(board):
    return not valid_moves(board, BLACK) and not valid_moves(board, WHITE)


def game_result(board):
    b, w = count_all_discs(board)
    if b > w: return "B"
    if w > b: return "W"
    return "tie"


# ══════════════════════════════════════════════════════════════════════
#  Position-Value Map (corners = invincible, edges = safe, C-squares = poison)
# ══════════════════════════════════════════════════════════════════════

POSITION_SCORES = [
    [ 100,  -15,   8,   5,   5,   8, -15,  100],
    [ -15,  -20,   1,   1,   1,   1, -20,  -15],
    [   8,    1,   3,   3,   3,   3,   1,    8],
    [   5,    1,   3,   3,   3,   3,   1,    5],
    [   5,    1,   3,   3,   3,   3,   1,    5],
    [   8,    1,   3,   3,   3,   3,   1,    8],
    [ -15,  -20,   1,   1,   1,   1, -20,  -15],
    [ 100,  -15,   8,   5,   5,   8, -15,  100],
]


# ══════════════════════════════════════════════════════════════════════
#  AI Strategies
# ══════════════════════════════════════════════════════════════════════

def strategy_positional(board, mark):
    """Position-first: weights corners (100) ≫ edges (8) ≫ center (3-5).
    Heavily penalizes C-squares (-15) and C-adjacent (-20) to avoid gifting corners."""
    moves = valid_moves(board, mark)
    if not moves:
        return None
    opp = opponent(mark)
    best = None
    best_score = -9999
    for r, c in moves:
        new_b = apply_move(board, r, c, mark)
        # Score = positional value of new piece + flipped piece positions
        score = POSITION_SCORES[r][c]
        for fr, fc in get_flips(board, r, c, mark):
            score += POSITION_SCORES[fr][fc] * 0.5  # flipping opponent's stuff is good
        # Bonus: taking a piece from opponent
        score += len(get_flips(board, r, c, mark)) * 0.1
        # Parry: edge stability — prefer moves that secure stable edges
        disc_diff = count_discs(new_b, mark) - count_discs(new_b, opp)
        score += disc_diff * 0.05
        if score > best_score:
            best_score = score
            best = (r, c)
    return best


def strategy_mobility(board, mark):
    """Mobility-first: maximises own valid-move count while minimising opponent's.
    Secondary: flips as many pieces as possible."""
    moves = valid_moves(board, mark)
    if not moves:
        return None
    opp = opponent(mark)
    best = None
    best_score = -9999
    for r, c in moves:
        new_b = apply_move(board, r, c, mark)
        my_moves = len(valid_moves(new_b, mark))
        opp_moves = len(valid_moves(new_b, opp))
        mobility_diff = my_moves - opp_moves
        pieces_flipped = len(get_flips(board, r, c, mark))
        # Mobility weight decays slightly as board fills (endgame: disc count matters)
        total_squares = 4  # 4 already occupied at start
        for row in board:
            total_squares += row.count(EMPTY)
        total_squares = 64 - sum(row.count(EMPTY) for row in board)
        if total_squares < 20:
            # Endgame: shift toward disc count
            disc_diff = count_discs(new_b, mark) - count_discs(new_b, opp)
            score = disc_diff * 10 + mobility_diff * 2 + pieces_flipped
        elif total_squares < 40:
            # Midgame: balance
            score = mobility_diff * 15 + pieces_flipped * 2
        else:
            # Opening: mobility is king
            score = mobility_diff * 20 + pieces_flipped
        if score > best_score:
            best_score = score
            best = (r, c)
    return best


STRATEGIES = {
    "positional": {
        "fn": strategy_positional,
        "desc": "Corner/edge control, positional value heuristic, avoids C-squares",
    },
    "mobility": {
        "fn": strategy_mobility,
        "desc": "Maximises own moves, minimises opponent moves, flipped-piece secondary",
    },
}


# ══════════════════════════════════════════════════════════════════════
#  Game Loop
# ══════════════════════════════════════════════════════════════════════

def play_game(strat_b="positional", strat_w="mobility", game_id=1):
    """Play one game — Black starts, alternate passes allowed."""
    board = new_board()
    moves_log = []
    mark = BLACK
    consecutive_passes = 0

    while not is_game_over(board):
        fn = STRATEGIES[strat_b if mark == BLACK else strat_w]["fn"]
        move = fn(board, mark)

        if move is None:
            consecutive_passes += 1
            moves_log.append({"player": mark, "move": "pass", "board": board_str(board)})
            if consecutive_passes >= 2:
                # Both pass consecutively → game over
                break
            mark = opponent(mark)
            continue

        consecutive_passes = 0
        r, c = move
        flips = get_flips(board, r, c, mark)
        board = apply_move(board, r, c, mark)
        moves_log.append({
            "player": mark,
            "move": f"{chr(c+97)}{r+1}",  # algebraic: a1-h8
            "flips": len(flips),
            "discs_b": count_discs(board, BLACK),
            "discs_w": count_discs(board, WHITE),
        })
        mark = opponent(mark)

    result = game_result(board)
    return {"result": result, "moves": moves_log, "boards": board, "id": game_id}


def run_tournament(strat_b="positional", strat_w="mobility", n_games=100):
    """Run N games Black=first-strat, alternating first-player each game."""
    results = {"B": 0, "W": 0, "tie": 0}
    total_b_discs = 0
    total_w_discs = 0

    for gid in range(1, n_games + 1):
        if gid % 2 == 1:
            sb, sw = strat_b, strat_w
        else:
            sb, sw = strat_w, strat_b

        game = play_game(sb, sw, gid)
        results[game["result"]] += 1

        bd, wd = count_all_discs(game["boards"])
        total_b_discs += bd
        total_w_discs += wd

        # Every game: result tile
        plato_write(
            f"game-{gid}/result",
            json.dumps({
                "game_id": gid,
                "B_strategy": sb,
                "W_strategy": sw,
                "result": game["result"],
                "moves": len(game["moves"]),
                "final_B": bd,
                "final_W": wd,
            }),
            [TAG_PREFIX, "othello-game", f"gid-{gid}", game["result"]],
        )

        # Detail tiles for early games + every 10th
        if gid <= 10 or gid % 10 == 0:
            plato_write(
                f"game-{gid}/moves",
                json.dumps(game["moves"]),
                [TAG_PREFIX, "othello-moves", f"gid-{gid}"],
            )

        if gid % 25 == 0:
            print(f"  Game {gid}/{n_games}: B={results['B']} W={results['W']} tie={results['tie']}  "
                  f"avg discs B={total_b_discs/gid:.1f} W={total_w_discs/gid:.1f}")

    return results, total_b_discs, total_w_discs


# ══════════════════════════════════════════════════════════════════════
#  Post-Tournament Analysis
# ══════════════════════════════════════════════════════════════════════

def agentic_analysis(results, strat_b, strat_w, total_b_discs, total_w_discs, n_games):
    total = sum(results.values())
    analysis = {
        "tournament": f"{strat_b}-vs-{strat_w}",
        TAG_PREFIX: True,
        "total_games": total,
        "B_wins": results["B"],
        "W_wins": results["W"],
        "ties": results["tie"],
        "B_strategy": strat_b,
        "W_strategy": strat_w,
        "avg_B_discs": round(total_b_discs / max(1, n_games), 1),
        "avg_W_discs": round(total_w_discs / max(1, n_games), 1),
        "B_win_pct": round(results["B"] / max(1, total) * 100, 1),
        "W_win_pct": round(results["W"] / max(1, total) * 100, 1),
        "summary": f"{strat_b} (B) won {results['B']}, {strat_w} (W) won {results['W']}, {results['tie']} ties. "
                   f"Avg discs: B={total_b_discs/max(1,n_games):.1f} W={total_w_discs/max(1,n_games):.1f}",
    }
    plato_write(
        f"tournament/{strat_b}-vs-{strat_w}/analysis",
        json.dumps(analysis, indent=2),
        [TAG_PREFIX, "othello-analysis", "tournament", strat_b, strat_w],
    )
    return analysis


# ══════════════════════════════════════════════════════════════════════
#  Main
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("═" * 55)
    print("  Othello/Reversi PLATO Loop Room — 8×8 reversible disc battles")
    print("═" * 55)
    print()

    # Seed room metadata
    plato_write("room/description",
        "Othello/Reversi Loop Room. 8×8 board, reversible disc capture.\n"
        "Strategies: positional (corner/edge value map) vs mobility (move-count differential).\n"
        "Games play algorithmically — no LLM per move.\n"
        f"Tag: {TAG_PREFIX}\n",
        [TAG_PREFIX, "othello-room", "description"])

    plato_write("room/strategies",
        json.dumps({k: {"desc": v["desc"]} for k, v in STRATEGIES.items()}, indent=2),
        [TAG_PREFIX, "othello-room", "strategies"])

    # ── Tournament: Positional vs Mobility (100 games) ──
    print("Tournament: positional (Black, alternating first) vs mobility (White)")
    print(f"  {100} games, alternating first-player each round\n")
    r1, tbd, twd = run_tournament("positional", "mobility", 100)
    a1 = agentic_analysis(r1, "positional", "mobility", tbd, twd, 100)
    print()
    print(f"  Final: positional {r1['B']} — mobility {r1['W']} — ties {r1['tie']}")
    print(f"  Avg discs: positional {tbd/100:.1f} — mobility {twd/100:.1f}")
    print()

    # ── Meta-style tile ──
    style_tile = {
        "room": ROOM,
        TAG_PREFIX: True,
        "tournaments": ["positional-vs-mobility"],
        "positional_win_rate": round(r1["B"] / max(1, sum(r1.values())) * 100, 1),
        "mobility_win_rate": round(r1["W"] / max(1, sum(r1.values())) * 100, 1),
        "observation": (
            "Othello positional edge-control strategy tested against mobility-first "
            "approach over 100 games with alternating first-player."
        ),
    }
    plato_write("room/evolved-style", json.dumps(style_tile),
                [TAG_PREFIX, "othello-room", "evolved-style", "meta-strategy"])

    print("═" * 55)
    print("  Evidence logged to PLATO. Room ready.")
    print("═" * 55)
