import asyncio
from concurrent.futures import ThreadPoolExecutor

from transformers import pipeline as hf_pipeline

from .config import settings
from .schemas import Entity, FilterResult

_pipe = None
# Single worker prevents concurrent GPU access
_executor = ThreadPoolExecutor(max_workers=1)


def load() -> None:
    global _pipe
    _pipe = hf_pipeline(
        "token-classification",
        model=settings.model_name,
        device=settings.device,
        aggregation_strategy=settings.aggregation_strategy,
    )


def _build_result(text: str, raw_entities: list[dict]) -> FilterResult:
    # Replace entities back-to-front so offsets stay valid during substitution
    sorted_ents = sorted(raw_entities, key=lambda e: e["start"], reverse=True)
    entities: list[Entity] = []
    redacted = text
    for ent in sorted_ents:
        label = ent.get("entity_group", ent.get("entity", "PII"))
        entities.append(
            Entity(text=ent["word"], label=label, start=ent["start"], end=ent["end"])
        )
        redacted = redacted[: ent["start"]] + f"[{label}]" + redacted[ent["end"] :]
    entities.sort(key=lambda e: e.start)
    return FilterResult(redacted=redacted, entities=entities)


def _run(texts: list[str]) -> list[FilterResult]:
    results: list[FilterResult] = []
    for i in range(0, len(texts), settings.max_batch_size):
        chunk = texts[i : i + settings.max_batch_size]
        batch: list[list[dict]] = _pipe(chunk, batch_size=len(chunk))
        results.extend(_build_result(t, e) for t, e in zip(chunk, batch))
    return results


async def process_batch(texts: list[str]) -> list[FilterResult]:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(_executor, _run, texts)
