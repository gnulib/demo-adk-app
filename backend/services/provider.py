from typing import Optional

from google.adk.agents import BaseAgent
from google.adk.sessions import (
    BaseSessionService,
    InMemorySessionService,
    DatabaseSessionService,
    VertexAiSessionService,
)
from utils.config import Config
from simple_agent.agent import root_agent as simple_agent_instance

# Module-level variable to hold the singleton instance of the root agent
_singleton_root_agent: Optional[BaseAgent] = None
# Module-level variable to hold the singleton instance of the session service
_singleton_session_service: Optional[BaseSessionService] = None


def get_root_agent(config: Config) -> BaseAgent:
    """
    Initializes and returns a singleton instance of the root agent.

    The agent is sourced from the simple_agent.agent module.
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


def get_session_service(config: Config) -> BaseSessionService:
    """
    Initializes and returns a singleton instance of a session service.

    The type of session service is determined based on the application
    configuration:
    1. If IS_TESTING is true, InMemorySessionService is used.
    2. If DB_URL is set, DatabaseSessionService is attempted.
    3. If DB_URL is not set (or DatabaseSessionService failed),
       VertexAiSessionService is attempted using PROJECT_ID and LOCATION.
    4. As a fallback, InMemorySessionService is used.

    Args:
        config: The application configuration object.

    Returns:
        A singleton instance of a BaseSessionService.
    """
    global _singleton_session_service
    if _singleton_session_service is not None:
        return _singleton_session_service

    # 1. Check for IS_TESTING
    if config.IS_TESTING:
        print("Using InMemorySessionService (IS_TESTING is true).")
        _singleton_session_service = InMemorySessionService()
        return _singleton_session_service

    # 2. Check for DB_URL
    if config.DB_URL:
        try:
            print(f"Attempting to use DatabaseSessionService with DB_URL: {config.DB_URL}")
            # Note: Using DatabaseSessionService might require 'sqlalchemy' and a DB driver.
            # Consider adding 'google-adk[database]' or 'sqlalchemy' to requirements.txt.
            _singleton_session_service = DatabaseSessionService(db_url=config.DB_URL)
            print("Successfully initialized DatabaseSessionService.")
            return _singleton_session_service
        except Exception as e:
            print(f"Failed to initialize DatabaseSessionService: {e}. Trying next option.")
            # Fall through if DatabaseSessionService initialization fails

    # 3. Try VertexAiSessionService if DB_URL is not set or DatabaseSessionService failed
    # This assumes that if DB_URL was set but failed, we still try VertexAI as a cloud-native option.
    try:
        print(f"Attempting to use VertexAiSessionService with Project: {config.PROJECT_ID}, Location: {config.LOCATION}.")
        _singleton_session_service = VertexAiSessionService(
            project_id=config.PROJECT_ID, location=config.LOCATION
        )
        print("Successfully initialized VertexAiSessionService.")
        return _singleton_session_service
    except Exception as e:
        print(f"Failed to initialize VertexAiSessionService: {e}. Falling back to InMemorySessionService.")
        # Fall through if VertexAiSessionService initialization fails

    # 4. Fallback to InMemorySessionService
    print("Falling back to InMemorySessionService.")
    _singleton_session_service = InMemorySessionService()
    return _singleton_session_service
