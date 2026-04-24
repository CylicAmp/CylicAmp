"""
FastAPI/Starlette HTTP middleware for filtering text/plain request bodies.
Intercepts requests with Content-Type: text/plain before they reach route handlers.
"""

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def text_filter_middleware(request: Request, call_next):
    # Only handle text/plain requests
    if request.headers.get("content-type", "") != "text/plain":
        return await call_next(request)

    body = await request.body()
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError:
        return await call_next(request)

    # Apply filtering logic here
    filtered_text = text  # replace with your logic

    # Rebuild request (FastAPI/Starlette compatible)
    async def receive():
        return {"type": "http.request", "body": filtered_text.encode()}

    new_request = Request(request.scope, receive=receive)
    return await call_next(new_request)
