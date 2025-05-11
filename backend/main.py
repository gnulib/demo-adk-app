import uvicorn

from api.app import get_fast_api_app
from utils.config import get_config
from services.provider import (
    get_root_agent,
    get_session_service,
    get_memory_service,
    get_artifact_service,
)
from services.runner import Runner

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
