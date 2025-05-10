from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings

# Global variable to hold the singleton instance
_config_instance: Optional["Config"] = None


# Define the Pydantic model for the application configuration
# Inherits from BaseSettings to automatically load from environment variables
class Config(BaseSettings):
    """
    Represents the application configuration settings.
    Values are loaded from environment variables.
    """
    PROJECT_ID: str = Field(..., description="The Google Cloud project ID.")
    LOCATION: str = Field(..., description="The Google Cloud region/location for resources.")
    USE_VERTEXAI: bool = Field(..., description="Boolean indicating if VertexAI is enabled.")
    APP_NAME: str = Field(..., description="A unique canonical name for the application.")
    DECKOFCARDS_URL: str = Field(..., description="URL for the Deckofcards API service to initialize client instance.")
    FIREBASE_KEY_JSON: str = Field(..., description="JSON content of the Firebase service account key.")
    CORS_ORIGINS: List[str] = Field(..., description="List of allowed origins for CORS.")
    IS_TESTING: Optional[bool] = Field(None, description="Boolean indicating if the application is running in a testing environment.")
    GCS_BUCKET: Optional[str] = Field(None, description="Google Cloud Storage bucket name (optional, used for GcsArtifactService).")
    DB_URL: Optional[str] = Field(None, description="Database connection URL (optional, used for DatabaseSessionService).")

    class Config:
        # Pydantic-settings specific configurations
        # For example, to load from a .env file:
        # env_file = ".env"
        # env_file_encoding = "utf-8"
        # extra = "ignore" # Ignore extra fields from environment
        pass


def get_config() -> Config:
    """
    Initializes and returns a singleton instance of the Config object.
    The configuration will be loaded from environment variables.
    """
    global _config_instance
    if _config_instance is None:
        # BaseSettings automatically reads from environment variables upon instantiation.
        _config_instance = Config()
    return _config_instance
