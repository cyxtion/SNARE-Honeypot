from fastapi import FastAPI, Header, HTTPException, BackgroundTasks
from app.config import get_settings
from app.api.v1.models import IncomingRequest, AgentResponse
from app.core.intelligence import harvester
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger()

app = FastAPI(title="S.N.A.R.E. Enterprise System")

@app.post("/honey-pot", response_model=AgentResponse)
async def honey_pot_endpoint(
    payload: IncomingRequest, 
    background_tasks: BackgroundTasks,
    x_api_key: str = Header(None)
):
    if x_api_key != settings.API_SECRET_KEY:
        logger.warning(f"Unauthorized Access: {x_api_key}")
        raise HTTPException(status_code=401, detail="Invalid API Key")

    logger.info(f"Received Session: {payload.sessionId}")

    intel_data = harvester.analyze(payload.text)
    if intel_data:
        logger.success(f"Intelligence Found: {intel_data}")

    response_text = "I am confused. Can you explain that again?"

    return {
        "status": "success",
        "reply": response_text
    }

@app.get("/")
def health_check():
    return {"system": "S.N.A.R.E.", "status": "online"}