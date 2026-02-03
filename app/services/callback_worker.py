import requests
from app.config import get_settings
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger()

def execute_guvi_callback(session_id: str, intel_data: dict, msg_count: int):
    try:
        payload = {
            "sessionId": session_id,
            "scamDetected": True,
            "totalMessagesExchanged": msg_count,
            "extractedIntelligence": {
                "bankAccounts": intel_data.get("bank_account", []),
                "upilds": intel_data.get("upi", []),
                "phishingLinks": intel_data.get("url", []),
                "phoneNumbers": intel_data.get("phone", []),
                "suspiciousKeywords": intel_data.get("suspicious_keywords", [])
            },
            "agentNotes": "S.N.A.R.E. System: Target engaged."
        }
        
        logger.info(f"?? [CALLBACK] Reporting Session {session_id} to GUVI...")
            
    except Exception as e:
        logger.error(f"? [CALLBACK EXCEPTION] {e}")
