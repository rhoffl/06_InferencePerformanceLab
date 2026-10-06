from __future__ import annotations
from pydantic import BaseModel, Field

class Target(BaseModel):
    name: str
    base_url: str
    model: str
    api_key_env: str | None = None
    runtime: str = "openai-compatible"
    device: str = "hosted"
    quantization: str = "unknown"
    hourly_cost_usd: float | None = None
    input_cost_per_million: float = 0
    output_cost_per_million: float = 0

class Experiment(BaseModel):
    name: str
    dataset: str
    targets: list[Target]
    concurrency: list[int] = Field(default_factory=lambda: [1])
    repetitions: int = 3
    warmup_requests: int = 2
    max_output_tokens: int = 128
    temperature: float = 0
    timeout_seconds: float = 120

class Sample(BaseModel):
    id: str
    task: str
    prompt: str
    reference: object | None = None

class Result(BaseModel):
    run_id: str
    experiment: str
    target: str
    model: str
    runtime: str
    device: str
    quantization: str
    sample_id: str
    task: str
    concurrency: int
    input_tokens: int
    output_tokens: int
    ttft_ms: float
    end_to_end_ms: float
    output_tokens_per_second: float
    peak_rss_mb: float
    quality_score: float
    estimated_cost_usd: float
    success: bool
    error: str | None = None

