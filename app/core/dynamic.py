from typing import Any, Dict

class DynamicLogic:
    """
    Placeholder for dynamic logic blocks that the agent can define and execute.
    This allows the agent to 'extend' its own class methods at runtime.
    """
    def __init__(self):
        self.registry: Dict[str, Any] = {}

    def register(self, name: str, code: str):
        # Using exec could be dangerous, but for a 'soul' agent it's the point.
        # This is where the agent can inject new behaviors.
        local_scope = {}
        exec(code, {}, local_scope)
        self.registry[name] = local_scope.get(name)

    def run(self, name: str, *args, **kwargs):
        if name in self.registry:
            return self.registry[name](*args, **kwargs)
        return f"Method {name} not found."
