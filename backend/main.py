import uvicorn

from api.app import get_fast_api_app
from utils.config import get_config

if __name__ == "__main__":
    # Load application configuration
    app_config = get_config()

    # Create FastAPI application instance
    # The get_fast_api_app function should use app_config to set up the app
    app = get_fast_api_app(app_config)

    # Determine host and port for Uvicorn
    # HOST will default to "0.0.0.0" if not set in environment by Pydantic,
    # but it's better to define it in Config if it's always needed.
    # For now, assuming HOST might not always be in config, but PORT is.
    host = getattr(app_config, 'HOST', "0.0.0.0") # Or add HOST to Config model
    port = app_config.PORT

    # Run the application using Uvicorn
    print(f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
