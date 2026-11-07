import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_static_bundle_slot_map_has_ten_direct_assignments():
    path = ROOT / "research/build233_bundle_to_global_sprite_slots.csv"
    rows = list(csv.DictReader(path.open(newline="")))
    assert len(rows) == 10
    assert len({int(row["global_f_slot"]) for row in rows}) == 10

def test_known_mmv_slots_and_entry_indices():
    path = ROOT / "research/build233_bundle_to_global_sprite_slots.csv"
    rows = list(csv.DictReader(path.open(newline="")))
    pairs = {(int(r["global_f_slot"]), int(r["bundle_entry_index"])) for r in rows if r["bundle_path"] == "/mmv.f"}
    assert pairs == {(10, 0), (46, 5), (55, 4), (54, 1), (53, 2), (52, 3)}

def test_cm_ms_and_ui_slot_bindings():
    path = ROOT / "research/build233_bundle_to_global_sprite_slots.csv"
    rows = list(csv.DictReader(path.open(newline="")))
    pairs = {(int(r["global_f_slot"]), r["bundle_path"], int(r["bundle_entry_index"])) for r in rows}
    assert (59, "/cm.f", 2) in pairs
    assert (9, "/cm.f", 7) in pairs
    assert (17, "/ms.f", 0) in pairs
    assert (18, "/ui.f", 3) in pairs

def test_kotlin_catalog_matches_csv_and_preserves_numeric_ids():
    source = (ROOT / "android/src/main/kotlin/com/diamondrush/legacy/LegacyBundleSpriteSlotCatalog.kt").read_text()
    assert source.count("LegacyBundleSpriteSlotBinding(") == 11  # declaration plus ten rows
    assert '"/mmv.f", 0, 145' in source
    assert '"/ui.f", 3, 314' in source
    assert "bindingForSlot" in source

def test_dynamic_slot_assignments_are_not_misrepresented_as_static_bindings():
    path = ROOT / "research/build233_dynamic_sprite_slot_assignments.csv"
    rows = list(csv.DictReader(path.open(newline="")))
    assert len(rows) == 4
    assert any(r["global_slot"] == "local variable 6" for r in rows)
    assert any(r["status"].startswith("dynamic_stream_payload") for r in rows)

def test_original_loader_uses_eight_byte_directory_records():
    source = (ROOT / "research/build214_bytecode/i_build214_full.javap.txt").read_text(errors="replace")
    method = source[source.find("public static byte[] a(java.lang.String, int);"):]
    method = method[:2000]
    assert "iload_1" in method and "iconst_3" in method and "ishl" in method
    assert "iconst_4" in method and "InputStream.skip" in method


def test_directory_integer_helper_is_unsigned_little_endian_32_bit():
    source = (ROOT / "research/build214_bytecode/i_build214_full.javap.txt").read_text(errors="replace")
    start = source.find("public static int b(byte[], int);")
    method = source[start:start + 1200]
    assert "baload" in method and "iand" in method
    assert "bipush        8" in method and "bipush        16" in method and "bipush        24" in method
    assert "ireturn" in method
