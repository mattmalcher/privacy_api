from pydantic import BaseModel


class FilterRequest(BaseModel):
    inputs: list[str]


class Entity(BaseModel):
    text: str
    label: str
    start: int
    end: int


class FilterResult(BaseModel):
    redacted: str
    entities: list[Entity]


class FilterResponse(BaseModel):
    results: list[FilterResult]
