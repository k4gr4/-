from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY が設定されていまんん！")

client = genai.Client(api_key=GEMINI_API_KEY)

def ask_gemini(prompt: str) -> str:
    res = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    return getattr(res, "text", None) or "……沈黙です。"
