from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CacheKeyDTO:
    key: str


@dataclass(frozen=True, slots=True)
class MapperDTO:
    text: str
    call: str
