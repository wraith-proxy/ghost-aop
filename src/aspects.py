import logging
import time
from datetime import datetime

import aspectlib

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)


# ---- Exceptions ----------------------------------------------------------------

class TransientError(Exception):
    """Retriable failure. Network blips, temporary unavailability, that sort of thing."""


class SchemaValidationError(Exception):
    """Output schema didn't match what we expected. Someone changed something."""


# ---- Lineage store (in-memory for the example) ---------------------------------

class LineageStore:
    def __init__(self):
        self._records: list[dict] = []

    def record(self, **kwargs):
        self._records.append(kwargs)
        logging.info(f"  [LINEAGE] {kwargs}")

    @property
    def records(self):
        return self._records


lineage_store = LineageStore()


# ---- Aspects -------------------------------------------------------------------

@aspectlib.Aspect
def log_execution(*args, **kwargs):
    """Logs entry, exit, and elapsed time for any stage.execute() call."""
    stage_name = args[0].__class__.__name__ if args else "unknown"
    logging.info(f"[{stage_name}] Starting")
    start = time.perf_counter()
    try:
        result = yield aspectlib.Proceed
        elapsed = time.perf_counter() - start
        logging.info(f"[{stage_name}] Done in {elapsed:.4f}s")
        yield aspectlib.Return(result)
    except Exception as e:
        logging.error(f"[{stage_name}] Failed: {e}")
        raise


@aspectlib.Aspect
def retry(*args, **kwargs):
    """Retries on TransientError up to 3 times before giving up."""
    stage_name = args[0].__class__.__name__ if args else "unknown"
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            result = yield aspectlib.Proceed
            yield aspectlib.Return(result)
            return
        except TransientError as e:
            if attempt == max_attempts - 1:
                logging.error(f"[{stage_name}] All {max_attempts} attempts failed.")
                raise
            logging.warning(
                f"[{stage_name}] Attempt {attempt + 1} failed ({e}), retrying..."
            )


@aspectlib.Aspect
def audit_trail(*args, **kwargs):
    """Records input/output lineage after successful execution."""
    result = yield aspectlib.Proceed
    lineage_store.record(
        stage=args[0].__class__.__name__,
        input_id=args[1].id,
        output_id=result.id,
        timestamp=datetime.utcnow().isoformat(),
    )
    yield aspectlib.Return(result)
