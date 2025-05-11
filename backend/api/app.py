from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, status, Response, Request
# Pydantic models are now in api.models
from google.adk.events import Event # Assuming this path is correct for your project structure
from google.adk.sessions import BaseSessionService, Session as AdkSession
from google.adk.memory import BaseMemoryService
from google.adk.artifacts import BaseArtifactService

from utils.config import Config
from api.models import Conversation, Message # Import models from the new module
from services.runner import Runner # Import the Runner class

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
        # For example, to enable CORS if your config.CORS_ORIGINS is set:
        from fastapi.middleware.cors import CORSMiddleware
        if config.CORS_ORIGINS:
            origins = [origin.strip() for origin in config.CORS_ORIGINS.split(',') if origin.strip()]
            if origins:
                _app.add_middleware(
                    CORSMiddleware,
                    allow_origins=origins,
                    allow_credentials=True,
                    allow_methods=["*"],
                allow_headers=["*"],
            )

        USER_ID = "hard_coded_user-01" # Hardcoded user ID as per requirement

        @_app.post("/conversations", response_model=Conversation, status_code=status.HTTP_201_CREATED)
        async def create_conversation(request: Request):
            """
            Creates a new conversation session.
            """
            session_service: BaseSessionService = request.app.state.session_service
            app_config: Config = request.app.state.config
            
            try:
                adk_session: AdkSession = await session_service.create_session(
                    user_id=USER_ID, app_id=app_config.APP_NAME
                )
                return Conversation(conv_id=adk_session.id, updated_at=adk_session.last_update_time)
            except Exception as e:
                # Log the exception e
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        @_app.get("/conversations", response_model=List[Conversation])
        async def get_conversations(request: Request):
            """
            Retrieves a list of all conversations for the hardcoded user.
            """
            session_service: BaseSessionService = request.app.state.session_service
            app_config: Config = request.app.state.config
            try:
                adk_sessions: List[AdkSession] = await session_service.list_sessions(
                    user_id=USER_ID, app_name=app_config.APP_NAME
                )
                return [
                    Conversation(conv_id=s.id, updated_at=s.last_update_time) for s in adk_sessions
                ]
            except Exception as e:
                # Log the exception e
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        @_app.post("/conversations/{conversation_id}/messages", response_model=Message)
        async def send_message(request: Request, conversation_id: str, message_request: Message):
            """
            Sends a message to a specific conversation and gets a response from the agent.
            """
            session_service: BaseSessionService = request.app.state.session_service
            app_runner: Runner = request.app.state.runner
            app_config: Config = request.app.state.config

            try:
                adk_session: Optional[AdkSession] = await session_service.get_session(
                    session_id=conversation_id, user_id=USER_ID, app_id=app_config.APP_NAME
                )
                if not adk_session:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
                
                response_message = await app_runner.invoke(session=adk_session, msg=message_request)
                return response_message
            except HTTPException: # Re-raise HTTPException
                raise
            except Exception as e:
                # Log the exception e
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        @_app.get("/conversations/{conversation_id}/history", response_model=List[Event])
        async def get_conversation_history(request: Request, conversation_id: str):
            """
            Retrieves the event history for a specific conversation.
            """
            session_service: BaseSessionService = request.app.state.session_service
            app_config: Config = request.app.state.config
            try:
                adk_session: Optional[AdkSession] = await session_service.get_session(
                    session_id=conversation_id, user_id=USER_ID, app_id=app_config.APP_NAME
                )
                if not adk_session:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
                return adk_session.history
            except HTTPException: # Re-raise HTTPException
                raise
            except Exception as e:
                # Log the exception e
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        @_app.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete_conversation(request: Request, conversation_id: str):
            """
            Deletes a specific conversation.
            """
            session_service: BaseSessionService = request.app.state.session_service
            app_config: Config = request.app.state.config
            try:
                await session_service.delete_session(
                    session_id=conversation_id, user_id=USER_ID, app_id=app_config.APP_NAME
                )
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                # Log the exception e
                # Consider if a 404 should be returned if delete is attempted on non-existent session,
                # depending on session_service.delete_session behavior.
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return _app
