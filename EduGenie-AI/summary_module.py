from ai_client import generate_with_gemini


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following text for a college student.

Text:
{text}

Instructions:
- Keep the summary concise.
- Include the main ideas.
- Use simple language.
- Use bullet points when useful.
- Do not add information that is not present in the original text.
"""

    return generate_with_gemini(prompt)