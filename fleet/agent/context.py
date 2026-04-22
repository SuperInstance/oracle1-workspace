"""
Agent Layer — Context Manager.
Manages context window, injects PLATO tiles, tracks token usage.
Python 3.10, zero external dependencies.
"""
import json
import urllib.request


class ContextManager:
    """Manages context window with tile injection and token tracking."""
    
    def __init__(self, max_tokens=4000, plato_url="http://127.0.0.1:8847"):
        self.max_tokens = max_tokens
        self.plato_url = plato_url
        self.messages = []
        self.token_count = 0
    
    def system(self, content):
        """Add system message."""
        self.messages.append({"role": "system", "content": content})
        self.token_count += len(content) // 4  # rough estimate
    
    def user(self, content):
        """Add user message."""
        self.messages.append({"role": "user", "content": content})
        self.token_count += len(content) // 4
    
    def assistant(self, content):
        """Add assistant message."""
        self.messages.append({"role": "assistant", "content": content})
        self.token_count += len(content) // 4
    
    def inject_tiles(self, domain, max_tiles=5):
        """Inject relevant PLATO tiles into context."""
        try:
            url = f"{self.plato_url}/rooms/{domain}"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as resp:
                room = json.loads(resp.read())
            
            tiles = room.get("tiles", [])[:max_tiles]
            if tiles:
                tile_text = "\n".join(
                    f"Q: {t.get('question','')} A: {t.get('answer','')}"
                    for t in tiles
                )
                context_msg = f"[Fleet Knowledge — {domain}]\n{tile_text}"
                self.system(context_msg)
        except Exception:
            pass  # Graceful degradation if PLATO unavailable
    
    def inject_history(self, history, max_rounds=5):
        """Inject conversation history for continuity."""
        for h in history[-(max_rounds * 2):]:
            role = h.get("role", "user")
            content = h.get("content", "")
            if role in ("user", "assistant"):
                self.messages.append({"role": role, "content": content})
                self.token_count += len(content) // 4
    
    def get_messages(self):
        """Get all messages, trimmed to fit context window."""
        # Trim from front if over limit
        while self.token_count > self.max_tokens and len(self.messages) > 1:
            removed = self.messages.pop(0)
            self.token_count -= len(removed.get("content", "")) // 4
        return self.messages
    
    def reset(self):
        """Clear context."""
        self.messages = []
        self.token_count = 0
    
    def summary(self):
        """Get context stats."""
        return {
            "messages": len(self.messages),
            "estimated_tokens": self.token_count,
            "max_tokens": self.max_tokens,
            "utilization": round(self.token_count / self.max_tokens, 2) if self.max_tokens else 0,
        }
