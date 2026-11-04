#!/usr/bin/env python3
"""Print safe structural hints for one extracted Diamond Rush sprite payload.

This is intentionally an inspector, not a decoder: the complete header schema
and resource-specific interpretation are still under reverse engineering.
"""
import argparse
from pathlib import Path


def u16le(data: bytes, pos: int) -> int:
    if pos < 0 or pos + 2 > len(data):
        raise ValueError(f"u16 at {pos} exceeds payload ({len(data)} bytes)")
    return data[pos] | (data[pos + 1] << 8)


def inspect(path: Path) -> None:
    data = path.read_bytes()
    print(f"payload={path} bytes={len(data)}")
    if len(data) < 8:
        print("status=too_short_for_initial_decoder_header")
        return
    print("initial_cursor_skip=6")
    count = u16le(data, 6)
    print(f"table0_count_u16le_at_6={count} (signed-short interpretation={count if count < 32768 else count-65536})")
    end = 8 + count * 2
    print(f"table0_range=[8,{end}) within_payload={end <= len(data)}")
    if end > len(data):
        print("status=header_incomplete; no further fields interpreted")
        return
    # The original parser reads the next 16-bit count immediately after table 0.
    if end + 2 <= len(data):
        count1 = u16le(data, end)
        signed1 = count1 if count1 < 32768 else count1 - 65536
        print(f"table1_count_u16le_at_{end}={count1} (signed-short={signed1})")
        end1 = end + 2 + max(0, signed1) * 4
        print(f"table1_records_4byte_range=[{end+2},{end1}) within_payload={end1 <= len(data)}")
    else:
        print("status=truncated_before_second_count")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("payload", type=Path)
    inspect(parser.parse_args().payload)
