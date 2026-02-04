from fastapi import FastAPI, Header, HTTPException, BackgroundTasks, Request
from app.config import get_settings
from app.api.v1.models import AgentResponse
from app.core.intelligence import harvester
from app.services.llm_engine import brain
from app.services.callback_worker import execute_guvi_callback
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger()

app = FastAPI(title="S.N.A.R.E. Enterprise System")

@app.post("/honey-pot", response_model=AgentResponse)
async def honey_pot_endpoint(
    background_tasks: BackgroundTasks,
    request: Request,
    x_api_key: str = Header(None)
):
    if x_api_key != settings.API_SECRET_KEY:
        logger.warning(f"Unauthorized Access Attempt: {x_api_key}")
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        body = await request.json()
    except Exception:
        body = {}

    session_id = body.get("sessionId", "unknown_session")
    
    user_text = body.get("text")
    if not user_text and isinstance(body.get("message"), dict):
        user_text = body["message"].get("text")
    elif not user_text and isinstance(body.get("message"), str):
        user_text = body["message"]
    
    if not user_text:
        user_text = "Hello"

    logger.info(f"Received Session: {session_id} | Input: {user_text[:50]}...")

    intel_data = harvester.analyze(user_text) or {}
    
    if intel_data:
        logger.success(f"Intelligence Extracted: {intel_data}")

    found_critical = (len(intel_data.get("upi", [])) > 0 or 
                      len(intel_data.get("bank_account", [])) > 0 or
                      len(intel_data.get("url", [])) > 0)
    
    history = body.get("conversationHistory", [])
    if not isinstance(history, list):
        history = []
        
    current_msg_count = len(history) + 1

    if found_critical:
        logger.info(f"Triggering Background Report for Session {session_id}")
        background_tasks.add_task(
            execute_guvi_callback, 
            session_id, 
            intel_data, 
            current_msg_count
        )

    try:
        reply_text = await brain.generate_response(user_text, history)
    except Exception as e:
        logger.error(f"Brain Engine Failure: {e}")
        reply_text = "I am sorry, my internet is very slow right now. Can you tell me that again?"

    return {
        "status": "success",
        "reply": reply_text
    }

@app.get("/")
def health_check():
    return {"status": "online", "version": "2.5.0-NoValidation"}