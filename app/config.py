from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "S.N.A.R.E. System"
    API_SECRET_KEY: str
    GROQ_API_KEY: str

    REDIS_URL: Optional[str] = None
    
    GUVI_CALLBACK_URL: str = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
    DEBUG_MODE: bool = True  

    class Config:
        env_file = ".env"
        extra = "ignore" 

@lru_cache()
def get_settings():
    return Settings()