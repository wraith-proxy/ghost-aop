from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class DataBatch:
    id: str
    records: list[dict]
    schema: str
    received_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class ProcessedBatch:
    id: str
    source_id: str
    records: list[dict]
    schema: str
    processed_at: datetime = field(default_factory=lambda: datetime.now(UTC))
