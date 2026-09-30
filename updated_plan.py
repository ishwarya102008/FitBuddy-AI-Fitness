import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def update_workout_plan(original_plan, feedback):

    prompt = f"""
    Update the following workout plan based on the user's feedback.

    ORIGINAL WORKOUT PLAN:
    {original_plan}

    USER FEEDBACK:
    {feedback}

    Generate a revised 7-day workout plan.
    Keep the useful parts of the original plan
    and apply the requested changes.
    """

    model = genai.GenerativeModel(
        "gemini-1.5-pro"
    )

    response = model.generate_content(prompt)

    return response.text
