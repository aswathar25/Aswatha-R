import json

from ai_client import generate_with_gemini


def clean_json_block(text: str) -> str:
    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def generate_quiz(topic: str):
    prompt = f"""
Create a quiz for a student about:

{topic}

Create exactly 3 multiple-choice questions.

For each question:
- Give exactly 4 options.
- Give one correct answer.
- The answer must exactly match one of the four options.

Return ONLY valid JSON.

Use this format:

[
  {{
    "question": "Question here",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Correct option"
  }}
]
"""

    response = generate_with_gemini(prompt)

    cleaned = clean_json_block(response)

    quiz = json.loads(cleaned)

    if not isinstance(quiz, list) or len(quiz) != 3:
        raise ValueError("Quiz must contain exactly 3 questions.")

    for item in quiz:
        if not all(key in item for key in ["question", "options", "answer"]):
            raise ValueError("Invalid quiz format.")

        if len(item["options"]) != 4:
            raise ValueError("Each question must have exactly 4 options.")

        if item["answer"] not in item["options"]:
            raise ValueError(
                "The correct answer must match one of the options."
            )

    return quiz