from openai import OpenAI

from src.client.model.config import OPENAI_API_KEY, SYSTEM_PROMPT

model = OpenAI(api_key=OPENAI_API_KEY)


def global_model(model_name: str, messages):
    chat = model.chat.completions.create(
        model=model_name,
        temperature=1,
        max_tokens=2048,
        top_p=1,
        messages=messages,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={"type": "text"},
    )
    return chat
