from fastapi import FastAPI, Request
from middleware import SmartFilterMiddleware

app = FastAPI()

app.add_middleware(
    SmartFilterMiddleware,
    enable_profanity_filter=True,
    enable_pii_redaction=True,
    enable_json_wrapper=True,
    rate_limit=60,
    log_file="filter_log.txt",
    custom_filters=[
        lambda t: t.replace("badword", "goodword")
    ]
)


@app.post("/chat")
async def chat(request: Request):
    body = await request.body()
    return {"received": body.decode()}


@app.get("/")
async def root():
    return {"status": "filter middleware active"}
