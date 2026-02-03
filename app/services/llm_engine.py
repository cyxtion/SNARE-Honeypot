import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import get_settings
from app.core.prompts import SYSTEM_INSTRUCTIONS, PERSONA_ROLES

settings = get_settings()

class SnareBrain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.7,
            model_name="llama-3.3-70b-versatile", 
            groq_api_key=settings.GROQ_API_KEY
        )

    def select_persona(self, text: str) -> str:
        text = text.lower()
        if any(w in text for w in ["block", "kyc", "pan", "account"]):
            return "bank_scam"
        elif any(w in text for w in ["win", "lottery", "prize", "congrats"]):
            return "lottery_scam"
        elif any(w in text for w in ["job", "hiring", "salary"]):
            return "job_scam"
        return "default"

    async def generate_response(self, text: str, history: list) -> str:
        scenario = self.select_persona(text)
        role_description = PERSONA_ROLES[scenario]

        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_INSTRUCTIONS),
            ("user", "SCAMMER SAYS: {text}\nHISTORY: {history}")
        ])

        chain = prompt | self.llm | StrOutputParser()

        history_text = "\n".join([f"{msg.sender}: {msg.text}" for msg in history[-3:]])
        
        try:
            return await chain.ainvoke({
                "persona_role": role_description,
                "context": "Incoming Scam Attempt",
                "text": text,
                "history": history_text
            })
        except Exception as e:
            return "I am sorry, my internet is slow. What did you say?"

brain = SnareBrain()
