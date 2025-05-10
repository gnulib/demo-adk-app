from typing import Optional
from fastapi import FastAPI
from utils.config import Config

# Global variable to hold the singleton FastAPI app instance
_fastapi_app_instance: Optional[FastAPI] = None


def get_fast_api_app(config: Config) -> FastAPI:
    """
    Initializes and returns a singleton instance of the FastAPI application.

    Args:
        config: The application configuration object.

    Returns:
        A FastAPI application instance.
    """
    global _fastapi_app_instance
    if _fastapi_app_instance is None:
        _fastapi_app_instance = FastAPI(
            title=config.APP_NAME,
            # You can add other FastAPI parameters here if needed,
            # for example, version, description, etc.
            # version="0.1.0",
            # description="My Awesome API",
        )
        # You can add middleware, exception handlers, routers, etc. here
        # For example:
        # from fastapi.middleware.cors import CORSMiddleware
        # _fastapi_app_instance.add_middleware(
        # CORSMiddleware,
        # allow_origins=config.CORS_ORIGINS,
        # allow_credentials=True,
        # allow_methods=["*"],
        # allow_headers=["*"],
        # )
    return _fastapi_app_instance
