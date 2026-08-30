"""High-level client API."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Set, Tuple

from kev_integrator.cache import load_cache, save_cache
from kev_integrator.fetcher import fetch_kev_catalog
from kev_integrator.metrics import _metrics
from kev_integrator.models import KEVEntry
from kev_integrator.parser import parse_catalog, parse_csv_rows
from kev_integrator.state import get_new_entries as _get_new_entries

DEFAULT_CACHE_PATH = Path.home() / ".cache" / "cisa_kev" / "catalog.json"
DEFAULT_STATE_DB = Path.home() / ".cache" / "cisa_kev" / "state.db"


def get_kev_catalog(
    cache_path: Optional[Path] = None,
    state_db: Optional[Path] = None,
    force_refresh: bool = False,
) -> Tuple[list[KEVEntry], dict]:
    cache = cache_path or DEFAULT_CACHE_PATH
    if not force_refresh:
        cached = load_cache(cache)
        if cached is not None:
            _metrics.record_cache_hit()
            entries = [KEVEntry.from_raw(v) for v in cached["vulnerabilities"]]
            return entries, cached["_metadata"]
    _metrics.record_cache_miss()

    raw_entries, metadata = fetch_kev_catalog()
    if metadata["source"] == "cisa_csv":
        entries = parse_csv_rows(raw_entries)
    else:
        entries = parse_catalog({"vulnerabilities": raw_entries})

    save_cache(cache, entries, metadata)
    return entries, metadata


def get_kev_cve_ids(
    cache_path: Optional[Path] = None,
    force_refresh: bool = False,
) -> Set[str]:
    entries, _ = get_kev_catalog(cache_path=cache_path, force_refresh=force_refresh)
    return {e.cve_id for e in entries}


def get_new_entries(
    entries: list[KEVEntry],
    state_db: Optional[Path] = None,
) -> list[KEVEntry]:
    db = state_db or DEFAULT_STATE_DB
    return _get_new_entries(entries, db)
