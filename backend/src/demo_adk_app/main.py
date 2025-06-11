import uvicorn
import logging

from demo_adk_app.api.app import get_fast_api_app
from demo_adk_app.utils.config import get_config
from demo_adk_app.services.provider import (
    get_root_agent,
    get_session_service,
    get_memory_service,
    get_artifact_service,
)
from demo_adk_app.services.runner import Runner
from demo_adk_app.api.auth import init_auth_module # Import the init function

# Configure basic logging to console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Get a logger instance for this module
logger = logging.getLogger(__name__)

# Get the logger for the specific module you want to silence
adk_llm_loggers = [#logging.getLogger('google_adk.google.adk.models.google_llm'),
                   logging.getLogger('google_genai._api_client'),
                   logging.getLogger('google_genai.models'),
                   logging.getLogger('google_genai.types'),
                   logging.getLogger('httpx'),]
for adk_llm_logger in adk_llm_loggers:
    # Set its level to CRITICAL to effectively disable all but the most severe messages
    adk_llm_logger.setLevel(logging.CRITICAL)
    # Prevent it from passing messages up to parent loggers (like the root logger)
    # adk_llm_logger.propagate = False

# Load application configuration at the module level
app_config = get_config()

# Initialize services and agent
root_agent = get_root_agent(config=app_config)
session_service = get_session_service(config=app_config)
memory_service = get_memory_service(config=app_config)
artifact_service = get_artifact_service(config=app_config)

# Initialize the Runner
app_runner = Runner(
    root_agent=root_agent,
    session_service=session_service,
    memory_service=memory_service,
    artifact_service=artifact_service,
    config=app_config,
)

# Initialize the auth module with config and session_service
init_auth_module(config=app_config, session_service=session_service)

# Create FastAPI application instance at the module level
# This allows Uvicorn to import 'app' directly: uvicorn backend.main:app
app = get_fast_api_app(
    runner=app_runner,
    session_service=session_service,
    memory_service=memory_service,
    artifact_service=artifact_service,
    config=app_config,
)

if __name__ == "__main__":
    # Determine host and port for Uvicorn when running script directly
    # HOST will default to "0.0.0.0" if not set in environment by Pydantic,
    # but it's better to define it in Config if it's always needed.
    # For now, assuming HOST might not always be in config, but PORT is.
    host = getattr(app_config, 'HOST', "0.0.0.0") # Or add HOST to Config model
    port = app_config.PORT

    # Run the application using Uvicorn
    print(f"Starting server on {host}:{port} (when run as script)")
    uvicorn.run(app, host=host, port=port)
