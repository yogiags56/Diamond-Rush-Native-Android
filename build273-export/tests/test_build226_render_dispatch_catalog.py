from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "android/src/main/kotlin/com/diamondrush/legacy/LegacyRenderDispatchCatalog.kt"
CSV = ROOT / "research/build226_main_dispatch_cfg_attribution.csv"
OVERLAY = ROOT / "research/build226_secondary_overlay_dispatch.csv"
SUPPLEMENTAL = ROOT / "research/build226_secondary_overlay_supplemental.csv"
TEXT = CATALOG.read_text()

def test_two_main_dispatch_domains_remain_distinct():
    assert "MAIN_PASS_BJ_SWITCH_OFFSET = 783" in TEXT
    assert "MAIN_PASS_BI_SWITCH_OFFSET = 2239" in TEXT
    assert "val bJCases" in TEXT and "val bICases" in TEXT
    assert "enum class" in TEXT

def test_main_switch_case_inventory_is_complete():
    rows = list(csv.DictReader(CSV.open()))
    bj = [r for r in rows if r["selector"] == "bJ"]
    bi = [r for r in rows if r["selector"] == "bI"]
    assert len(bj) == 35 and len(bi) == 50
    assert [int(r["raw_case_value"]) for r in bj] == list(range(3, 38))
    assert [int(r["raw_case_value"]) for r in bi] == list(range(50))

def test_secondary_overlay_numeric_routes():
    rows = list(csv.DictReader(OVERLAY.open()))
    routes = {r["raw_id_condition"]: r["resource_index"] for r in rows}
    assert routes["20..25"] == "3"
    assert routes["31"] == "15"
    assert routes["32"] == "16"
    assert routes["36"] == "20"
    assert routes["80..207"] == "42"

def test_supplemental_overlays_are_independent():
    rows = list(csv.DictReader(SUPPLEMENTAL.open()))
    assert [(r["condition"], r["resource_index"]) for r in rows] == [
        ("(packed_cell_value & 0xF0000000) >> 28 > 0", "13"),
        ("byte_plane_value == 54", "7"),
    ]
    assert "packedCellValue and -268435456" in TEXT
    assert "bytePlaneValue == 54" in TEXT

def test_generated_kotlin_source_has_real_line_breaks():
    assert r"\\n" not in TEXT
    assert "LegacyRawDispatchCase(3, 1890)," in TEXT
    assert "LegacyRawDispatchCase(49, 2452)," in TEXT

def test_high_metadata_nibble_uses_signed_shift_positive_test():
    assert "((packedCellValue and -268435456) shr 28) > 0" in TEXT

def test_overlay_dispatch_does_not_assign_semantic_names():
    assert "rawLowByte" in TEXT
    assert "gameObject" not in TEXT.lower()
