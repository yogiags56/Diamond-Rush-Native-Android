import csv
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JAR = ROOT / "original.jar"


def parse_archive(data):
    assert len(data) >= 2
    count = data[1]
    cursor = 2
    records = []
    for room_index in range(count):
        first = int.from_bytes(data[cursor:cursor + 2], "little")
        second = int.from_bytes(data[cursor + 2:cursor + 4], "little")
        cursor += 4
        cells = first * second
        assert cells > 0
        primary = data[cursor:cursor + cells]
        packed = data[cursor + 2 * cells:cursor + 3 * cells]
        assert len(primary) == cells and len(packed) == cells
        records.append((room_index, first, second, primary, packed))
        cursor += cells * 3
    assert cursor == len(data)
    return records


def test_all_original_archives_reassemble_without_losing_records():
    with zipfile.ZipFile(JAR) as jar:
        for name, expected in (("w0.bin", 14), ("w1.bin", 13), ("w2.bin", 14)):
            records = parse_archive(jar.read(name))
            assert len(records) == expected
            assert sum(len(r[3]) for r in records) == sum(r[1] * r[2] for r in records)


def test_build240_real_room_census_and_overlay_route_inventory():
    with zipfile.ZipFile(JAR) as jar:
        aggregate = Counter()
        dimensions = []
        for name in ("w0.bin", "w1.bin", "w2.bin"):
            for index, first, second, primary, packed in parse_archive(jar.read(name)):
                dimensions.append((name, index, first, second))
                for raw in packed:
                    low = raw
                    if 20 <= low <= 25:
                        aggregate["f3"] += 1
                    elif low == 31:
                        aggregate["f15"] += 1
                    elif low == 32:
                        aggregate["f16"] += 1
                    elif low == 36:
                        aggregate["f20"] += 1
                    elif low >= 80 and ((low - 80) & 0xff) < 128:
                        aggregate["f42_direct"] += 1
        assert len(dimensions) == 41
        assert aggregate["f3"] > 0
        # The current three original archives contain no low-byte selectors 31, 32, or 36.
        # Keep those dispatch routes covered by synthetic Kotlin fixtures, not fabricated room hits.
        assert aggregate["f15"] == 0
        assert aggregate["f16"] == 0
        assert aggregate["f20"] == 0
        assert aggregate["f42_direct"] > 0
