import logging
import uuid

# Importing pipeline runs __init__.py, which runs the weaver.
# By the time the next line finishes, every stage is already woven.
from pipeline.aspects import lineage_store
from pipeline.models import DataBatch
from pipeline.stages import ExtractStage, TransformStage, LoadStage


def run(batch: DataBatch) -> None:
    extracted  = ExtractStage().execute(batch)
    transformed = TransformStage().execute(extracted)
    LoadStage().execute(transformed)


if __name__ == "__main__":
    incoming = DataBatch(
        id=str(uuid.uuid4()),
        records=[
            {"Name": "Alice", "Score": 91},
            {"Name": "Bob",   "Score": 74},
            {"Name": "Carol", "Score": 88},
        ],
        schema="raw_v1",
    )

    print("\n=== PIPELINE RUN ===\n")
    run(incoming)

    print("\n=== LINEAGE TRAIL ===\n")
    for entry in lineage_store.records:
        print(f"  {entry}")
