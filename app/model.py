import asyncio
from concurrent.futures import ThreadPoolExecutor

from opf import OPF

from .config import settings
from .schemas import Entity, FilterResult

_redactor: OPF | None = None
_executor = ThreadPoolExecutor(max_workers=1)


def load() -> None:
    global _redactor
    _redactor = OPF(
        model=settings.model_path,
        device=settings.device,
        output_mode=settings.output_mode,
        decode_mode=settings.decode_mode,
        trim_whitespace=settings.trim_whitespace,
        discard_overlapping_predicted_spans=settings.discard_overlapping_predicted_spans,
    )


def _build_result(raw) -> FilterResult:
    entities = [
        Entity(
            text=span.text,
            label=span.label,
            start=span.start,
            end=span.end,
            placeholder=span.placeholder,
        )
        for span in raw.detected_spans
    ]
    return FilterResult(redacted=raw.redacted_text, entities=entities)


def _run(texts: list[str]) -> list[FilterResult]:
    return [_build_result(_redactor.redact(text)) for text in texts]


async def process_batch(texts: list[str]) -> list[FilterResult]:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(_executor, _run, texts)
