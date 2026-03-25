import os

import config
import dotenv
import openai


def call_openai(payload):
    dotenv.load_dotenv()
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=config.openai_model,
        temperature=config.temperature,
        messages=[
            {"role": "system", "content": payload["system"]},
            *payload["messages"],
        ],
    )
    return response.choices[0].message.content
