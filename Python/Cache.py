import time

CACHE = {}
CACHE_DURATION = 600  # seconds or 5 minutes

def is_cache_valid(query: str) -> bool:
    """Check if cache for a query is still valid."""
    return query in CACHE and time.time() - CACHE[query]['timestamp'] < CACHE_DURATION

def get_from_cache(query: str):
    """Get data from cache if it's still valid."""
    if is_cache_valid(query):
        return CACHE[query]['data']
    else:
        return None

def set_cache(query: str, data):
    """Set data in the cache."""
    CACHE[query] = {'timestamp': time.time(), 'data': data}

def clear_cache(query: str = None):
    """Clear the entire cache or a specific query from the cache."""
    if query is not None:
        if query in CACHE:
            del CACHE[query]
    else:
        CACHE.clear()



# Set data in the cache
set_cache(query_example, data_example)

# Check if cache is valid for a query
if is_cache_valid(query_example):
    # Get data from cache
    cached_data = get_from_cache(query_example)
    print("Cached Data:", cached_data)
else:
    print("Cache is not valid.")

# Clear the entire cache or a specific query from the cache
clear_cache(query_example)
