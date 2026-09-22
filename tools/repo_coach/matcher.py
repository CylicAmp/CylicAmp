"""Fixed content matching for the GitHub coaching bot.

Two fixes:

1. `"data" or "assets"` returned "data" and left "assets" unreachable --
   Python's `or` yields its first truthy operand. Directories are now a
   list, so both are real.

2. Substring matching flagged ordinary text: "auth" matched "author",
   "token" matched "tokenize", "secret" matched "SECRETARY".

   Plain \\b is not right either, because \\b treats "_" as a word
   character, so \\bapi_key\\b would MISS "my_api_key" -- a real
   credential name. The boundary used here is (?<![A-Za-z0-9]) and
   (?![A-Za-z0-9]): letters and digits break a match, underscores and
   punctuation do not. That keeps "author" clean while still catching
   "my_api_key".
"""

import re
from typing import Dict, List, Pattern

SENSITIVE_PATTERNS = [
    "BEGIN PRIVATE KEY", "BEGIN RSA PRIVATE KEY", "password", "secret",
    "api_key", "private_key", "credential", "token", "auth", "hdf5",
    "jinja2", "exploit",
]

GUIDELINE_DIRECTORIES: Dict[str, List[str]] = {
    "CODE":          ["src"],
    "DOCUMENTATION": ["docs"],
    "CONFIGURATION": ["."],
    "TESTS":         ["tests"],
    "DATA":          ["data", "assets"],   # was: "data" or "assets"
}

def primary_directory(content_type: str) -> str:
    """First configured directory for a content type."""
    dirs = GUIDELINE_DIRECTORIES.get(content_type) or GUIDELINE_DIRECTORIES["DOCUMENTATION"]
    return dirs[0]

def _compile(pattern: str) -> Pattern[str]:
    """Identifier-aware boundary: alphanumerics break a match, _ does not."""
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(pattern) + r"(?![A-Za-z0-9])",
                      re.IGNORECASE)

_COMPILED = {p: _compile(p) for p in SENSITIVE_PATTERNS}

def find_sensitive(text: str) -> List[str]:
    """Patterns genuinely present in text, as whole identifier tokens."""
    return [p for p, rx in _COMPILED.items() if rx.search(text)]

def is_sensitive(text: str) -> bool:
    return bool(find_sensitive(text))
