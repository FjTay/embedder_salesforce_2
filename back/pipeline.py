import json

import llm.llm
import llm.llm_utils
import prompts.prompts_utils


def _log_pretty_json(label, data):
    try:
        print(f"{label}:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except TypeError:
        print(f"{label} (non JSON): {data}")


def run_pipeline(user_nl_request):
    system_prompt = prompts.prompts_utils.build_prompt()
    payload = {
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": user_nl_request}
        ],
    }
    model_raw = llm.llm.call_llm(payload)
    current_parsed = llm.llm_utils.parse_llm_json(model_raw)
    _log_pretty_json("current_parsed", current_parsed)
    return {
        "assistant_response": current_parsed["assistant_response"],
        "conversation_summary": current_parsed["conversation_summary"],
        "selected_tool": current_parsed["selected_tool"],
    }


def run_data_query_tool_llm(user_nl_request):
    system_prompt = prompts.prompts_utils.build_prompt()
    payload = {
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_nl_request}],
    }
    model_raw = llm.llm.call_llm(payload)
    parsed = llm.llm_utils.parse_llm_json(model_raw)
    _log_pretty_json("data_query_tool_llm", parsed)
    return parsed
