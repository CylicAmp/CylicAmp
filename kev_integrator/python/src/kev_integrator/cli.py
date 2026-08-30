"""Command-line interface."""

import argparse
import json
import logging
import sys
from pathlib import Path

from kev_integrator.client import get_kev_catalog, get_new_entries
from kev_integrator.metrics import _metrics


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(description="CISA KEV Catalog Sync")
    parser.add_argument("--refresh", action="store_true", help="Force refresh")
    parser.add_argument("--new-only", action="store_true", help="Only new entries")
    parser.add_argument("--output", type=Path, help="Output JSON file")
    parser.add_argument("--metrics", action="store_true", help="Print metrics")
    args = parser.parse_args()

    entries, meta = get_kev_catalog(force_refresh=args.refresh)

    if args.new_only:
        entries = get_new_entries(entries)

    result = {
        "metadata": meta,
        "count": len(entries),
        "entries": [e.to_dict() for e in entries],
    }

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
    else:
        print(json.dumps(result, indent=2, default=str))

    if args.metrics:
        print(json.dumps(_metrics.to_dict(), indent=2), file=sys.stderr)


if __name__ == "__main__":
    main()
