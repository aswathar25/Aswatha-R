import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash"
)


def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Please add your Gemini API key to the .env file."
        )

    return genai.Client(api_key=api_key)


def generate_with_gemini(prompt: str) -> str:
    client = get_gemini_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text