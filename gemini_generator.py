import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def generate_workout_gemini(
    username,
    age,
    weight,
    goal,
    intensity
):

    prompt = f"""
Create a personalized 7-day workout plan.

Name: {username}
Age: {age}
Weight: {weight}
Goal: {goal}
Intensity: {intensity}

For each day provide:

Day
Warm-up
Main Workout
Sets and Repetitions
Rest
Cool-down

Make the plan simple and well structured.
"""

    model = genai.GenerativeModel(
        "gemini-1.5-pro"
    )

    response = model.generate_content(prompt)

    return response.text
