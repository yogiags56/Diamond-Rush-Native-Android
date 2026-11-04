#!/usr/bin/env python3
"""Corpus-level probe for the initial tables of extracted .f payload sections.

This is a structural probe, not a full sprite decoder. A section that does not
match this prefix is reported as unclassified, not corrupt: resource sections
can contain non-image data or use another entry point.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "reference" / "sections"


def u16(data: bytes, pos: int) -> int:
    if pos < 0 or pos + 2 > len(data):
        raise ValueError("u16 out of bounds")
    return data[pos] | data[pos + 1] << 8


def probe(data: bytes):
    if len(data) < 8:
        return {"status": "too_short"}
    count0 = u16(data, 6)
    end0 = 8 + count0 * 2
    if end0 + 2 > len(data):
        return {"status": "table0_out_of_bounds", "table0_count": count0}
    raw1 = u16(data, end0)
    count1 = raw1 if raw1 < 0x8000 else raw1 - 0x10000
    end1 = end0 + 2 + max(0, count1) * 4
    if end1 > len(data):
        return {"status": "table1_out_of_bounds", "table0_count": count0,
                "table1_count_signed": count1}
    return {"status": "prefix_valid", "table0_count": count0,
            "table1_count_signed": count1, "header_prefix_end": end1}


def main():
    manifest = json.loads((ROOT / "manifest.json").read_text())
    results = []
    for item in manifest:
        payload = (ROOT / item["output"]).read_bytes()
        result = probe(payload)
        results.append({"file": item["output"], "bytes": len(payload), **result})
    counts = {}
    for result in results:
        status = result["status"]
        counts[status] = counts.get(status, 0) + 1
    print(f"sections={len(results)}")
    for status, count in sorted(counts.items()):
        print(f"{status}={count}")
    print("\nUnclassified sections (not necessarily malformed):")
    for result in results:
        if result["status"] != "prefix_valid":
            print(f"{result['file']}: {result['status']} ({result['bytes']} bytes)")


if __name__ == "__main__":
    main()
