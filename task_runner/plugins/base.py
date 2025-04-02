from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class PluginConfig(BaseModel):
    """Base configuration for all plugins"""
    name: str
    enabled: bool = True
    config: Dict[str, Any] = {}

class BasePlugin(ABC):
    """Base class for all plugins"""

    def __init__(self, config: PluginConfig):
        self.config = config
        self._initialized = False

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the plugin"""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup plugin resources"""
        pass

    @property
    def is_initialized(self) -> bool:
        """Check if plugin is initialized"""
        return self._initialized

    def __enter__(self):
        """Context manager entry"""
        if not self._initialized:
            self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()

class PluginManager:
    """Manages plugin loading and lifecycle"""

    def __init__(self):
        self._plugins: Dict[str, BasePlugin] = {}
        self._configs: Dict[str, PluginConfig] = {}

    def register_plugin(self, name: str, plugin_class: type[BasePlugin], config: PluginConfig) -> None:
        """Register a new plugin"""
        if name in self._plugins:
            raise ValueError(f"Plugin {name} is already registered")

        self._configs[name] = config
        self._plugins[name] = plugin_class(config)

    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """Get a plugin by name"""
        return self._plugins.get(name)

    def initialize_plugin(self, name: str) -> None:
        """Initialize a specific plugin"""
        if plugin := self._plugins.get(name):
            plugin.initialize()

    def cleanup_plugin(self, name: str) -> None:
        """Cleanup a specific plugin"""
        if plugin := self._plugins.get(name):
            plugin.cleanup()

    def initialize_all(self) -> None:
        """Initialize all plugins"""
        for plugin in self._plugins.values():
            plugin.initialize()

    def cleanup_all(self) -> None:
        """Cleanup all plugins"""
        for plugin in self._plugins.values():
            plugin.cleanup()
