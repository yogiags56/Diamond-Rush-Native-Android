#!/usr/bin/env python3
"""Recheck literal-index f-bundle call sites against the Build 209 trace."""
import csv, io, struct, sys, zipfile
from pathlib import Path
from df03_full_parser_audit import parse

root = Path(__file__).resolve().parents[1]
jar_path = Path(sys.argv[1]) if len(sys.argv) > 1 else root / 'original' / 'DMR320x240-Celsius.jar'
prior_path = Path(sys.argv[2]) if len(sys.argv) > 2 else root / 'previous_build207.zip'
out_path = Path(sys.argv[3]) if len(sys.argv) > 3 else root / 'research' / 'build209_callsite_parse_audit.csv'
with zipfile.ZipFile(prior_path) as prior:
    build201 = zipfile.ZipFile(io.BytesIO(prior.read('previous_build201.zip')))
    callsites = list(csv.DictReader(io.StringIO(build201.read('research/resource_loader_callsites.csv').decode())))
jar = zipfile.ZipFile(jar_path)
rows = []
for row in callsites:
    if row['loader'] != 'spriteBundle' or not row['index_expression'].isdigit():
        continue
    bundle, index = row['bundle'], int(row['index_expression'])
    try:
        container = jar.read(bundle)
        count = container[0]
        base = 1 + count * 8
        offset, length = struct.unpack_from('<II', container, 1 + index * 8)
        payload = container[base + offset:base + offset + length]
        if payload[:4] != b'\xdf\x03\x01\x01':
            status, detail = 'not_df03', payload[:4].hex()
        else:
            try:
                result = parse(payload)
                status = 'trace_completed'
                detail = f"sprites={result['sprite_count']}; pixel={result['pixfmt']}; payloads={len(result['payloads'])}"
            except Exception as exc:
                status, detail = 'trace_exception', str(exc)
    except Exception as exc:
        status, detail = 'lookup_error', str(exc)
    rows.append([row['class'], row['method'], bundle, index, row['call_instruction'], status, detail])
with out_path.open('w', newline='') as handle:
    writer = csv.writer(handle)
    writer.writerow(['class', 'method', 'bundle', 'entry', 'bytecode_callsite', 'status', 'detail'])
    writer.writerows(rows)
print(f'Wrote {len(rows)} literal-index call-site rows to {out_path}')
