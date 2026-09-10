"""Sandbox file seeded 2026-09-10 to test whether CodeRabbit (and other
review tools) catch "self.X referenced but never assigned" bugs -- a
pattern found for real in a workshop PR review (demand_profiler.py:57:
self.adi_threshold / self.cv2_threshold used in classify() but never set
in __init__). Not in the original 14-bug test set
(three-tool-accuracy-comparison.md) -- these variants test coverage on
this new pattern, from a direct miss to one that needs call-graph tracing.
"""
from __future__ import annotations


class DemandProfiler:
    """Case 1: direct miss -- same shape as the real bug found live."""

    def __init__(self, adi_col: str, cv2_col: str) -> None:
        self.adi_col = adi_col
        self.cv2_col = cv2_col
        # self.adi_threshold / self.cv2_threshold never assigned here

    def classify(self, adi: float, cv2: float) -> str:
        if adi > self.adi_threshold and cv2 > self.cv2_threshold:
            return "erratic"
        return "smooth"


class ConditionalConfig:
    """Case 2: only assigned on one branch of __init__ -- undefined on
    the other branch's code path."""

    def __init__(self, use_cache: bool) -> None:
        self.use_cache = use_cache
        if use_cache:
            self.cache_ttl_seconds = 3600

    def get_ttl(self) -> int:
        return self.cache_ttl_seconds  # AttributeError if use_cache=False


class BaseValidator:
    """Case 3: base class references an attribute it expects a subclass
    to set -- an informal "abstract contract", arguably not always a real
    bug. Included to see whether the tool false-positives here."""

    def validate(self, value: float) -> bool:
        return value <= self.max_allowed  # never set in this class


class StrictValidator(BaseValidator):
    def __init__(self, max_allowed: float) -> None:
        self.max_allowed = max_allowed


class LazySetup:
    """Case 4: attribute is set by a helper method that's never actually
    called from __init__ -- requires tracing the call graph, not just
    scanning __init__ line by line."""

    def __init__(self, path: str) -> None:
        self.path = path
        # self._setup() was meant to be called here but isn't

    def _setup(self) -> None:
        self.handle = open(self.path)

    def read(self) -> str:
        return self.handle.read()  # AttributeError -- _setup() never ran
