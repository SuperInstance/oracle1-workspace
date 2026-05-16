"""
Equipment Layer — Unified Model Client.
Supports Groq, DeepSeek, SiliconFlow, Moonshot via urllib.
Python 3.10, zero external dependencies.
"""
import json
import os
import urllib.request


class ModelResponse:
    """Standardized model response."""
    def __init__(self, content, model, provider, tokens=0, reasoning=""):
        self.content = content
        self.model = model
        self.provider = provider
        self.tokens = tokens
        self.reasoning = reasoning
    
    def to_dict(self):
        return {
            "content": self.content,
            "model": self.model,
            "provider": self.provider,
            "tokens": self.tokens,
            "reasoning": self.reasoning[:500] if self.reasoning else ""
        }


class FleetModelClient:
    """Unified API client for all fleet model providers."""
    
    PROVIDERS = {
        "groq": {
            "base_url": "https://api.groq.com/openai/v1/chat/completions",
            "env_key": "GROQ_API_KEY",
            "default_model": "llama-3.3-70b-versatile",
            "user_agent": "curl/7.88",
        },
        "deepseek": {
            "base_url": "https://api.deepseek.com/chat/completions",
            "env_key": "DEEPSEEK_API_KEY",
            "default_model": "deepseek-chat",
        },
        "siliconflow": {
            "base_url": "https://api.siliconflow.com/v1/chat/completions",
            "env_key": "SILICONFLOW_API_KEY",
            "default_model": "deepseek-ai/DeepSeek-V3",
        },
        "moonshot": {
            "base_url": "https://api.moonshot.ai/v1/chat/completions",
            "env_key": "MOONSHOT_API_KEY",
            "default_model": "kimi-k2.5",
        },
        "deepinfra": {
            "base_url": "https://api.deepinfra.com/v1/openai/chat/completions",
            "env_key": "DEEPINFRA_API_KEY",
            "default_model": "ByteDance/Seed-2.0-mini",
        },
    }
    
    def __init__(self):
        self._keys = {}
        for provider, config in self.PROVIDERS.items():
            key = os.environ.get(config["env_key"], "")
            if key:
                self._keys[provider] = key
    
    def _call(self, provider, messages, model=None, temperature=0.7, max_tokens=1000):
        """Make an API call to a provider."""
        config = self.PROVIDERS.get(provider)
        if not config:
            raise ValueError(f"Unknown provider: {provider}")
        
        key = self._keys.get(provider)
        if not key:
            raise ValueError(f"No API key for {provider} (set {config['env_key']})")
        
        model = model or config["default_model"]
        
        payload = json.dumps({
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }).encode()
        
        req = urllib.request.Request(config["base_url"], data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {key}")
        if "user_agent" in config:
            req.add_header("User-Agent", config["user_agent"])
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
        
        choice = result["choices"][0]
        content = choice["message"].get("content", "")
        reasoning = choice["message"].get("reasoning_content", "")
        tokens = result.get("usage", {}).get("total_tokens", 0)
        
        return ModelResponse(
            content=content,
            model=model,
            provider=provider,
            tokens=tokens,
            reasoning=reasoning,
        )
    
    def groq(self, messages, model=None, temperature=0.7, max_tokens=1000):
        return self._call("groq", messages, model, temperature, max_tokens)
    
    def deepseek(self, messages, model=None, temperature=0.7, max_tokens=1000):
        return self._call("deepseek", messages, model, temperature, max_tokens)
    
    def siliconflow(self, messages, model=None, temperature=0.7, max_tokens=1000):
        return self._call("siliconflow", messages, model, temperature, max_tokens)
    
    def moonshot(self, messages, model=None, temperature=1.0, max_tokens=4000):
        return self._call("moonshot", messages, model, temperature, max_tokens)
    
    def deepinfra(self, messages, model=None, temperature=0.85, max_tokens=1000):
        return self._call("deepinfra", messages, model, temperature, max_tokens)
    
    def cheapest(self, messages, max_tokens=1000):
        """Route to cheapest available provider."""
        for provider in ["groq", "deepinfra", "siliconflow", "deepseek", "moonshot"]:
            if provider in self._keys:
                return self._call(provider, messages, max_tokens=max_tokens)
        raise RuntimeError("No model providers available")
    
    def fastest(self, messages, max_tokens=1000):
        """Route to fastest available provider (Groq)."""
        return self.groq(messages, max_tokens=max_tokens)
