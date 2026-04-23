import aspectlib

from .aspects import audit_trail, log_execution, retry
from .stages import ExtractStage, LoadStage, TransformStage

# This runs exactly once when anything imports from `pipeline`.
# Every stage gets the full aspect stack woven in before
# any caller can instantiate them.

_STAGES = [ExtractStage, TransformStage, LoadStage]
_ASPECTS = [log_execution, retry, audit_trail]

for _stage in _STAGES:
    aspectlib.weave(_stage, _ASPECTS)
