#!/usr/bin/env python3
"""Conservative probe for the class-f decoder's palette/header stage.

This does not decode pixels. It mirrors the verified bytecode reads up to the
palette and image-offset table, and rejects impossible cumulative offsets.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse, json

class FormatError(ValueError):
    pass

class Reader:
    def __init__(self, data): self.data, self.pos = data, 0
    def take(self, n, label):
        if n < 0 or self.pos + n > len(self.data):
            raise FormatError(f'{label}: need {n} bytes at {self.pos}; payload={len(self.data)}')
        out = self.data[self.pos:self.pos+n]; self.pos += n; return out
    def u8(self, label): return self.take(1, label)[0]
    def u16(self, label):
        b = self.take(2, label); return b[0] | (b[1] << 8)
    def s16(self, label):
        v = self.u16(label); return v - 65536 if v & 0x8000 else v

@dataclass
class Probe:
    payload_size: int
    image_count: int
    table1_count: int
    table2_count: int
    table3_count: int
    table4_count: int
    palette_format: int | None
    palette_groups: int
    palette_colors: int
    palette_entry_bytes: int | None
    alpha_or_mode_word: int | None
    image_offsets: list
    metadata_end: int
    status: str

def probe(data: bytes) -> Probe:
    r = Reader(data)
    r.take(6, 'fixed prefix')
    image_count = r.s16('image table count')
    if image_count < 0: raise FormatError('negative image table count')
    r.take(image_count * 2, 'image dimension table')
    n1 = r.s16('table1 count')
    if n1 < 0: raise FormatError('negative table1 count')
    r.take(n1 * 4, 'table1 records')
    n2 = r.s16('table2 count')
    if n2 < 0: raise FormatError('negative table2 count')
    r.take(n2 * 4, 'table2 records')
    r.take(n2 * 4, 'table2 auxiliary data')
    n3 = r.s16('table3 count')
    if n3 < 0: raise FormatError('negative table3 count')
    r.take(n3 * 5, 'table3 records')
    n4 = r.s16('table4 count')
    if n4 < 0: raise FormatError('negative table4 count')
    r.take(n4 * 4, 'table4 records')

    fmt = groups = colors = entry_bytes = alpha = None
    offsets = []
    status = 'prefix-only'
    if image_count:
        fmt = r.s16('palette format')
        groups = r.u8('palette group count')
        colors = r.u8('palette color count')
        # Exact switch values in class f.a(byte[],int), interpreted signed-short.
        entry_bytes = { -30584: 4, 17476: 2, 21781: 2, 25861: 2 }.get(fmt)
        if entry_bytes is None:
            raise FormatError(f'unsupported palette format {fmt} (0x{fmt & 0xffff:04x})')
        r.take(groups * colors * entry_bytes, 'palette entries')
        alpha = r.s16('palette alpha/mode word')
        running = 0
        for i in range(image_count):
            size = r.s16(f'image offset delta {i}')
            if size < 0: raise FormatError(f'negative image offset delta at {i}')
            running += size
            if running > len(data):
                raise FormatError(f'image offset table cumulative size {running} exceeds payload {len(data)}')
            offsets.append(running)
        status = 'image-offset-table-bounded'
    return Probe(len(data), image_count, n1, n2, n3, n4, fmt, groups or 0,
                 colors or 0, entry_bytes, alpha, offsets, r.pos, status)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('payload', type=Path); ap.add_argument('--json', action='store_true'); a = ap.parse_args()
    try:
        result = asdict(probe(a.payload.read_bytes()))
        print(json.dumps(result, indent=2) if a.json else '\n'.join(f'{k}={v}' for k,v in result.items()))
    except (OSError, FormatError) as e:
        raise SystemExit(f'UNRESOLVED/INVALID: {e}')
if __name__ == '__main__': main()
