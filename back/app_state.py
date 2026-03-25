current_task = "intention seeking"
past_context_summary = ""
tool_for_execution_prompt = ""


def refresh_current_task_from_selected_tool(selected_tool: str) -> None:
    global current_task, tool_for_execution_prompt
    selected = selected_tool.strip()
    if selected != "nothing":
        current_task = "tool execution"
        tool_for_execution_prompt = selected
    else:
        current_task = "intention seeking"
        tool_for_execution_prompt = ""


def reset_after_tool_llm():
    global current_task, tool_for_execution_prompt
    current_task = "intention seeking"
    tool_for_execution_prompt = ""
