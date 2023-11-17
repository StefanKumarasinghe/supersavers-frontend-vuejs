import time
CACHE = {}
CACHE_DURATION = 3600  # seconds or 5 minutes
def is_cache_valid(query: str) -> bool:
    """Check if cache for a query is still valid."""
    return query in CACHE and time.time() - CACHE[query]['timestamp'] < CACHE_DURATION