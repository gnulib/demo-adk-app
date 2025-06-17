from datetime import datetime
from pydantic import BaseModel, Field

# Pydantic Models
class Conversation(BaseModel):
    conv_id: str
    updated_at: datetime

class Message(BaseModel):
    text: str

class StreamingEvent(BaseModel):
    type: str = Field(None, description="type of the event: start, error, action, message, end")
    data: str = Field(None, description="string payload for the event, specific to type")