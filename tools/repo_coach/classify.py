"""Content-type classification for the GitHub coaching bot.

The original used ordered substring regexes, which failed two ways:

  DATA was `{|\\"|:|\\[|\\]|,` -- any brace, quote, colon, bracket or
  comma. `for i in range(3):` and `x, y = 1, 2` both classified as data.

  Order was wrong and the markers were substrings. CODE was tested
  before TESTS, so `def test_foo()` matched `def ` and came back CODE.
  `test ` matched "latest version"; `it\\(` matched "exit(".

This parses instead of pattern-matching. Each check either succeeds
decisively or declines, and they run most-specific first, because a
test file IS code and a CSV IS a valid Python tuple expression.
"""

import ast
import csv
import configparser
import io
import json
import re
from enum import Enum
from typing import Optional, Tuple


class ContentType(Enum):
    CODE = "CODE"
    DOCUMENTATION = "DOCUMENTATION"
    CONFIGURATION = "CONFIGURATION"
    TESTS = "TESTS"
    DATA = "DATA"


# --------------------------------------------------------------------
# decisive parsers
# --------------------------------------------------------------------

def _is_json(text: str) -> bool:
    text = text.strip()
    if not text or text[0] not in "{[":
        return False
    try:
        json.loads(text)
        return True
    except (json.JSONDecodeError, ValueError):
        return False


def _is_csv(text: str) -> bool:
    """Two or more rows with a constant field count above one."""
    lines = [ln for ln in text.strip().splitlines() if ln.strip()]
    if len(lines) < 2:
        return False
    try:
        rows = list(csv.reader(io.StringIO("\n".join(lines))))
    except csv.Error:
        return False
    widths = {len(r) for r in rows}
    return len(widths) == 1 and widths.pop() > 1


def _is_ini(text: str) -> bool:
    if not re.match(r"\s*\[[^\]\n]+\]\s*$", text.splitlines()[0] if text.strip() else ""):
        return False
    try:
        configparser.ConfigParser().read_string(text)
        return True
    except configparser.Error:
        return False


def _python_tree(text: str) -> Optional[ast.Module]:
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return None
    return tree if tree.body else None      # all-comments is not code


# `=>` is punctuation, so \b cannot anchor it -- it is matched literally.
_JS = re.compile(r"\b(function|const|let|var|require|module\.exports|export)\b|=>")
_MD = re.compile(r"^\s{0,3}(#{1,6}\s+\S|[-*+]\s+\S|\d+\.\s+\S|>\s|```)", re.M)


# --------------------------------------------------------------------
# test detection
# --------------------------------------------------------------------

_JS_TEST = re.compile(r"\b(describe|it|test|expect|beforeEach|afterEach)\s*\(")


def _python_is_test(tree: ast.Module, text: str) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("test_") or node.name == "test":
                return True
        if isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
            return True
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in getattr(node, "names", [])]
            mod = getattr(node, "module", None)
            for n in names + ([mod] if mod else []):
                if n and n.split(".")[0] in {"pytest", "unittest", "nose", "hypothesis"}:
                    return True
    return False


# --------------------------------------------------------------------
# classifier
# --------------------------------------------------------------------

def classify(text: str) -> Tuple[ContentType, str]:
    """Most-specific first: a test is code, and a CSV row is valid Python."""
    if not text or not text.strip():
        return ContentType.DOCUMENTATION, "empty content"

    if _is_json(text):
        return ContentType.DATA, "parses as JSON"
    if _is_csv(text):
        return ContentType.DATA, "parses as CSV with a constant field count"
    if _is_ini(text):
        return ContentType.CONFIGURATION, "parses as INI/config"

    tree = _python_tree(text)
    if tree is not None:
        if _python_is_test(tree, text):
            return ContentType.TESTS, "Python AST with test functions or a test framework import"
        return ContentType.CODE, "parses as Python with executable statements"

    if _JS.search(text):
        if _JS_TEST.search(text):
            return ContentType.TESTS, "JavaScript with test-framework calls"
        return ContentType.CODE, "JavaScript syntax"

    if _MD.search(text):
        return ContentType.DOCUMENTATION, "Markdown structure"

    return ContentType.DOCUMENTATION, "no decisive signal; defaulting to documentation"
