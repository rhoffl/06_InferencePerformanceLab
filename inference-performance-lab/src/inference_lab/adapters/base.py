from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Response:
    text: str
    input_tokens: int
    output_tokens: int
    ttft_ms: float
    end_to_end_ms: float

class Backend(ABC):
    @abstractmethod
    async def generate(self, prompt: str, max_tokens: int, temperature: float) -> Response: ...

