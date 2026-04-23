import uuid

from .models import DataBatch, ProcessedBatch


class ExtractStage:
    """Validates and passes through the raw batch. In reality: fetch from source."""

    def execute(self, batch: DataBatch) -> DataBatch:
        # Simulate light validation/normalisation at extract time
        normalised = [
            {k.strip().lower(): v for k, v in record.items()}
            for record in batch.records
        ]
        return DataBatch(
            id=batch.id,
            records=normalised,
            schema=batch.schema,
        )


class TransformStage:
    """Applies business rules and produces a ProcessedBatch."""

    def execute(self, batch: DataBatch) -> ProcessedBatch:
        transformed = [
            {**record, "processed": True, "source_batch": batch.id}
            for record in batch.records
        ]
        return ProcessedBatch(
            id=str(uuid.uuid4()),
            source_id=batch.id,
            records=transformed,
            schema="processed_v1",
        )


class LoadStage:
    """Writes to the sink. Here we just return the batch to keep things simple."""

    def execute(self, batch: ProcessedBatch) -> ProcessedBatch:
        # In reality: write to warehouse, API, file, whatever
        return batch
