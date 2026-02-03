from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List, Union

class AgentResponse(BaseModel):
    status: str = "success"
    reply: str
class IncomingRequest(BaseModel):
    sessionId: Optional[Union[str, int, Any]] = "unknown_session"
    message: Optional[Union[Dict[str, Any], str, Any]] = None
    text: Optional[str] = None
    sender: Optional[str] = "scammer"
    conversationHistory: Optional[List[Any]] = []
    metadata: Optional[Any] = None

    class Config:
        extra = "allow"