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
    VertexAiMemoryBankService,
)
from google.adk.artifacts import (
    BaseArtifactService,
    InMemoryArtifactService,
    GcsArtifactService,
)
import vertexai # For Vertex AI specific initializations
# Assuming agent_engines is available under vertexai.preview. This might vary based on SDK version.
# If this import fails, you may need to find the correct path for 'agent_engines'
# e.g., from google.cloud import aiplatform_v1beta1 as aiplatform (and use its client)
# or from vertexai.preview.language_models import Agent (if it's that kind of agent)
# For this change, proceeding with the user's implied 'from vertexai import agent_engines' style.
from vertexai import agent_engines, rag

from demo_adk_app.utils.config import Config
from demo_adk_app.simple_agent.agent import root_agent as simple_agent_instance
from demo_adk_app.agents.game_master_agent.agent import root_agent as game_master_agent

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
        _singleton_root_agent = game_master_agent
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

    # Initialize Vertex AI and determine AGENT_ID if not in testing mode
    # This logic is placed here to ensure AGENT_ID is set on the config object
    # before other session services might be initialized or used with it.
    if not config.IS_TESTING and not config.AGENT_ID: # Only run if not testing and AGENT_ID not already set
        try:
            print(f"Initializing Vertex AI for project: {config.GOOGLE_CLOUD_PROJECT}, location: {config.GOOGLE_CLOUD_LOCATION}")
            vertexai.init(
                project=config.GOOGLE_CLOUD_PROJECT,
                location=config.GOOGLE_CLOUD_LOCATION,
                staging_bucket=f"gs://{config.APP_NAME}-{config.GOOGLE_CLOUD_PROJECT}" # Corrected f-string
            )
            print("Vertex AI initialized.")

            print("Checking for existing Vertex AI agent engines...")
            resource_id: str | None = None
            # The following list() and create() calls are based on the user's example.
            # Actual SDK usage for listing/creating specific types of Vertex AI "agents" or "engines"
            # (e.g., RAG engines, Dialogflow CX agents) might differ.
            for item in agent_engines.list(): # This call might need specific parameters or client setup
                resource_id = item.name
                print(f"Found existing agent engine: {resource_id}")
                break
            
            if not resource_id:
                print("No existing agent engine found. Creating a new one...")
                # The create() method might require parameters like display_name.
                # Using parameter-less create() as per user's example.
                agent = agent_engines.create() 
                resource_id = agent.name
                print(f"Created new agent engine: {resource_id}")
            
            config.AGENT_ID = resource_id # Store the found/created ID in the config
            print(f"AGENT_ID set in config: {config.AGENT_ID}")

        except Exception as e:
            print(f"Error during Vertex AI agent engine setup: {e}. AGENT_ID will not be set by this process.")
            # Depending on requirements, might want to re-raise or handle differently.
            # Fallback to InMemorySessionService
            print("Falling back to InMemorySessionService.")
            _singleton_session_service = InMemorySessionService()
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
        print(f"Attempting to use VertexAiSessionService with default project and location.")
        _singleton_session_service = VertexAiSessionService(
            project=None, location=None
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
    2. Otherwise, VertexAiMemoryBankService is attempted with default parameters.
    3. As a fallback (if VertexAiMemoryBankService fails), InMemoryMemoryService is used.

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

    # 2. Try VertexAiMemoryBankService
    try:
        print("Attempting to use VertexAiMemoryBankService.")
        # VertexAiMemoryBankService might require GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION
        # to be set in the environment, or other specific credentials/setup.
        if not config.AGENT_ID:
            # initialize session service to set AGENT_ID if not already set
            get_session_service(config)

        _singleton_memory_service = VertexAiMemoryBankService(
            project=config.GOOGLE_CLOUD_PROJECT,
            location=config.GOOGLE_CLOUD_LOCATION,
            agent_engine_id=config.AGENT_ID
        )
        print("Successfully initialized VertexAiMemoryBankService.")
        return _singleton_memory_service
    except Exception as e:
        print(f"Failed to initialize VertexAiMemoryBankService: {e}. Falling back to InMemoryMemoryService.")
        # Fall through if VertexAiMemoryBankService initialization fails

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
