from datetime import datetime
from typing import List, Optional, Any, Dict, Annotated # Added Any, Dict, Annotated

from fastapi import FastAPI, HTTPException, status, Response, Request, Depends
# Pydantic models are now in api.models
from google.adk.events import Event # Assuming this path is correct for your project structure
from google.adk.sessions import BaseSessionService, Session as AdkSession # Removed ListSessionsResponse
from google.adk.memory import BaseMemoryService
from google.adk.artifacts import BaseArtifactService

from utils.config import Config
from api.models import Conversation, Message # Import models from the new module
from services.runner import Runner # Import the Runner class
from api.auth import get_authenticated_user, get_authorized_session # Import auth dependencies

# Global variable to hold the singleton FastAPI app instance
_app: Optional[FastAPI] = None


def get_fast_api_app(
    runner: Runner,
    session_service: BaseSessionService,
    memory_service: BaseMemoryService,
    artifact_service: BaseArtifactService,
    config: Config,
) -> FastAPI:
    """
    Initializes and returns a singleton instance of the FastAPI application.

    Args:
        runner: The application's agent runner instance.
        session_service: The session service instance.
        memory_service: The memory service instance.
        artifact_service: The artifact service instance.
        config: The application configuration object.

    Returns:
        A FastAPI application instance.
    """
    global _app
    if _app is None:
        _app = FastAPI(
            title=config.APP_NAME,
            # You can add other FastAPI parameters here if needed,
            # for example, version, description, etc.
            # version="0.1.0",
            # description="My Awesome API",
        )

        # Store services and runner on app.state for access in endpoints
        _app.state.runner = runner
        _app.state.session_service = session_service
        _app.state.memory_service = memory_service
        _app.state.artifact_service = artifact_service
        _app.state.config = config # Storing config as well if needed in endpoints

        # You can add middleware, exception handlers, routers, etc. here
        # For example, to enable CORS:
        from fastapi.middleware.cors import CORSMiddleware
        
        origins_from_config = []
        if config.CORS_ORIGINS:
            origins_from_config = [origin.strip() for origin in config.CORS_ORIGINS.split(',') if origin.strip()]

        # If CORS_ORIGINS is not set or is empty after parsing, 
        # and if IS_TESTING is true, default to common development origin.
        # For production, CORS_ORIGINS should be explicitly configured.
        final_origins = origins_from_config
        if not final_origins and config.IS_TESTING:
            final_origins = ["http://localhost:3000"] # Default for React dev server during testing
        
        if final_origins: # Ensure there's at least one origin to allow
            _app.add_middleware(
                CORSMiddleware,
                allow_origins=final_origins,
                allow_credentials=True,
                allow_methods=["*"], # Allows all methods
                allow_headers=["*"], # Allows all headers
            )

        # USER_ID = "hard_coded_user-01" # Hardcoded user ID removed, will use authenticated user's ID

        @_app.post("/conversations", response_model=Conversation, status_code=status.HTTP_201_CREATED)
        async def create_conversation(
            request: Request,
            user: Annotated[Dict, Depends(get_authenticated_user)]
        ):
            """
            Creates a new conversation session for the authenticated user.
            """
            session_service: BaseSessionService = request.app.state.session_service
            app_config: Config = request.app.state.config
            user_id = user.get("uid")
            
            try:
                app_name_to_use = app_config.AGENT_ID if app_config.AGENT_ID else app_config.APP_NAME
                adk_session: AdkSession = session_service.create_session(
                    user_id=user_id, app_name=app_name_to_use
                )
                return Conversation(conv_id=adk_session.id, updated_at=adk_session.last_update_time)
            except Exception as e:
                # Log the exception e
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        @_app.get("/conversations", response_model=List[Conversation])
        async def get_conversations(
            request: Request,
            user: Annotated[Dict, Depends(get_authenticated_user)]
        ):
            """
            Retrieves a list of all conversations for the authenticated user.
            """
            session_service: BaseSessionService = request.app.state.session_service
            app_config: Config = request.app.state.config
            user_id = user.get("uid")
            try:
                app_name_to_use = app_config.AGENT_ID if app_config.AGENT_ID else app_config.APP_NAME
                list_sessions_response: Any = session_service.list_sessions(
                    user_id=user_id, app_name=app_name_to_use
                )
                adk_sessions: List[AdkSession] = list_sessions_response.sessions
                return [
                    Conversation(conv_id=s.id, updated_at=s.last_update_time) for s in adk_sessions
                ]
            except Exception as e:
                # Log the exception e
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        @_app.post("/conversations/{conversation_id}/messages", response_model=Message)
        async def send_message(
            request: Request, 
            message_request: Message,
            adk_session: Annotated[AdkSession, Depends(get_authorized_session)] # Injects authorized session
        ):
            """
            Sends a message to a specific conversation and gets a response from the agent.
            User authorization for the conversation is handled by get_authorized_session.
            """
            app_runner: Runner = request.app.state.runner
            try:
                response_message = await app_runner.invoke(session=adk_session, msg=message_request)
                return response_message
            except HTTPException: # Re-raise HTTPException
                raise
            except Exception as e:
                # Log the exception e
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        @_app.get("/conversations/{conversation_id}/history", response_model=List[Event])
        async def get_conversation_history(
            adk_session: Annotated[AdkSession, Depends(get_authorized_session)] # Injects authorized session
        ):
            """
            Retrieves the event history for a specific conversation.
            User authorization for the conversation is handled by get_authorized_session.
            """
            try:
                return adk_session.events
            except HTTPException: # Re-raise HTTPException
                raise
            except Exception as e:
                # Log the exception e
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        @_app.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete_conversation(
            request: Request,
            adk_session: Annotated[AdkSession, Depends(get_authorized_session)] # Injects authorized session
        ):
            """
            Deletes a specific conversation.
            User authorization for the conversation is handled by get_authorized_session.
            """
            session_service: BaseSessionService = request.app.state.session_service
            app_config: Config = request.app.state.config
            try:
                app_name_to_use = app_config.AGENT_ID if app_config.AGENT_ID else app_config.APP_NAME
                session_service.delete_session(
                    session_id=adk_session.id, user_id=adk_session.user_id, app_name=app_name_to_use
                )
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                # Log the exception e
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return _app
