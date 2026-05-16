"""Shared game room base class. All game rooms inherit from this.
Eliminates ~50 lines of boilerplate per game room.
"""

import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.plato_client import submit, submit_result

class GameRoom:
    """Base class for PLATO Loop Room game rooms."""
    
    def __init__(self, name, strategies=None):
        self.name = name
        self.strategies = strategies or {}
        self.results = {"X": 0, "O": 0, "draw": 0}
    
    def register(self):
        """Register the game room on PLATO."""
        submit("research_log", f"{self.name}/room/description",
               f"{self.name} Loop Room. Strategies: {', '.join(self.strategies.keys())}",
               tags=[self.name, "game-room", "description"])
    
    def run_tournament(self, s1, s2, n=100, tag=None):
        """Run N games between two strategies."""
        self.results = {"X": 0, "O": 0, "draw": 0}
        sw = {"s1": s1, "s2": s2}
        
        for gid in range(1, n + 1):
            a = s1 if gid % 2 == 1 else s2
            b = s2 if gid % 2 == 1 else s1
            game = self.play_game(a, b, gid)
            self.results[game["result"]] += 1
            
            if gid % 25 == 0:
                print(f"  {gid}/{n}: X={self.results['X']} O={self.results['O']} draw={self.results['draw']}")
        
        # Submit results
        key = f"{s1}-vs-{s2}" if tag is None else tag
        submit_result(self.name, {
            "X": self.results["X"], "O": self.results["O"],
            "draw": self.results["draw"], "total": n,
            "strategies": {"X": s1, "O": s2}
        }, f"tournament/{key}/result", tags=[self.name, "tournament", key])
        
        return self.results
    
    def play_game(self, s1, s2, gid):
        """Override in subclass. Returns {'result': 'X'|'O'|'draw', 'moves': [...]}"""
        raise NotImplementedError
