from __future__ import annotations
import asyncio, json, os, time, uuid
from pathlib import Path
import psutil, yaml
from .adapters.openai_compatible import OpenAICompatibleBackend
from .quality import score
from .schemas import Experiment, Result, Sample

def load_experiment(path: str) -> Experiment:
    return Experiment.model_validate(yaml.safe_load(Path(path).read_text()))

def load_samples(path: str) -> list[Sample]:
    return [Sample.model_validate_json(line) for line in Path(path).read_text().splitlines() if line.strip()]

async def run_experiment(config_path: str, output_dir: str = "results") -> Path:
    exp = load_experiment(config_path); samples = load_samples(exp.dataset)
    run_id = f"{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    rows: list[Result] = []
    for target in exp.targets:
        backend = OpenAICompatibleBackend(target, exp.timeout_seconds)
        for sample in samples[:exp.warmup_requests]:
            try: await backend.generate(sample.prompt, min(16, exp.max_output_tokens), exp.temperature)
            except Exception: pass
        for concurrency in exp.concurrency:
            sem = asyncio.Semaphore(concurrency)
            async def one(sample: Sample):
                async with sem:
                    rss0 = psutil.Process().memory_info().rss
                    try:
                        r = await backend.generate(sample.prompt, exp.max_output_tokens, exp.temperature)
                        cost = r.input_tokens*target.input_cost_per_million/1e6 + r.output_tokens*target.output_cost_per_million/1e6
                        rows.append(Result(run_id=run_id, experiment=exp.name, target=target.name, model=target.model,
                            runtime=target.runtime, device=target.device, quantization=target.quantization,
                            sample_id=sample.id, task=sample.task, concurrency=concurrency,
                            input_tokens=r.input_tokens, output_tokens=r.output_tokens, ttft_ms=r.ttft_ms,
                            end_to_end_ms=r.end_to_end_ms, output_tokens_per_second=r.output_tokens/max(r.end_to_end_ms/1000, .001),
                            peak_rss_mb=max(rss0, psutil.Process().memory_info().rss)/1048576,
                            quality_score=score(sample.task, r.text, sample.reference), estimated_cost_usd=cost, success=True))
                    except Exception as e:
                        rows.append(Result(run_id=run_id, experiment=exp.name, target=target.name, model=target.model,
                            runtime=target.runtime, device=target.device, quantization=target.quantization,
                            sample_id=sample.id, task=sample.task, concurrency=concurrency, input_tokens=0,
                            output_tokens=0, ttft_ms=0, end_to_end_ms=0, output_tokens_per_second=0,
                            peak_rss_mb=psutil.Process().memory_info().rss/1048576, quality_score=0,
                            estimated_cost_usd=0, success=False, error=str(e)[:500]))
            jobs = [one(s) for _ in range(exp.repetitions) for s in samples]
            await asyncio.gather(*jobs)
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    path = out / f"{run_id}.jsonl"
    path.write_text("\n".join(r.model_dump_json() for r in rows) + "\n")
    return path

