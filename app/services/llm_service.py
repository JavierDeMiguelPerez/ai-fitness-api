# app/services/llm_service.py
from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

MODEL_NAME = "llama3-8b-8192"
import json

def generate_fitness_plan(user_profile: dict) -> dict:
    system_prompt = """
    You are a professional AI fitness coach. 
    You must output ONLY valid JSON. No markdown formatting, no conversational text.
    The JSON must strictly follow this structure:
    {
        "plan_name": "string",
        "goal": "string",
        "days": [
            {
                "day_name": "string",
                "exercises": [
                    {"name": "string", "sets": 0, "reps": "string", "rest_seconds": 0}
                ]
            }
        ]
    }
    """
    
    user_prompt = f"Create a workout plan for this user profile: {json.dumps(user_profile)}"
    
    # 3. TODO: Haz la llamada a client.chat.completions.create()
    # Pásale los dos mensajes (system y user)
    # ¡Y no olvides añadir response_format={"type": "json_object"} !
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    # 4. Extraemos el texto y lo convertimos a un diccionario Python real
    raw_json_string = response.choices[0].message.content
    return json.loads(raw_json_string)