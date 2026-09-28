import os
from groq import Groq

_client = Groq(api_key=os.environ["GROQ_API_KEY"])

MODEL = "openai/gpt-oss-120b"
FALLBACK_MODEL = "qwen/qwen3-32b"


def generate_response(prompt: str) -> str:
    """
    Sends the prompt to Groq and returns the raw text response.
    Falls back to a second model if the first one errors out.
    """
    try:
        completion = _client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"\n[groq_llm] Primary model failed ({e}), trying fallback...")
        completion = _client.chat.completions.create(
            model=FALLBACK_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return completion.choices[0].message.content
    