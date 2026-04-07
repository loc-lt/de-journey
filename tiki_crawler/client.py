from __future__ import annotations

import asyncio
import importlib.util
import random
import time

import httpx

from tiki_crawler.models import FetchResult


API_URL = "https://api.tiki.vn/product-detail/api/v1/products/{product_id}"
DEFAULT_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "user-agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
}


def create_client() -> httpx.AsyncClient:
    """Create one shared HTTP client so connections can be reused efficiently."""
    use_http2 = importlib.util.find_spec("h2") is not None
    return httpx.AsyncClient(
        headers=DEFAULT_HEADERS,
        http2=use_http2,
        follow_redirects=True,
    )


def create_sync_client() -> httpx.Client:
    """Retry recheck runs sequentially, so a sync client is simpler to reason about."""
    use_http2 = importlib.util.find_spec("h2") is not None
    return httpx.Client(
        headers=DEFAULT_HEADERS,
        http2=use_http2,
        follow_redirects=True,
    )


def build_backoff_delay(attempt: int) -> float:
    """Use exponential backoff with a little jitter to avoid request bursts."""
    return (2**attempt) + random.uniform(0, 0.3)


async def fetch_product(
    product_id: int,
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    timeout_s: float,
    max_retries: int,
) -> FetchResult:
    """
    Fetch one product detail document.

    Each request is wrapped in its own retry loop so that one failing product
    does not interrupt the rest of the batch.
    """
    async with semaphore:
        last_error = "unknown_error"
        for attempt in range(max_retries + 1):
            started = time.perf_counter()
            try:
                response = await client.get(API_URL.format(product_id=product_id), timeout=timeout_s)
                elapsed_s = time.perf_counter() - started
                status = response.status_code

                if status == 200:
                    return FetchResult(
                        product_id=product_id,
                        ok=True,
                        status_code=status,
                        elapsed_s=elapsed_s,
                        payload=response.json(),
                    )

                if status in {429, 500, 502, 503, 504} and attempt < max_retries:
                    await asyncio.sleep(build_backoff_delay(attempt))
                    continue

                return FetchResult(
                    product_id=product_id,
                    ok=False,
                    status_code=status,
                    elapsed_s=elapsed_s,
                    error=f"http_{status}",
                )
            except (httpx.TimeoutException, httpx.TransportError) as exc:
                elapsed_s = time.perf_counter() - started
                last_error = exc.__class__.__name__
                if attempt < max_retries:
                    await asyncio.sleep(build_backoff_delay(attempt))
                    continue
                return FetchResult(
                    product_id=product_id,
                    ok=False,
                    status_code=None,
                    elapsed_s=elapsed_s,
                    error=last_error,
                )

        return FetchResult(
            product_id=product_id,
            ok=False,
            status_code=None,
            elapsed_s=0.0,
            error=last_error,
        )


def fetch_product_sync(
    product_id: int,
    client: httpx.Client,
    timeout_s: float,
    max_retries: int,
) -> FetchResult:
    """
    Sequential retry helper used by the failed-ID recheck pipeline.

    This intentionally avoids async orchestration so the screening step is easy
    to reason about and closer to the Coach's "slow but trustworthy" guidance.
    """
    last_error = "unknown_error"
    for attempt in range(max_retries + 1):
        started = time.perf_counter()
        try:
            response = client.get(API_URL.format(product_id=product_id), timeout=timeout_s)
            elapsed_s = time.perf_counter() - started
            status = response.status_code

            if status == 200:
                return FetchResult(
                    product_id=product_id,
                    ok=True,
                    status_code=status,
                    elapsed_s=elapsed_s,
                    payload=response.json(),
                )

            if status in {429, 500, 502, 503, 504} and attempt < max_retries:
                time.sleep(build_backoff_delay(attempt))
                continue

            return FetchResult(
                product_id=product_id,
                ok=False,
                status_code=status,
                elapsed_s=elapsed_s,
                error=f"http_{status}",
            )
        except (httpx.TimeoutException, httpx.TransportError) as exc:
            elapsed_s = time.perf_counter() - started
            last_error = exc.__class__.__name__
            if attempt < max_retries:
                time.sleep(build_backoff_delay(attempt))
                continue
            return FetchResult(
                product_id=product_id,
                ok=False,
                status_code=None,
                elapsed_s=elapsed_s,
                error=last_error,
            )

    return FetchResult(
        product_id=product_id,
        ok=False,
        status_code=None,
        elapsed_s=0.0,
        error=last_error,
    )
