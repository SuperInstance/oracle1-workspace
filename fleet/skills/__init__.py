"""
Skills Layer — Behavior and Prompt Templates.
Skills define HOW an agent thinks for a given task.
"""
import json


class Skill:
    """Base class for fleet skills."""
    
    name = "base"
    description = "Base skill"
    
    def __init__(self):
        self.templates = {}
    
    def register(self, key, template):
        """Register a prompt template."""
        self.templates[key] = template
    
    def render(self, key, **kwargs):
        """Render a template with variables."""
        template = self.templates.get(key, "")
        return template.format(**kwargs)
    
    def execute(self, context_manager, model_client, **kwargs):
        """Execute the skill. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement execute()")
    
    def system_prompt(self):
        """Return the skill's system prompt. Override in subclasses."""
        return ""


class SkillRegistry:
    """Registry of available skills."""
    
    def __init__(self):
        self._skills = {}
    
    def register(self, skill):
        """Register a skill."""
        self._skills[skill.name] = skill
    
    def get(self, name):
        """Get a skill by name."""
        return self._skills.get(name)
    
    def list_skills(self):
        """List all registered skills."""
        return {name: skill.description for name, skill in self._skills.items()}
    
    def execute(self, name, context_manager, model_client, **kwargs):
        """Execute a skill by name."""
        skill = self.get(name)
        if not skill:
            raise ValueError(f"Unknown skill: {name}")
        return skill.execute(context_manager, model_client, **kwargs)


# Global registry
registry = SkillRegistry()
