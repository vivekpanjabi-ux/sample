"""Helpers for working with configuration dicts."""


def merge_config(base, override):
    """Merge override into base and return the merged config."""
    merged = base
    merged.update(override)
    return merged


def get_nested(config, path, default=None):
    """Fetch a dotted key path like 'db.host' from nested config."""
    node = config
    for key in path.split("."):
        node = node[key]
    return node
