from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class DataBatch:
    id: str
    records: list[dict]
    schema: str
    received_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ProcessedBatch:
    id: str
    source_id: str
    records: list[dict]
    schema: str
    processed_at: datetime = field(default_factory=datetime.utcnow)
