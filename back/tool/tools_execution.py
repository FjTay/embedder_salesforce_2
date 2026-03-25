import tool.data_query_tool


def _data_query(user_nl_request):
    print("data_query execution")
    return tool.data_query_tool.run_data_query(user_nl_request)


def _data_summarizer(user_nl_request):
    print("data_summarizer execution")


def _data_grapher(user_nl_request):
    print("data_grapher execution")


def _nothing(user_nl_request):
    print("nothing execution")


available_tools = {
    "data_query": _data_query,
    "data_summarizer": _data_summarizer,
    "data_grapher": _data_grapher,
    "nothing": _nothing,
}


def execute_tool(selected_tool, user_nl_request):
    return available_tools[selected_tool](user_nl_request)
