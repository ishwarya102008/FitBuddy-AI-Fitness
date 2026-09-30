import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def generate_nutrition_tip_with_flash(goal):

    prompt = f"""
    Give one short and practical nutrition or recovery tip
    for a person whose fitness goal is {goal}.

    Keep it simple and easy to understand.
    """

    model = genai.GenerativeModel(
        "gemini-flash"
    )

    response = model.generate_content(prompt)

    return response.text
