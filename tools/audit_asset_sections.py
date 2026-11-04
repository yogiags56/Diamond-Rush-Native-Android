#!/usr/bin/env python3
"""Audit extracted Diamond Rush .f sections against the original JAR."""
from __future__ import annotations
import argparse, hashlib, json, zipfile
from collections import Counter
from pathlib import Path


def parse_container(data: bytes, resource: str):
    if len(data) < 1:
        raise ValueError(f"{resource}: empty container")
    count = data[0]
    table_end = 1 + count * 8
    if table_end > len(data):
        raise ValueError(f"{resource}: truncated index table")
    records = []
    spans = []
    for index in range(count):
        p = 1 + index * 8
        offset = int.from_bytes(data[p:p+4], 'little')
        length = int.from_bytes(data[p+4:p+8], 'little')
        start, end = table_end + offset, table_end + offset + length
        if end > len(data):
            raise ValueError(f"{resource} section {index}: payload ends past EOF")
        if length == 0:
            raise ValueError(f"{resource} section {index}: empty payload")
        spans.append((start, end, index))
        records.append((index, offset, length, data[start:end]))
    ordered = sorted(spans)
    for previous, current in zip(ordered, ordered[1:]):
        if current[0] < previous[1]:
            raise ValueError(f"{resource}: sections {previous[2]} and {current[2]} overlap")
    return records


def audit(jar_path: Path, extracted_dir: Path):
    manifest_path = extracted_dir / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    checked = 0
    resources = Counter()
    total_bytes = 0
    with zipfile.ZipFile(jar_path) as jar:
        for resource, entries_iter in _group(manifest).items():
            try:
                original = jar.read(resource)
            except KeyError as exc:
                raise ValueError(f"{resource}: missing from source JAR") from exc
            parsed = parse_container(original, resource)
            entries = list(entries_iter)
            if len(entries) != len(parsed):
                raise ValueError(f"{resource}: manifest count differs from source")
            for entry, (idx, offset, length, payload) in zip(sorted(entries, key=lambda x: x['section']), parsed):
                if (entry['section'], entry['offset'], entry['length']) != (idx, offset, length):
                    raise ValueError(f"{resource} section {idx}: manifest index mismatch")
                extracted = (extracted_dir / entry['output']).read_bytes()
                if extracted != payload:
                    raise ValueError(f"{entry['output']}: differs from original JAR payload")
                checked += 1; resources[resource] += 1; total_bytes += length
    return checked, resources, total_bytes


def _group(entries):
    grouped = {}
    for entry in entries:
        grouped.setdefault(entry['resource'], []).append(entry)
    return grouped


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('jar', type=Path)
    ap.add_argument('sections', type=Path)
    args = ap.parse_args()
    count, resources, size = audit(args.jar, args.sections)
    print(f'PASS: {count} payloads match the original JAR byte-for-byte')
    print(f'PASS: {len(resources)} resources; {size:,} payload bytes audited')
    for name, n in sorted(resources.items()):
        print(f'  {name}: {n} sections')

if __name__ == '__main__':
    main()
