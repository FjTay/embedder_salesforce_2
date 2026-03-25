import llm.claude_client
import llm.openai_client
import config


def call_llm(payload):
    available_llms = {
        "OPENAI": lambda: llm.openai_client.call_openai(payload),
        "CLAUDE": lambda: llm.claude_client.call_claude(payload),
    }
    current = config.llm_target.upper()
    return available_llms[current]()
