import csv
import importlib.util
import struct
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JAR = ROOT / "original.jar"
PARSER_PATH = ROOT / "research/df03_full_parser_audit.py"

spec = importlib.util.spec_from_file_location("df03_parser_build234", PARSER_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def make_minimal_payload():
    # Fixed six-byte header, one 2x1 sprite, no opaque pre-palette tables.
    return (
        bytes.fromhex("df0301010101") +
        struct.pack("<h", 1) + bytes([2, 1]) +
        struct.pack("<h", 0) +  # four-byte table count
        struct.pack("<h", 0) +  # metadata row count
        struct.pack("<h", 0) +  # five-byte table count
        struct.pack("<h", 0) +  # byte/short table count
        struct.pack("<h", 21781) + bytes([1, 2]) +
        struct.pack("<HH", 0x8000, 0x7c00) +
        struct.pack("<h", 5632) +
        struct.pack("<h", 1) + bytes([0x10])
    )

def test_minimal_payload_cursor_and_palette_fields():
    parsed = module.parse(make_minimal_payload())
    assert parsed["sprite_count"] == 1
    assert parsed["dims"] == bytes([2, 1])
    assert parsed["palfmt"] == 21781
    assert parsed["pixfmt"] == 5632
    assert parsed["palettes"] == [bytes([0x00, 0x80, 0x00, 0x7c])]
    assert parsed["lengths"] == [1]
    assert parsed["payloads"] == [bytes([0x10])]
    assert parsed["trailing"] == b""

def test_bundle_directory_reader_uses_little_endian_32_bit_offset_and_length():
    payload = make_minimal_payload()
    bundle = bytes([1]) + struct.pack("<II", 0, len(payload)) + payload
    count = bundle[0]
    base = 1 + count * 8
    off, length = struct.unpack_from("<II", bundle, 1)
    assert bundle[base + off:base + off + length] == payload

def test_all_original_df03_bundle_entries_parse_without_failure():
    rows = list(csv.DictReader((ROOT / "research/build234_corrected_resource_inventory.csv").open(newline="")))
    failures = list(csv.DictReader((ROOT / "research/build234_corrected_resource_inventory_failures.csv").open(newline="")))
    assert len(rows) == 94
    assert failures == []
    assert sum(int(row["sprite_count"]) for row in rows) == 1372
    assert all(int(row["trailing_bytes"]) == 0 for row in rows)

def test_all_ten_build233_static_mappings_now_parse():
    bindings = list(csv.DictReader((ROOT / "research/build233_bundle_to_global_sprite_slots.csv").open(newline="")))
    with zipfile.ZipFile(JAR) as archive:
        for binding in bindings:
            bundle = archive.read(binding["bundle_path"].lstrip("/"))
            entry_count = bundle[0]
            base = 1 + entry_count * 8
            index = int(binding["bundle_entry_index"])
            offset, length = struct.unpack_from("<II", bundle, 1 + index * 8)
            payload = bundle[base + offset:base + offset + length]
            parsed = module.parse(payload)
            assert parsed["sprite_count"] > 0
            assert parsed["pixfmt"] in (5632, 10225, 1024)
            assert len(parsed["payloads"]) == parsed["sprite_count"]

def test_four_byte_tables_use_shift_left_two_bytecode_semantics():
    source = (ROOT / "research/build213_bytecode/f_class_full.javap.txt").read_text(errors="replace")
    assert "iload         4" in source
    assert "iconst_2" in source and "ishl" in source
    parser = PARSER_PATH.read_text()
    assert "table2_count*4" in parser
    assert "table3_count*4" in parser


def test_mapped_slots_expand_to_87_sprite_records():
    rows = list(csv.DictReader((ROOT / "research/build234_mapped_sprite_directory.csv").open(newline="")))
    assert len(rows) == 87
    assert all(int(row["width"]) > 0 and int(row["height"]) > 0 for row in rows)
    assert {int(row["pixel_format"]) for row in rows} == {5632}


def test_all_bundle_directories_are_in_bounds():
    total_entries = 0
    df03_entries = 0
    with zipfile.ZipFile(JAR) as archive:
        for name in archive.namelist():
            if name.endswith(".f"):
                entries = module.read_bundle_entries(archive.read(name))
                total_entries += len(entries)
                df03_entries += sum(entry[3][:4] == module.MAGIC for entry in entries)
    assert total_entries == 121
    assert df03_entries == 94
