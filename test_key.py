import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

key = os.getenv("GROQ_API_KEY")
print(f"Debug: Your API Key is found as: {key}")

if not key:
    print("ERROR: Key is missing! Check your .env file.")
    exit()

if key.startswith("gsk_"):
    print("Format looks correct (starts with gsk_)")
else:
    print("WARNING: Key format looks wrong. Should start with 'gsk_'")

print("Attempting to contact Groq Cloud...")
try:
    llm = ChatGroq(temperature=0, groq_api_key=key, model_name="llama3-70b-8192")
    response = llm.invoke("Say 'System Operational' if you can hear me.")
    print(f"SUCCESS! AI Replied: {response.content}")
except Exception as e:
    print(f"CONNECTION FAILED: {e}")