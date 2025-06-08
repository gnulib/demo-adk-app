import firebase_admin
from firebase_admin import auth as firebase_auth # Alias to avoid conflict with local 'auth'
from fastapi import Depends, HTTPException, status, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated, Optional, Dict

from utils.config import Config
from google.adk.sessions import Session as AdkSession, BaseSessionService

# Module-level globals to store config and session service
_config_instance: Optional[Config] = None
_session_service_instance: Optional[BaseSessionService] = None

# HTTPBearer security scheme
security_scheme = HTTPBearer()

def init_auth_module(config: Config, session_service: BaseSessionService):
    """
    Initializes the authentication module with necessary configurations and services.
    This should be called once during application startup.
    """
    global _config_instance, _session_service_instance
    _config_instance = config
    _session_service_instance = session_service

    # Initialize Firebase Admin SDK if not already initialized
    # Uses GOOGLE_APPLICATION_CREDENTIALS environment variable by default
    if not firebase_admin._apps:
        firebase_admin.initialize_app()

async def get_authenticated_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)]
) -> Dict:
    """
    Verifies the Firebase ID token from the Authorization header.
    Returns the decoded token (user payload) if valid.
    """
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        return decoded_token
    except firebase_auth.InvalidIdTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Firebase ID token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e: # Catch other potential errors during verification
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_authorized_session(
    conversation_id: Annotated[str, Path(description="The ID of the conversation to access.")],
    user: Annotated[Dict, Depends(get_authenticated_user)]
) -> AdkSession:
    """
    Retrieves a conversation session if the authenticated user is authorized.
    Checks if the auth module has been initialized.
    """
    if not _config_instance or not _session_service_instance:
        # This indicates a server-side configuration error.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication module not properly initialized on the server."
        )

    user_id = user.get("uid")
    if not user_id:
        # This should ideally be caught by token verification, but as a safeguard:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID (uid) not found in token.",
        )

    try:
        app_name_to_use = _config_instance.AGENT_ID if _config_instance.AGENT_ID else _config_instance.APP_NAME
        adk_session: Optional[AdkSession] = await _session_service_instance.get_session(
            session_id=conversation_id, user_id=user_id, app_name=app_name_to_use
        )
        if not adk_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Conversation not found or user not authorized."
            )
        return adk_session
    except HTTPException: # Re-raise known HTTPExceptions (like the 404 above)
        raise
    except Exception as e:
        # Log the exception e if you have logging setup
        # print(f"Error retrieving session: {e}") # Basic print for debugging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"An error occurred while retrieving the conversation: {str(e)}"
        )
