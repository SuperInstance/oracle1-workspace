"""Harness standard for PLATO-NG Loop Rooms.

Every room has exactly four harness components:
  p: system prompt / soul configuration
  G: sub-agents (agentic rooms invoked by the orchestrator)
  K: skills (algorithmic routines, reusable programs)
  M: memory (persistent knowledge store)

The harness is stored as a PLATO tile at rooms/{name}/harness.
The Refiner reads and edits this tile mid-episode.
"""

HARNESS_SCHEMA = {
    "version": "0.1.0",
    "p": {"required": True, "type": "string", "description": "System prompt or soul.md path"},
    "G": {"required": False, "type": "list", "description": "Sub-agent room IDs"},
    "K": {"required": False, "type": "list", "description": "Skill tile IDs"},
    "M": {"required": False, "type": "dict", "description": "Memory configuration"},
}

def new_harness(prompt="", sub_agents=None, skills=None, memory=None):
    return {
        "p": prompt,
        "G": sub_agents or [],
        "K": skills or [],
        "M": memory or {"mode": "tile", "prefix": "memory/"},
    }

def validate(harness):
    """Check harness conforms to schema."""
    errors = []
    SCHEMA_FIELDS = {k: v for k, v in HARNESS_SCHEMA.items() if isinstance(v, dict)}
    for field, spec in SCHEMA_FIELDS.items():
        if spec["required"] and field not in harness:
            errors.append(f"Missing required field: {field}")
        if field in harness and spec["type"] == "list" and not isinstance(harness[field], list):
            errors.append(f"Field {field} should be a list")
    return errors

def patch(harness, edits):
    """CRUD: apply edits to a harness. Returns new harness."""
    result = dict(harness)
    for key, value in edits.items():
        if key in HARNESS_SCHEMA:
            if value is None:
                result.pop(key, None)
            else:
                result[key] = value
    return result
