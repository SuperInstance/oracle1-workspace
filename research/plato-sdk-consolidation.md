# PLATO SDK Consolidation Recommendation

## Status: Two SDKs, One Has Real Code

### Current State

**plato-sdk** (canonical):
- Real implementation, 9 Python source files
- Agent, Armor, Client, Equipment, Session, Skills, CLI
- Used by domain agents (activelog, deckboss, etc.)
- Published to PyPI (@superinstance/plato-sdk)

**plato-sdk-unified** (meta-package):
- No real implementation, only __init__.py
- Meta-package that bundles 8 consciousness packages
- NOT used by any domain agent
- Never published to PyPI

### Recommendation

**Keep plato-sdk as the canonical SDK.**
Deprecate plato-sdk-unified or convert it to a thin meta-package that wraps plato-sdk + other packages.

### Action Items

1. Update domain agents to explicitly depend on `plato-sdk` (not unified)
2. Update PLATO documentation to reference `plato-sdk` as the canonical SDK
3. Mark `plato-sdk-unified` as deprecated or convert to thin wrapper
4. Consider publishing `plato-sdk` to PyPI (@superinstance scope)
