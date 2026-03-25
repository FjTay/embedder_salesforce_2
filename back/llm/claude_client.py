import os

import anthropic
import config
import dotenv


def call_claude(payload):
    dotenv.load_dotenv()
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model=config.claude_model,
        temperature=config.temperature,
        max_tokens=1024,
        system=payload["system"],
        messages=payload["messages"],
    )
    return response.content[0].text
