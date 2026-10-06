from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel
from .runner import run_experiment

app = FastAPI(title="Inference Performance Lab", version="1.0.0")
class RunRequest(BaseModel): config: str = "configs/experiments/demo.yaml"

@app.get("/health")
def health(): return {"status": "ok"}

@app.post("/runs", status_code=202)
async def start(req: RunRequest, tasks: BackgroundTasks):
    tasks.add_task(run_experiment, req.config)
    return {"status": "accepted", "config": req.config}

