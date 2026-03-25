import json


def parse_llm_json(raw_response):
    content = raw_response.strip()
    content = content.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        json_start = content.find("{")
        json_end = content.rfind("}") + 1
        if json_start < 0 or json_end <= json_start:
            raise ValueError(f"Invalid LLM JSON response: {raw_response}")
        return json.loads(content[json_start:json_end])
