import configparser

import app_state


def build_prompt_intention_seeking():
    company_parser = configparser.ConfigParser()
    company_parser.read("prompts/company.ini")
    agent_role_parser = configparser.ConfigParser()
    agent_role_parser.read("prompts/agent_role.ini")
    past_context_parser = configparser.ConfigParser()
    past_context_parser.read("prompts/past_context.ini")
    output_format_parser = configparser.ConfigParser()
    output_format_parser.read("prompts/output_format.ini")
    tooling_parser = configparser.ConfigParser()
    tooling_parser.read("prompts/toolings.ini")
    available_tools_parser = configparser.ConfigParser()
    available_tools_parser.read("tool/available_tools.ini")
    company_definition = company_parser["company"]["definition"]
    agent_role_definition = agent_role_parser["agent_role"]["role"]
    past_context_instruction = past_context_parser["past_context"]["summary"]
    output_format_instruction = output_format_parser["output_format"]["instruction"]
    tooling_instruction = tooling_parser["tooling"]["instruction"]
    available_tools = available_tools_parser["tools"]
    available_tools_text = "\n".join(
        [f"{tool_name}: {tool_description}" for tool_name, tool_description in available_tools.items()]
    )
    return "\n".join(
        [
            company_definition,
            agent_role_definition,
            past_context_instruction,
            "Contexte precedent condense:",
            app_state.past_context_summary,
            tooling_instruction,
            "Outils disponibles:",
            available_tools_text,
            output_format_instruction,
        ]
    )


def _build_prompt_tool_execution_data_query():
    company_parser = configparser.ConfigParser()
    company_parser.read("prompts/company.ini")
    agent_role_parser = configparser.ConfigParser()
    agent_role_parser.read("prompts/agent_role.ini")
    past_context_parser = configparser.ConfigParser()
    past_context_parser.read("prompts/past_context.ini")
    company_definition = company_parser["company"]["definition"]
    agent_role_definition = agent_role_parser["agent_role"]["role"]
    past_context_instruction = past_context_parser["past_context"]["summary"]
    tool_parser = configparser.ConfigParser()
    tool_parser.read("prompts/tool_data_query.ini")
    section = tool_parser["tool_data_query"]
    instruction = section["instruction"]
    expected_output = section["expected_output"]
    parts = [
        company_definition,
        agent_role_definition,
        past_context_instruction,
        "Contexte precedent condense:",
        app_state.past_context_summary,
        instruction,
        expected_output,
    ]
    return "\n".join(parts)


def _build_prompt_tool_execution_data_summarizer():
    company_parser = configparser.ConfigParser()
    company_parser.read("prompts/company.ini")
    agent_role_parser = configparser.ConfigParser()
    agent_role_parser.read("prompts/agent_role.ini")
    company_definition = company_parser["company"]["definition"]
    agent_role_definition = agent_role_parser["agent_role"]["role"]
    tool_parser = configparser.ConfigParser()
    tool_parser.read("prompts/tool_data_summarizer.ini")
    section = tool_parser["tool_data_summarizer"]
    instruction = section["instruction"]
    expected_output = section["expected_output"]
    parts = [
        company_definition,
        agent_role_definition,
        instruction,
        expected_output,
    ]
    return "\n".join(parts)


def _build_prompt_tool_execution_data_grapher():
    company_parser = configparser.ConfigParser()
    company_parser.read("prompts/company.ini")
    agent_role_parser = configparser.ConfigParser()
    agent_role_parser.read("prompts/agent_role.ini")
    company_definition = company_parser["company"]["definition"]
    agent_role_definition = agent_role_parser["agent_role"]["role"]
    tool_parser = configparser.ConfigParser()
    tool_parser.read("prompts/tool_data_grapher.ini")
    section = tool_parser["tool_data_grapher"]
    instruction = section["instruction"]
    expected_output = section["expected_output"]
    parts = [
        company_definition,
        agent_role_definition,
        instruction,
        expected_output,
    ]
    return "\n".join(parts)


tool_execution_prompt_builders = {
    "data_query": _build_prompt_tool_execution_data_query,
    "data_summarizer": _build_prompt_tool_execution_data_summarizer,
    "data_grapher": _build_prompt_tool_execution_data_grapher,
}


def build_prompt_tool_execution():
    return tool_execution_prompt_builders[app_state.tool_for_execution_prompt]()


prompt_builders = {
    "intention seeking": build_prompt_intention_seeking,
    "tool execution": build_prompt_tool_execution,
}


def build_prompt():
    return prompt_builders[app_state.current_task]()
