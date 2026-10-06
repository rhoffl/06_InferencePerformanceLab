from __future__ import annotations
import json, os, time
import httpx
from .base import Backend, Response
from ..schemas import Target

class OpenAICompatibleBackend(Backend):
    def __init__(self, target: Target, timeout: float = 120):
        self.target = target
        self.key = os.getenv(target.api_key_env or "", "")
        self.client = httpx.AsyncClient(timeout=timeout)

    async def generate(self, prompt: str, max_tokens: int, temperature: float) -> Response:
        headers = {"Content-Type": "application/json"}
        if self.key:
            headers["Authorization"] = f"Bearer {self.key}"
        payload = {"model": self.target.model, "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": max_tokens, "temperature": temperature, "stream": True}
        started = time.perf_counter_ns(); first = None; pieces = []; usage = {}
        async with self.client.stream("POST", f"{self.target.base_url.rstrip('/')}/chat/completions",
                                      headers=headers, json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line.startswith("data: ") or line == "data: [DONE]":
                    continue
                event = json.loads(line[6:])
                usage = event.get("usage") or usage
                delta = event.get("choices", [{}])[0].get("delta", {}).get("content")
                if delta:
                    first = first or time.perf_counter_ns(); pieces.append(delta)
        ended = time.perf_counter_ns()
        text = "".join(pieces)
        inp = usage.get("prompt_tokens", max(1, len(prompt.split())))
        out = usage.get("completion_tokens", max(1, len(text.split())))
        return Response(text, inp, out, ((first or ended)-started)/1e6, (ended-started)/1e6)

