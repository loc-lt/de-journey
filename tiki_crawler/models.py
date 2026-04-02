from __future__ import annotations

from dataclasses import dataclass
from typing import Any

@dataclass
class FetchResult:
    product_id: int
    ok: bool
    status_code: int | None
    elapsed_s: float
    payload: dict[str, Any] | None = None
    error: str | None = None
