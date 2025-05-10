from typing import List, Optional
from pydantic import BaseModel, Field

# Global variable to hold the singleton instance
_config_instance: Optional["Config"] = None


# Define the Pydantic model for the application configuration
class Config(BaseModel):
    """
    Represents the application configuration settings.
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
        # This inner Config class is used by Pydantic for its own configuration,
        # e.g., to enable ORM mode or to provide example data.
        # For environment variable loading, you'd typically use pydantic-settings' BaseSettings.
        # Since BaseModel is requested, direct instantiation or a custom loader is implied.
        pass


def get_config() -> Config:
    """
    Initializes and returns a singleton instance of the Config object.
    The configuration will be loaded based on Pydantic's default mechanisms
    (e.g., environment variables if BaseSettings were used, or direct instantiation).
    """
    global _config_instance
    if _config_instance is None:
        # Here, you would typically load from environment variables or a config file.
        # Since we are using BaseModel, an explicit instantiation with values is expected
        # or a custom loading mechanism. For now, this will raise validation errors
        # if required fields are not provided during instantiation.
        # This example assumes that Pydantic will be used with environment variables
        # (if Config was derived from BaseSettings) or that values are passed explicitly.
        # For the purpose of this example, we'll rely on Pydantic's default behavior
        # which for BaseModel means explicit provision of data or it will fail validation
        # if fields are required and not provided.
        # A more complete solution would involve loading from .env files or environment.
        _config_instance = Config()
    return _config_instance

# Example of how you might load it if you were using pydantic-settings
# from pydantic_settings import BaseSettings
# class Settings(BaseSettings):
#     PROJECT_ID: str
#     LOCATION: str
#     ...
#     class Config:
#         env_file = ".env" # example
#
# _settings_instance: Optional[Settings] = None
# def get_settings() -> Settings:
#    global _settings_instance
#    if _settings_instance is None:
#        _settings_instance = Settings()
#    return _settings_instance
