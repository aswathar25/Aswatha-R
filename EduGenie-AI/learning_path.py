from ai_client import generate_with_gemini


def recommend_learning_path(topic: str) -> str:
    prompt = f"""
Create a beginner-friendly learning path for:

{topic}

Include:

1. Prerequisites
2. Beginner level
3. Intermediate level
4. Advanced level
5. Practice activities
6. A mini project
7. Useful resource types
8. Suggested timeline
9. Final project idea

Keep the explanation simple and practical for a college student.
"""

    return generate_with_gemini(prompt)