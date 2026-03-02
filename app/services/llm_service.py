# app/services/llm_service.py
from groq import Groq
from app.core.config import settings

# Inicializamos el cliente usando nuestra API Key validada
client = Groq(api_key=settings.GROQ_API_KEY)

# Usaremos Llama 3 de 8 billones de parámetros (súper rápido y gratis)
MODEL_NAME = "llama3-8b-8192"

def generate_fitness_plan(prompt: str) -> str:
    # TODO: Aquí haremos la llamada a la API de Groq más adelante
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content