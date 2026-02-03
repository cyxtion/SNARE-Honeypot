import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
key = os.getenv("GROQ_API_KEY")

print(f"?? Key loaded: {key[:10]}...")

try:
    print("?? Contacting Groq (Llama 3.3)...")
    llm = ChatGroq(temperature=0, groq_api_key=key, model_name="llama-3.3-70b-versatile")
    response = llm.invoke("Are you operational? Reply with 'SYSTEM ONLINE'.")
    print(f"?? SUCCESS! AI Replied: {response.content}")
except Exception as e:
    print(f"? ERROR: {e}")
