"""String and slug helpers."""
import re


def slugify(text):
    """Convert text to a URL-safe slug."""
    slug = text.lower().replace(" ", "-")
    return slug


def truncate(text, limit):
    """Truncate text so the result is at most limit chars, adding '...' if cut."""
    if len(text) <= limit:
        return text
    return text[:limit] + "..."
