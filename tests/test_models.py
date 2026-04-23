from datetime import UTC, datetime

from pipeline.models import DataBatch, ProcessedBatch


def test_databatch_stores_fields():
    batch = DataBatch(id="b1", records=[{"x": 1}], schema="raw_v1")
    assert batch.id == "b1"
    assert batch.records == [{"x": 1}]
    assert batch.schema == "raw_v1"


def test_databatch_received_at_defaults_to_now():
    before = datetime.now(UTC)
    batch = DataBatch(id="b1", records=[], schema="raw_v1")
    after = datetime.now(UTC)
    assert before <= batch.received_at <= after


def test_processedbatch_stores_fields():
    batch = ProcessedBatch(
        id="p1", source_id="b1", records=[{"processed": True}], schema="processed_v1"
    )
    assert batch.id == "p1"
    assert batch.source_id == "b1"
    assert batch.schema == "processed_v1"
    assert batch.records == [{"processed": True}]


def test_processedbatch_processed_at_defaults_to_now():
    before = datetime.now(UTC)
    batch = ProcessedBatch(id="p1", source_id="b1", records=[], schema="processed_v1")
    after = datetime.now(UTC)
    assert before <= batch.processed_at <= after
