from pydantic import BaseModel, Field
from typing import List, Optional, Any, Union

class AgentResponse(BaseModel):
    status: str = "success"
    reply: str

class IncomingRequest(BaseModel):
    sessionId: Union[str, int, Any] = Field(..., description="Session ID")

    message: Optional[Any] = None 

    sender: Optional[str] = "unknown"

    text: Optional[str] = ""

    timestamp: Optional[Any] = 0

    conversationHistory: Optional[List[Any]] = []

    metadata: Optional[Any] = None

    class Config:
        extra = "ignore"