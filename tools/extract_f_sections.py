#!/usr/bin/env python3
"""Extract indexed payloads from Diamond Rush MIDP .f resource containers."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def split_resource(path: Path):
    data = path.read_bytes()
    if not data: raise ValueError("empty resource")
    count = data[0]
    table_end = 1 + count * 8
    if table_end > len(data): raise ValueError(f"truncated index: {path.name}")
    result = []
    for index in range(count):
        p = 1 + index * 8
        offset = int.from_bytes(data[p:p+4], "little")
        length = int.from_bytes(data[p+4:p+8], "little")
        start, end = table_end + offset, table_end + offset + length
        if end > len(data): raise ValueError(f"section {index} exceeds {path.name}")
        result.append((index, offset, length, data[start:end]))
    return result

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", type=Path, help="directory containing original .f files")
    ap.add_argument("output", type=Path, help="directory for extracted sections")
    args = ap.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    manifest = []
    for resource in sorted(args.input.glob("*.f")):
        for index, offset, length, payload in split_resource(resource):
            name = f"{resource.stem}_section_{index:02d}.bin"
            (args.output / name).write_bytes(payload)
            manifest.append({"resource": resource.name, "section": index,
                             "offset": offset, "length": length, "output": name})
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2)+"\n", encoding="utf-8")
    print(f"Extracted {len(manifest)} sections from {len(list(args.input.glob('*.f')))} resources.")
if __name__ == "__main__": main()
