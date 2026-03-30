import fastapi
import fastapi.middleware.cors
import uvicorn

import config
import router.user_query


app = fastapi.FastAPI()
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router.user_query.router)


@app.get("/config")
def get_config():
    return {"llm_target": config.llm_target}


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
