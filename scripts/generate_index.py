#!/usr/bin/env python3
"""Generate deterministic community plugin registry index.json (+ gzip).

Reads only plugins/*.json (top-level). Does not enumerate examples/ or templates/.

Usage:
  python scripts/generate_index.py --plugins-dir plugins --output-dir generated
"""

from __future__ import annotations

import argparse
import gzip
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

MINIMUM_CLIENT_VERSION = "1.0.0"
SCHEMA_VERSION = 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate community plugin registry index"
    )
    parser.add_argument("--plugins-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--generated-at",
        default=None,
        help="Optional fixed generatedAtUtc (ISO-8601). Default: now (UTC).",
    )
    args = parser.parse_args()

    plugins_dir = Path(args.plugins_dir)
    output_dir = Path(args.output_dir)

    if not plugins_dir.is_dir():
        print(
            f"error: plugins directory not found: {plugins_dir}",
            file=sys.stderr,
        )
        return 2

    entries: list[dict] = []

    for path in sorted(plugins_dir.glob("*.json"), key=lambda p: p.name):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as ex:
            print(f"error: {path.name}: {ex}", file=sys.stderr)
            return 1

        if not isinstance(data, dict):
            print(
                f"error: {path.name}: expected JSON object",
                file=sys.stderr,
            )
            return 1

        entries.append(data)

    entries.sort(key=lambda entry: str(entry.get("id") or ""))

    generated_at = (
        args.generated_at
        or datetime.now(timezone.utc).isoformat()
    )

    index = {
        "schemaVersion": SCHEMA_VERSION,
        "generatedAtUtc": generated_at,
        "minimumClientVersion": MINIMUM_CLIENT_VERSION,
        "plugins": entries,
    }

    output_dir.mkdir(parents=True, exist_ok=True)

    index_path = output_dir / "index.json"
    gzip_path = output_dir / "index.json.gz"

    text = json.dumps(index, indent=2, ensure_ascii=False) + "\n"
    index_path.write_text(text, encoding="utf-8")

    # Produce reproducible gzip output. gzip.open() stores the current
    # timestamp in the gzip header, which causes CI comparisons to fail.
    with gzip_path.open("wb") as output:
        with gzip.GzipFile(
            filename="",
            mode="wb",
            fileobj=output,
            mtime=0,
        ) as gz:
            gz.write(text.encode("utf-8"))

    print(f"::notice::Wrote {index_path} ({len(entries)} plugin(s))")
    print(
        f"::notice::Wrote {gzip_path} "
        f"({gzip_path.stat().st_size} bytes gzip)"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())