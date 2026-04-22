from typing import Dict, Any, Optional, Callable
from abc import ABC, abstractmethod


class Skill(ABC):
    """Base class for skills with registration and execution capabilities."""

    _registry: Dict[str, "Skill"] = {}

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.metadata: Dict[str, Any] = {}
        self._is_registered = False

    @classmethod
    def register(cls, skill: "Skill") -> bool:
        """Register a skill in the global registry."""
        if skill.name in cls._registry:
            return False
        cls._registry[skill.name] = skill
        skill._is_registered = True
        return True

    @classmethod
    def unregister(cls, name: str) -> bool:
        """Unregister a skill from the global registry."""
        if name in cls._registry:
            cls._registry[name]._is_registered = False
            del cls._registry[name]
            return True
        return False

    @classmethod
    def get(cls, name: str) -> Optional["Skill"]:
        """Get a registered skill by name."""
        return cls._registry.get(name)

    @classmethod
    def list_all(cls) -> Dict[str, "Skill"]:
        """List all registered skills."""
        return cls._registry.copy()

    @classmethod
    def execute(cls, name: str, *args, **kwargs) -> Any:
        """Execute a registered skill by name."""
        skill = cls.get(name)
        if not skill:
            raise ValueError(f"Skill '{name}' not found in registry")
        return skill.execute_impl(*args, **kwargs)

    @abstractmethod
    def execute_impl(self, *args, **kwargs) -> Any:
        """Implementation of the skill execution. Must be overridden by subclasses."""
        pass

    def is_registered(self) -> bool:
        """Check if this skill is registered."""
        return self._is_registered

    def set_metadata(self, key: str, value: Any):
        """Set metadata for this skill."""
        self.metadata[key] = value

    def get_metadata(self, key: str) -> Optional[Any]:
        """Get metadata value for this skill."""
        return self.metadata.get(key)

    def to_dict(self) -> Dict[str, Any]:
        """Convert skill to dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "registered": self._is_registered,
            "metadata": self.metadata,
        }


__all__ = ["Skill"]
