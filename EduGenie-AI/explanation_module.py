import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = os.getenv(
    "LOCAL_EXPLANATION_MODEL",
    "MBZUAI/LaMini-Flan-T5-783M"
)

_tokenizer = None
_model = None


def get_explanation_model():
    global _tokenizer, _model

    if _tokenizer is None or _model is None:
        print("Loading local explanation model...")

        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

        _model = AutoModelForSeq2SeqLM.from_pretrained(
            MODEL_NAME
        )

        print("Local explanation model loaded.")

    return _tokenizer, _model


def explain_topic(topic: str) -> str:

    prompt = f"""
Explain the following topic to a beginner student.

Topic:
{topic}

Instructions:
- Use very simple English.
- Explain the meaning first.
- Explain the important points step by step.
- Give a simple example if possible.
- Avoid difficult technical words.
- Keep the explanation concise and easy to understand.
"""

    tokenizer, model = get_explanation_model()

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=250,
        do_sample=False
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return answer