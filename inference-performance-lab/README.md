# Inference Performance Lab

A reproducible portfolio project for evaluating LLM serving configurations across quality, throughput, latency, memory, and cost.

## What it compares

- Hosted and OpenAI-compatible local endpoints
- CPU, GPU, runtime, and quantization metadata
- Concurrency and batch-oriented serving configurations
- Short and long-context datasets
- Cold/warm cache and speculative-decoding configurations
- Quality, TTFT, end-to-end latency, throughput, process memory, reliability, and token cost

The included mock server makes the project runnable without a GPU or API key. Real vLLM, llama.cpp, TGI, and hosted endpoints can be added through YAML because they expose compatible APIs.

## Quick start

```bash
cp .env.example .env
docker compose up --build -d
docker compose exec api inference-lab run configs/experiments/demo.yaml
```

Open:

- API and documentation: http://localhost:8006/docs
- Dashboard: http://localhost:8501
- Mock model health: http://localhost:9006/health

## Real benchmark

1. Copy `configs/experiments/hosted-local-template.yaml`.
2. Pin exact model identifiers and revisions.
3. Set current provider prices; never rely on stale hard-coded prices.
4. Start the local server separately and update its URL.
5. Add versioned JSONL workloads with reference answers.
6. Run each configuration several times and report confidence intervals.

```bash
inference-lab run configs/experiments/my-run.yaml
```

## Required experiment controls

Record model/tokenizer revision, prompt template, runtime/container version, CPU/GPU, RAM/VRAM, drivers, quantization algorithm, decoding parameters, concurrency, cache state, input/output token distribution, warmups, repetitions, and test timestamp. Hosted results are observations of a provider on a particular date, not permanent properties of a model.

## Extending the lab

- **Quantization:** create targets for FP16/BF16, INT8, AWQ/GPTQ INT4, or GGUF Q4/Q5/Q8.
- **CPU/GPU:** serve the same model revision with llama.cpp CPU and GPU-offload configurations.
- **Batching:** compare continuous-batching server settings while independently varying client concurrency.
- **Context:** create datasets bucketed at 512, 2K, 8K, 16K, and 32K input tokens.
- **Caching:** repeat identical shared prefixes under cold and warm cache states; record hit rate.
- **Speculative decoding:** compare the same primary model with decoding disabled and enabled; record draft model and acceptance rate.
- **Hardware telemetry:** add NVIDIA DCGM/Prometheus for true VRAM, utilization, power, and energy measurements. The starter currently records benchmark-process RSS only.

## Why fastest or largest is not automatically best

Production selection is constrained optimization. First discard configurations that fail required quality, p95 latency, privacy, context, or reliability thresholds. Among eligible choices, compare cost per successful task—not merely cost per token. A fast small model can lose through invalid outputs and retries; a large model can lose when marginal quality does not justify memory, latency, and cost. Plot the Pareto frontier and avoid declaring a universal winner.

## Honest limitations

- Provider internals and model revisions may be opaque.
- Client RSS is not GPU VRAM; add DCGM or NVML before making hardware claims.
- The demo's quantization label is simulated and proves orchestration only.
- Network latency, rate limits, cache state, and time of day can confound hosted comparisons.
- LLM-as-judge scoring can be biased; prefer deterministic task metrics wherever possible.

## Portfolio evidence

Publish configuration files, dataset manifests/hashes, raw request-level measurements, aggregation notebooks, environment details, and a short decision report. Highlight p50/p95/p99 latency, quality confidence intervals, failure rate, memory, and cost per successful task.

