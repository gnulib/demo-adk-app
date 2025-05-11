from typing import Optional

from google.adk.agents import BaseAgent # Assuming BaseAgent is here
from backend.utils.config import Config
from backend.simple_agent.agent import root_agent as simple_agent_instance

# Module-level variable to hold the singleton instance of the root agent
_singleton_root_agent: Optional[BaseAgent] = None


def get_root_agent(config: Config) -> BaseAgent:
    """
    Initializes and returns a singleton instance of the root agent.

    The agent is sourced from the backend.simple_agent.agent module.
    The config parameter is accepted for consistency but not directly used
    for initializing this specific pre-configured agent.

    Args:
        config: The application configuration object.

    Returns:
        A singleton instance of the BaseAgent.
    """
    global _singleton_root_agent
    if _singleton_root_agent is None:
        # The root_agent from simple_agent.agent is already an initialized instance.
        # We are ensuring that this provider returns that same instance as a singleton.
        _singleton_root_agent = simple_agent_instance
    return _singleton_root_agent
