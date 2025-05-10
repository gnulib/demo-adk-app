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
    # Uses APP_HOST and APP_PORT from config if available, otherwise defaults.
    host = getattr(app_config, 'HOST', "0.0.0.0")
    port = getattr(app_config, 'PORT', 8000)

    # Run the application using Uvicorn
    print(f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
