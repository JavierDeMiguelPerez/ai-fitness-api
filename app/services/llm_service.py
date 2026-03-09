# app/services/llm_service.py
from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

MODEL_NAME = "llama-3.1-8b-instant"
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
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    raw_json_string = response.choices[0].message.content
    return json.loads(raw_json_string)

def modify_fitness_plan(current_plan: dict, modification_prompt: str) -> dict:
    system_prompt = """
    You are an elite AI fitness coach. 
    You will receive a current JSON workout plan and a user's request to modify it.
    Your task is to apply the requested modifications while keeping the rest of the plan intact.
    If the user asks to remove an exercise, ALWAYS replace it with a biomechanically similar alternative
    to maintain the total workout volume, unless the user explicitly asks to just delete it.
    You must output ONLY valid JSON. No markdown formatting, no conversational text.
    The JSON must strictly follow the exact same structure as the provided plan:
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
    
    user_prompt = f"Current Plan: {json.dumps(current_plan)}\n\nUser Modification Request: {modification_prompt}"
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    raw_json_string = response.choices[0].message.content
    return json.loads(raw_json_string)



def generate_diet_plan(user_profile: dict) -> dict:
    system_prompt = """
    You are an elite AI sports nutritionist. 
    Calculate the estimated daily caloric needs and macros based on the user's profile and goal.
    You must output ONLY valid JSON. No markdown formatting, no conversational text.
    The JSON must strictly follow this structure:
    {
        "plan_name": "string",
        "goal": "string",
        "days": [
            {
                "day_name": "string",
                "total_calories": 0,
                "meals": [
                    {
                        "meal_name": "string",
                        "description": "string",
                        "calories": 0,
                        "protein_g": 0,
                        "carbs_g": 0,
                        "fats_g": 0
                    }
                ]
            }
        ]
    }
    """
    
    user_prompt = f"Create a 3-day diet plan for this user profile: {json.dumps(user_profile)}"
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    raw_json_string = response.choices[0].message.content
    return json.loads(raw_json_string)

def analyze_meal_text(meal_text: str) -> dict:
    system_prompt = """
    You are an expert AI nutritionist and calorie estimator.
    The user will tell you what they just ate in natural language.
    Your job is to identify the food, estimate the total calories, and break down the macronutrients.
    You must output ONLY valid JSON. No markdown formatting, no conversational text.
    The JSON must strictly follow this structure:
    {
        "food_recognized": "string (a clean summary of what they ate)",
        "calories": 0,
        "protein_g": 0,
        "carbs_g": 0,
        "fats_g": 0
    }
    """
    
    user_prompt = f"Analyze this meal: {meal_text}"
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    raw_json_string = response.choices[0].message.content
    return json.loads(raw_json_string)

def modify_diet_plan(current_plan: dict, modification_prompt: str) -> dict:
    system_prompt = """
    You are an elite AI sports nutritionist. 
    You will receive a current JSON diet plan and a user's request to modify it.
    Your task is to apply the requested modifications while keeping the rest of the plan intact.
    IMPORTANT: If the user asks to remove a food, ALWAYS replace it with a nutritionally similar alternative (matching macros as close as possible) unless they explicitly ask to just delete it.
    You must output ONLY valid JSON. No markdown formatting, no conversational text.
    The JSON must strictly follow the exact same structure as the provided plan:
    {
        "plan_name": "string",
        "goal": "string",
        "days": [
            {
                "day_name": "string",
                "total_calories": 0,
                "meals": [
                    {
                        "meal_name": "string",
                        "description": "string",
                        "calories": 0,
                        "protein_g": 0,
                        "carbs_g": 0,
                        "fats_g": 0
                    }
                ]
            }
        ]
    }
    """
    
    user_prompt = f"Current Plan: {json.dumps(current_plan)}\n\nUser Modification Request: {modification_prompt}"
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    raw_json_string = response.choices[0].message.content
    return json.loads(raw_json_string)