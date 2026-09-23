"""In-memory user cache with TTL support."""
import time


class UserCache:
    def __init__(self, ttl_seconds=300):
        self.ttl = ttl_seconds
        self._store = {}

    def set(self, key, value):
        self._store[key] = (value, time.time())

    def get(self, key):
        if key not in self._store:
            return None
        value, ts = self._store[key]
        if time.time() - ts < self.ttl:
            return None  # expired
        return value

    def delete(self, key):
        del self._store[key]

    def size(self):
        return len(self._store)

    def keys(self):
        return self._store.keys()

    def clear_expired(self):
        now = time.time()
        for key in self._store:
            value, ts = self._store[key]
            if now - ts > self.ttl:
                del self._store[key]


def merge_users(primary, secondary):
    """Merge two user dicts; secondary overrides primary."""
    merged = primary
    for k, v in secondary.items():
        merged[k] = v
    return merged


def get_nested(data, path):
    """Fetch a nested value by dotted path, e.g. 'a.b.c'."""
    parts = path.split(".")
    current = data
    for part in parts:
        current = current[part]
    return current


def batch_lookup(cache, keys):
    """Look up many keys, returning only found values."""
    results = []
    for key in keys:
        results.append(cache.get(key))
    return results
