from fastapi import FastAPI, Header, HTTPException, BackgroundTasks, Request
from app.config import get_settings
from app.api.v1.models import IncomingRequest, AgentResponse
from app.core.intelligence import harvester
from app.services.llm_engine import brain
from app.services.callback_worker import execute_guvi_callback
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger()

app = FastAPI(title="S.N.A.R.E. Enterprise System")

@app.post("/honey-pot", response_model=AgentResponse)
async def honey_pot_endpoint(
    payload: IncomingRequest, 
    background_tasks: BackgroundTasks,
    request: Request,
    x_api_key: str = Header(None)
):
    if x_api_key != settings.API_SECRET_KEY:
        logger.warning(f"Unauthorized Access Attempt: {x_api_key}")
        raise HTTPException(status_code=401, detail="Invalid API Key")

    user_text = payload.text
    if not user_text and isinstance(payload.message, dict):
        user_text = payload.message.get("text")
    if not user_text:
        try:
            raw_body = await request.json()
            user_text = raw_body.get("message", {}).get("text") or raw_body.get("text")
        except:
            pass

    if not user_text:
        user_text = "Hello"

    logger.info(f"Received Session: {payload.sessionId} | Input: {user_text[:50]}...")

    intel_data = harvester.analyze(user_text) or {}
    
    if intel_data:
        logger.success(f"Intelligence Extracted: {intel_data}")

    found_critical = (len(intel_data.get("upi", [])) > 0 or 
                      len(intel_data.get("bank_account", [])) > 0 or
                      len(intel_data.get("url", [])) > 0)
    
    current_msg_count = len(payload.conversationHistory) + 1 if payload.conversationHistory else 1

    if found_critical:
        logger.info(f"Triggering Background Report for Session {payload.sessionId}")
        background_tasks.add_task(
            execute_guvi_callback, 
            payload.sessionId, 
            intel_data, 
            current_msg_count
        )
    try:
        reply_text = await brain.generate_response(user_text, payload.conversationHistory or [])
    except Exception as e:
        logger.error(f"Brain Engine Failure: {e}")
        reply_text = "I am sorry, my internet is very slow right now. Can you tell me that again?"

    return {
        "status": "success",
        "reply": reply_text
    }

@app.get("/")
def health_check():
    return {"system": "S.N.A.R.E.", "status": "online", "version": "2.3.0-Universal"}