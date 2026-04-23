import pytest

from pipeline.aspects import lineage_store
from pipeline.models import DataBatch


@pytest.fixture(autouse=True)
def reset_lineage():
    lineage_store._records.clear()
    yield
    lineage_store._records.clear()


@pytest.fixture
def raw_batch():
    return DataBatch(
        id="batch-001",
        records=[
            {"Name": "Alice", "Score": 91},
            {"Name": "Bob", "Score": 74},
        ],
        schema="raw_v1",
    )
