from typing import Optional

from google.adk.agents import BaseAgent
from google.adk.sessions import (
    BaseSessionService,
    InMemorySessionService,
    DatabaseSessionService,
    VertexAiSessionService,
)
from google.adk.memory import (
    BaseMemoryService,
    InMemoryMemoryService,
    VertexAiRagMemoryService,
)
from google.adk.artifacts import (
    BaseArtifactService,
    InMemoryArtifactService,
    GcsArtifactService,
)
from utils.config import Config
from simple_agent.agent import root_agent as simple_agent_instance

# Module-level variable to hold the singleton instance of the root agent
_singleton_root_agent: Optional[BaseAgent] = None
# Module-level variable to hold the singleton instance of the session service
_singleton_session_service: Optional[BaseSessionService] = None
# Module-level variable to hold the singleton instance of the memory service
_singleton_memory_service: Optional[BaseMemoryService] = None
# Module-level variable to hold the singleton instance of the artifact service
_singleton_artifact_service: Optional[BaseArtifactService] = None


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
        print(f"Attempting to use VertexAiSessionService with Project: {config.GOOGLE_CLOUD_PROJECT}, Location: {config.GOOGLE_CLOUD_LOCATION}.")
        _singleton_session_service = VertexAiSessionService(
            project_id=config.GOOGLE_CLOUD_PROJECT, location=config.GOOGLE_CLOUD_LOCATION
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


def get_memory_service(config: Config) -> BaseMemoryService:
    """
    Initializes and returns a singleton instance of a memory service.

    The type of memory service is determined based on the application
    configuration:
    1. If IS_TESTING is true, InMemoryMemoryService is used.
    2. Otherwise, VertexAiRagMemoryService is attempted with default parameters.
    3. As a fallback (if VertexAiRagMemoryService fails), InMemoryMemoryService is used.

    Args:
        config: The application configuration object.

    Returns:
        A singleton instance of a BaseMemoryService.
    """
    global _singleton_memory_service
    if _singleton_memory_service is not None:
        return _singleton_memory_service

    # 1. Check for IS_TESTING
    if config.IS_TESTING:
        print("Using InMemoryMemoryService (IS_TESTING is true).")
        _singleton_memory_service = InMemoryMemoryService()
        return _singleton_memory_service

    # 2. Try VertexAiRagMemoryService
    try:
        print("Attempting to use VertexAiRagMemoryService with default parameters.")
        # VertexAiRagMemoryService might require GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION
        # to be set in the environment, or other specific credentials/setup.
        # It will use default values for its parameters if not specified.
        _singleton_memory_service = VertexAiRagMemoryService()
        print("Successfully initialized VertexAiRagMemoryService.")
        return _singleton_memory_service
    except Exception as e:
        print(f"Failed to initialize VertexAiRagMemoryService: {e}. Falling back to InMemoryMemoryService.")
        # Fall through if VertexAiRagMemoryService initialization fails

    # 3. Fallback to InMemoryMemoryService
    print("Falling back to InMemoryMemoryService.")
    _singleton_memory_service = InMemoryMemoryService()
    return _singleton_memory_service


def get_artifact_service(config: Config) -> BaseArtifactService:
    """
    Initializes and returns a singleton instance of an artifact service.

    The type of artifact service is determined based on the application
    configuration:
    1. If IS_TESTING is true, InMemoryArtifactService is used.
    2. If GCS_BUCKET is set, GcsArtifactService is attempted.
    3. As a fallback, InMemoryArtifactService is used.

    Args:
        config: The application configuration object.

    Returns:
        A singleton instance of a BaseArtifactService.
    """
    global _singleton_artifact_service
    if _singleton_artifact_service is not None:
        return _singleton_artifact_service

    # 1. Check for IS_TESTING
    if config.IS_TESTING:
        print("Using InMemoryArtifactService (IS_TESTING is true).")
        _singleton_artifact_service = InMemoryArtifactService()
        return _singleton_artifact_service

    # 2. Check for GCS_BUCKET
    if config.GCS_BUCKET:
        try:
            print(f"Attempting to use GcsArtifactService with GCS_BUCKET: {config.GCS_BUCKET}")
            # GcsArtifactService might require Google Cloud credentials to be configured.
            # Consider adding 'google-cloud-storage' to requirements.txt if not already included by google-adk.
            _singleton_artifact_service = GcsArtifactService(bucket_name=config.GCS_BUCKET)
            print("Successfully initialized GcsArtifactService.")
            return _singleton_artifact_service
        except Exception as e:
            print(f"Failed to initialize GcsArtifactService: {e}. Falling back to InMemoryArtifactService.")
            # Fall through if GcsArtifactService initialization fails

    # 3. Fallback to InMemoryArtifactService
    print("Falling back to InMemoryArtifactService.")
    _singleton_artifact_service = InMemoryArtifactService()
    return _singleton_artifact_service
