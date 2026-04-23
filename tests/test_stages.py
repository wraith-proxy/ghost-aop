import pytest

from pipeline.models import DataBatch, ProcessedBatch
from pipeline.stages import ExtractStage, LoadStage, TransformStage


def test_extract_lowercases_and_strips_keys(raw_batch):
    dirty = DataBatch(
        id="b1",
        records=[{" Name ": "Alice", "  SCORE  ": 91}],
        schema="raw_v1",
    )
    result = ExtractStage().execute(dirty)
    assert result.records == [{"name": "Alice", "score": 91}]


def test_extract_preserves_id_and_schema(raw_batch):
    result = ExtractStage().execute(raw_batch)
    assert result.id == raw_batch.id
    assert result.schema == raw_batch.schema


def test_extract_preserves_values(raw_batch):
    result = ExtractStage().execute(raw_batch)
    values = [r["score"] for r in result.records]
    assert values == [91, 74]


def test_extract_returns_databatch(raw_batch):
    result = ExtractStage().execute(raw_batch)
    assert isinstance(result, DataBatch)


def test_transform_produces_processed_batch(raw_batch):
    extracted = ExtractStage().execute(raw_batch)
    result = TransformStage().execute(extracted)
    assert isinstance(result, ProcessedBatch)


def test_transform_sets_processed_flag(raw_batch):
    extracted = ExtractStage().execute(raw_batch)
    result = TransformStage().execute(extracted)
    assert all(r["processed"] is True for r in result.records)


def test_transform_adds_source_batch_reference(raw_batch):
    extracted = ExtractStage().execute(raw_batch)
    result = TransformStage().execute(extracted)
    assert all(r["source_batch"] == extracted.id for r in result.records)


def test_transform_sets_schema_and_source_id(raw_batch):
    extracted = ExtractStage().execute(raw_batch)
    result = TransformStage().execute(extracted)
    assert result.schema == "processed_v1"
    assert result.source_id == extracted.id


def test_transform_generates_unique_ids(raw_batch):
    extracted = ExtractStage().execute(raw_batch)
    id_a = TransformStage().execute(extracted).id
    id_b = TransformStage().execute(extracted).id
    assert id_a != id_b


def test_load_returns_batch_unchanged(raw_batch):
    extracted = ExtractStage().execute(raw_batch)
    processed = TransformStage().execute(extracted)
    result = LoadStage().execute(processed)
    assert result is processed


@pytest.mark.parametrize(
    "records",
    [
        [],
        [{"only": "one"}],
        [{"a": 1}, {"b": 2}, {"c": 3}],
    ],
)
def test_extract_handles_various_record_counts(records):
    batch = DataBatch(id="x", records=records, schema="raw_v1")
    result = ExtractStage().execute(batch)
    assert len(result.records) == len(records)
