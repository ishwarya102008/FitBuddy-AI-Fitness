import os
from google import genai
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Create Gemini client
client = genai.Client(api_key=API_KEY)


def generate_fitness_response(user_message):
    prompt = f"""
You are GetFit Buddy, a friendly wellness assistant.

User message:
{user_message}

Give a simple, supportive and easy-to-understand response.
Do not provide medical diagnosis or treatment.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":
    print("GetFit Buddy AI is ready!")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("GetFit Buddy: Bye! Stay healthy 😊")
            break

        answer = generate_fitness_response(user_input)
        print("GetFit Buddy:", answer)
