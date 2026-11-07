import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_access_inventory_has_expected_schema_and_entries():
    path = ROOT / "research/build232_sprite_resource_array_accesses.csv"
    rows = list(csv.DictReader(path.open(newline="")))
    assert len(rows) == 248
    assert {"method", "bytecode_offset", "array_index_constant", "access_kind"} <= set(rows[0])

def test_render_method_consumer_indices_include_known_overlay_resources():
    path = ROOT / "research/build232_sprite_resource_array_accesses.csv"
    rows = list(csv.DictReader(path.open(newline="")))
    d_rows = [r for r in rows if r["method"] == "private void D();" and r["array_index_constant"]]
    indices = {int(r["array_index_constant"]) for r in d_rows}
    assert {3, 7, 13, 15, 16, 20, 42} <= indices

def test_overlay_indices_remain_numeric_and_not_gameplay_labels():
    source = (ROOT / "android/src/main/kotlin/com/diamondrush/legacy/LegacySpriteResourceConsumerCatalog.kt").read_text()
    assert "setof(3, 7, 13, 15, 16, 20, 42)" in source.lower()
    assert "enemy" not in source.lower()

def test_resource_array_is_initialized_with_61_slots():
    source = (ROOT / "research/build214_bytecode/i_build214_full.javap.txt").read_text(errors="replace")
    assert "bipush        61" in source
    assert "anewarray     #136                // class f" in source
