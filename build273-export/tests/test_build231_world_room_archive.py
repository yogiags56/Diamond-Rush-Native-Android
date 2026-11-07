from pathlib import Path
import struct
import zipfile

ROOT = Path(__file__).resolve().parents[1]
JAR = ROOT / "original/DMR320x240-Celsius.jar"


def inspect_archive(data):
    assert len(data) >= 2
    declared = data[1]
    cursor = 2
    records = []
    for room_index in range(declared):
        assert len(data) - cursor >= 4
        first, second = struct.unpack_from("<HH", data, cursor)
        assert first > 0 and second > 0
        payload_offset = cursor + 4
        payload_size = first * second * 3
        assert payload_size <= len(data) - payload_offset
        records.append((first, second, cursor, payload_offset, payload_size))
        cursor = payload_offset + payload_size
    return records, cursor


def test_original_room_archives_have_complete_declared_record_sets():
    expected_counts = {"w0.bin": 14, "w1.bin": 13, "w2.bin": 14}
    with zipfile.ZipFile(JAR) as jar:
        for name, expected in expected_counts.items():
            data = jar.read(name)
            records, consumed = inspect_archive(data)
            assert data[0] == 1  # retained opaque prefix byte; no semantics inferred
            assert len(records) == expected == data[1]
            assert consumed == len(data)


def test_archive_decoder_keeps_prefix_opaque_and_reuses_record_decoder():
    source = (ROOT / "android/src/main/kotlin/com/diamondrush/legacy/LegacyWorldRoomArchiveDecoder.kt").read_text()
    assert "opaquePrefixByte" in source
    assert "LegacyRoomPayloadDecoder.decodeSelectedRecord" in source
    assert "recordsOnly = bytes.copyOfRange(2, indexed.consumedBytes)" in source
    assert "trailingBytes" in source


def test_real_room_archive_dimensions_are_inventoried_without_semantic_labels():
    expected = {
        "w0.bin": [(26, 21), (27, 24), (27, 26), (40, 23), (51, 24), (30, 75), (26, 45), (44, 29), (35, 14), (50, 30), (50, 31), (46, 31), (46, 31), (68, 11)],
        "w1.bin": [(45, 24), (40, 24), (33, 30), (43, 30), (45, 33), (43, 33), (36, 43), (53, 27), (34, 32), (35, 25), (37, 24), (60, 20), (23, 60)],
        "w2.bin": [(60, 26), (39, 35), (35, 42), (38, 38), (46, 27), (49, 28), (55, 30), (51, 20), (51, 37), (104, 17), (35, 25), (45, 28), (35, 32), (35, 26)],
    }
    with zipfile.ZipFile(JAR) as jar:
        for name, dimensions in expected.items():
            records, _ = inspect_archive(jar.read(name))
            assert [(r[0], r[1]) for r in records] == dimensions
