from datetime import datetime
from pydantic import BaseModel

# Pydantic Models
class Conversation(BaseModel):
    conv_id: str
    updated_at: datetime

class Message(BaseModel):
    text: str
