import fastapi
import pydantic

import app_state
import pipeline


router = fastapi.APIRouter()

MOCK_DATA_DISPLAY_FOR_FRONT = {
    "data_display": "array",
    "records": [
        {
            "Id": "00100001",
            "Name": "Acme Switzerland SA",
            "Industry": "Construction",
            "Type": "Customer",
            "CreatedDate": "2024-09-12",
        },
        {
            "Id": "00100002",
            "Name": "Beta Retail AG",
            "Industry": "Retail",
            "Type": "Partner",
            "CreatedDate": "2025-01-03",
        },
        {
            "Id": "00100003",
            "Name": "Gamma Architecture Sàrl",
            "Industry": "Architecture",
            "Type": "Customer",
            "CreatedDate": "2025-02-20",
        },
    ],
}


class UserQueryRequest(pydantic.BaseModel):
    user_nl_request: str


@router.post("/user_query")
def user_query(request: UserQueryRequest):
    llm_response = pipeline.run_pipeline(request.user_nl_request)
    current_exchange_summary = llm_response["conversation_summary"].strip()
    selected_tool = llm_response["selected_tool"].strip()
    app_state.refresh_current_task_from_selected_tool(selected_tool)

    app_state.past_context_summary = (
        f"{app_state.past_context_summary.strip()} {current_exchange_summary}".strip()
    )

    response = {
        "assistant_response": llm_response["assistant_response"],
        "conversation_summary": app_state.past_context_summary,
        "selected_tool": selected_tool,
    }
    if selected_tool == "data_query":
        try:
            pipeline.run_data_query_tool_llm(request.user_nl_request)
            response["data_display"] = MOCK_DATA_DISPLAY_FOR_FRONT["data_display"]
            response["records"] = MOCK_DATA_DISPLAY_FOR_FRONT["records"]
        finally:
            app_state.reset_after_tool_llm()
    return response
