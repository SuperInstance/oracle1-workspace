"""
Universal Four-Layer Adapter.
Wraps any existing service script to give it fleet library access.
Services can progressively replace inline code with library imports.
"""
import sys
import os
FLEET_LIB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, FLEET_LIB)

# Make fleet modules available to all services
from equipment.plato import PlatoClient
from equipment.models import FleetModelClient
from equipment.mud import MudEngine, Room
from equipment.matrix import MatrixClient
from agent.context import ContextManager
from skills import Skill, SkillRegistry

# Singleton instances for all services
plato = PlatoClient()
models = FleetModelClient()
matrix = MatrixClient(
    token=os.environ.get("MATRIX_TOKEN", ""),
    server_name="147.224.38.131"
)

def inject_into(globals_dict):
    """Inject fleet modules into a service's global namespace."""
    globals_dict.update({
        "plato": plato,
        "models": models,
        "matrix": matrix,
        "MudEngine": MudEngine,
        "Room": Room,
        "ContextManager": ContextManager,
        "SkillRegistry": SkillRegistry,
        "PlatoClient": PlatoClient,
        "FleetModelClient": FleetModelClient,
        "MatrixClient": MatrixClient,
    })

def service_fetch(url, timeout=3):
    """Cross-service HTTP fetch. Returns parsed JSON or None."""
    import urllib.request, json
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "fleet/3.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except:
        return None

print(f"[adapter] Fleet library injected ({len([plato, models, matrix])} singletons)")
