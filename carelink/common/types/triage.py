from dataclasses import dataclass

@dataclass
class PreliminaryTriage:
    severity: str | None = None
    summary: str | None = None

