import asyncio, json, time
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()
@app.get("/health")
def health(): return {"status": "ok"}

@app.post("/v1/chat/completions")
async def complete(body: dict):
    prompt = body["messages"][-1]["content"]
    text = '{"customer":"Acme","amount":1250,"invoice_date":"2026-09-01"}' if "invoice" in prompt.lower() else "Paris"
    async def events():
        for word in text.split():
            await asyncio.sleep(.01)
            event = {"choices":[{"delta":{"content":word+" "}}]}
            yield f"data: {json.dumps(event)}\n\n"
        usage = {"prompt_tokens":len(prompt.split()),"completion_tokens":len(text.split())}
        yield f"data: {json.dumps({'choices':[{'delta':{}}], 'usage':usage})}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(events(), media_type="text/event-stream")

