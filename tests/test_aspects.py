import aspectlib
import pytest

from pipeline.aspects import (
    LineageStore,
    SchemaValidationError,
    TransientError,
    audit_trail,
    lineage_store,
    log_execution,
    retry,
)
from pipeline.models import DataBatch


# ---- Helpers -------------------------------------------------------------------


def _batch(batch_id="b1"):
    return DataBatch(id=batch_id, records=[{"x": 1}], schema="raw_v1")


class _SucceedingStage:
    def execute(self, batch):
        return batch


class _FlakyStage:
    def __init__(self, fail_times: int):
        self._fail_times = fail_times
        self._calls = 0

    def execute(self, batch):
        self._calls += 1
        if self._calls <= self._fail_times:
            raise TransientError("temporary blip")
        return batch


class _ExplodingStage:
    def execute(self, batch):
        raise ValueError("hard failure")


# ---- LineageStore --------------------------------------------------------------


def test_lineage_store_starts_empty():
    store = LineageStore()
    assert store.records == []


def test_lineage_store_records_entry():
    store = LineageStore()
    store.record(stage="X", input_id="a", output_id="b")
    assert len(store.records) == 1
    assert store.records[0]["stage"] == "X"


def test_lineage_store_accumulates():
    store = LineageStore()
    store.record(a=1)
    store.record(a=2)
    assert len(store.records) == 2


# ---- Exceptions ----------------------------------------------------------------


def test_transient_error_is_exception():
    assert issubclass(TransientError, Exception)


def test_schema_validation_error_is_exception():
    assert issubclass(SchemaValidationError, Exception)


# ---- retry aspect --------------------------------------------------------------


def test_retry_returns_on_first_success():
    batch = _batch()
    with aspectlib.weave(_SucceedingStage, retry):
        result = _SucceedingStage().execute(batch)
    assert result is batch


def test_retry_succeeds_after_transient_errors():
    batch = _batch()
    stage = _FlakyStage(fail_times=2)
    with aspectlib.weave(_FlakyStage, retry):
        result = stage.execute(batch)
    assert result is batch
    assert stage._calls == 3


def test_retry_raises_after_max_attempts():
    batch = _batch()
    stage = _FlakyStage(fail_times=3)
    with aspectlib.weave(_FlakyStage, retry):
        with pytest.raises(TransientError):
            stage.execute(batch)
    assert stage._calls == 3


def test_retry_does_not_swallow_other_exceptions():
    batch = _batch()
    with aspectlib.weave(_ExplodingStage, retry):
        with pytest.raises(ValueError):
            _ExplodingStage().execute(batch)


# ---- audit_trail aspect --------------------------------------------------------


def test_audit_trail_records_lineage():
    batch = _batch("input-001")
    with aspectlib.weave(_SucceedingStage, audit_trail):
        _SucceedingStage().execute(batch)
    assert len(lineage_store.records) == 1
    entry = lineage_store.records[0]
    assert entry["input_id"] == "input-001"
    assert entry["output_id"] == "input-001"
    assert entry["stage"] == "_SucceedingStage"
    assert "timestamp" in entry


def test_audit_trail_does_not_record_on_failure():
    batch = _batch()
    with aspectlib.weave(_ExplodingStage, audit_trail):
        with pytest.raises(ValueError):
            _ExplodingStage().execute(batch)
    assert lineage_store.records == []


# ---- log_execution aspect ------------------------------------------------------


def test_log_execution_passes_result_through(caplog):
    batch = _batch()
    with aspectlib.weave(_SucceedingStage, log_execution):
        result = _SucceedingStage().execute(batch)
    assert result is batch


def test_log_execution_logs_start_and_done(caplog):
    batch = _batch()
    with caplog.at_level("INFO"):
        with aspectlib.weave(_SucceedingStage, log_execution):
            _SucceedingStage().execute(batch)
    messages = caplog.text
    assert "Starting" in messages
    assert "Done in" in messages


def test_log_execution_logs_error_and_reraises(caplog):
    batch = _batch()
    with caplog.at_level("ERROR"):
        with aspectlib.weave(_ExplodingStage, log_execution):
            with pytest.raises(ValueError):
                _ExplodingStage().execute(batch)
    assert "Failed" in caplog.text
