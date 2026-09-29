"""Usage: python3 -m forensic.mdh.cli <input.ndjson> --source-id ID [--horizon SECONDS] [--chunk N]

Reads the file as raw bytes (fed in chunks of N bytes, default 4096), runs the
pipeline, validates the result, prints the canonical MDHRecord, and exits 1 if
validation fails."""
import argparse
import sys

from .pipeline import reconstruct
from .validate import validate


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("path")
    a.add_argument("--source-id", required=True)
    a.add_argument("--horizon", type=float, default=None)
    a.add_argument("--chunk", type=int, default=4096)
    args = a.parse_args(argv)
    raw = open(args.path, "rb").read()
    chunks = [raw[i:i + args.chunk] for i in range(0, len(raw), args.chunk)]
    rec, text = reconstruct(chunks, args.source_id, args.horizon)
    problems = validate(rec, raw)
    print(text)
    if problems:
        print("VALIDATION FAILED:", *problems, sep="\n  ", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
