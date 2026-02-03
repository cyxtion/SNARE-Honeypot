from pydantic import BaseModel, Field
from typing import List, Optional, Any, Union, Dict

class AgentResponse(BaseModel):
    status: str = "success"
    reply: str

class IncomingRequest(BaseModel):
    sessionId: Optional[Union[str, int, Any]] = Field(default="unknown_session")
    message: Optional[Union[Dict[str, Any], str, Any]] = None
    sender: Optional[str] = "unknown"
    text: Optional[str] = None
    timestamp: Optional[Any] = 0
    conversationHistory: Optional[List[Any]] = []
    metadata: Optional[Any] = None

    class Config:
        extra = "ignore"