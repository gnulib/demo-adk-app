from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from google.adk.events import Event # Assuming this path is correct for your project structure

from utils.config import Config


# Pydantic Models
class Conversation(BaseModel):
    conv_id: str
    updated_at: datetime

class Message(BaseModel):
    text: str

# Global variable to hold the singleton FastAPI app instance
_app: Optional[FastAPI] = None


def get_fast_api_app(config: Config) -> FastAPI:
    """
    Initializes and returns a singleton instance of the FastAPI application.

    Args:
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

        @_app.post("/conversations", response_model=Conversation, status_code=status.HTTP_201_CREATED)
        async def create_conversation():
            """
            Creates a new conversation.
            Placeholder: Replace with actual logic to create and store a new conversation session.
            """
            # Example placeholder logic:
            # new_conv_id = "conv_" + str(uuid.uuid4()) # Requires import uuid
            # new_updated_at = datetime.utcnow()
            # Store this new conversation details
            print("Placeholder: Creating a new conversation.")
            return Conversation(conv_id="new_sample_conv_id", updated_at=datetime.utcnow())

        @_app.get("/conversations", response_model=List[Conversation])
        async def get_conversations():
            """
            Retrieves a list of all conversations.
            Placeholder: Replace with actual logic to fetch conversations from a data store.
            """
            print("Placeholder: Fetching all conversations.")
            # Example placeholder logic:
            return [
                Conversation(conv_id="sample_conv_1", updated_at=datetime.utcnow()),
                Conversation(conv_id="sample_conv_2", updated_at=datetime.utcnow())
            ]

        @_app.post("/conversations/{conversation_id}/messages", response_model=Message)
        async def send_message(conversation_id: str, message_request: Message):
            """
            Sends a message to a specific conversation.
            Placeholder: Replace with actual logic to find the conversation,
                         process the message (e.g., with an agent), and store it.
            """
            print(f"Placeholder: Sending message to conversation {conversation_id}: '{message_request.text}'")
            # Example placeholder logic:
            # 1. Validate conversation_id exists
            # 2. Process message_request.text (e.g., call an agent)
            # 3. Store the message and agent's response if any
            # For now, just echoing the received message text
            return Message(text=f"Received in {conversation_id}: {message_request.text}")

        @_app.get("/conversations/{conversation_id}/history", response_model=List[Event])
        async def get_conversation_history(conversation_id: str):
            """
            Retrieves the event history for a specific conversation.
            Placeholder: Replace with actual logic to fetch events (e.g., from google.adk.events format)
                         associated with the conversation_id.
            """
            print(f"Placeholder: Fetching history for conversation {conversation_id}.")
            # Example placeholder logic:
            # This would typically involve querying a database or event store.
            # The structure of Event objects will depend on google.adk.events.
            return [] # Return an empty list as a placeholder

        @_app.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete_conversation(conversation_id: str):
            """
            Deletes a specific conversation.
            Placeholder: Replace with actual logic to delete the conversation and its associated data.
            """
            print(f"Placeholder: Deleting conversation {conversation_id}.")
            # Example placeholder logic:
            # 1. Find and delete conversation data by conversation_id
            # If not found, you might raise HTTPException(status_code=404, detail="Conversation not found")
            # On successful deletion, return a 204 response.
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    return _app
