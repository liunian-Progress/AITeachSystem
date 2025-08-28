from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
import httpx

app = FastAPI()

# 前端页面
@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", encoding="utf-8") as f:
        return f.read()

# 流式代理接口
@app.post("/stream-chat")
async def stream_chat(request: Request):
    data = await request.json()
    api_key = "app-X2rVmrT5w8TDCOuoDHjgYrgd"  # 替换成你自己的
    url = "http://47.120.30.18:8099/v1/chat-messages"

    async def event_stream():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", url,
                                     headers={
                                         "Authorization": f"Bearer {api_key}",
                                         "Content-Type": "application/json"
                                     },
                                     json={**data, "response_mode": "streaming"}) as r:
                async for chunk in r.aiter_bytes():
                    if chunk:
                        yield chunk

    return StreamingResponse(event_stream(), media_type="text/event-stream")