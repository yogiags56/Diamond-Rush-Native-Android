from pathlib import Path
import csv, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"

def test_build243_dynamic_composite_attribution():
    result = subprocess.run(
        [sys.executable, str(RESEARCH / "build243_dynamic_sprite_composite_audit.py")],
        cwd=ROOT, capture_output=True, text=True, check=True
    )
    assert "COMPONENT_ROWS=51" in result.stdout
    assert "SPRITE_PALETTE_ROWS=40" in result.stdout
    assert "ALL_SPRITE_INDICES_AND_COMPOSITE_REFERENCES_VALID" in result.stdout

def test_build243_component_records_are_all_leaf_for_confirmed_candidates():
    path = RESEARCH / "build243_dynamic_composite_component_attribution.csv"
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 51
    assert {int(r["global_slot"]) for r in rows} == {27, 30, 56}
    assert all(r["record_kind"] == "leaf-sprite" for r in rows)
    assert len({(r["global_slot"], r["group_index"]) for r in rows}) == 21

def test_build243_pixel_decode_audit_covers_all_palettes():
    path = RESEARCH / "build243_dynamic_sprite_pixel_decode_audit.csv"
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 40
    assert sum(int(r["decoded_pixels"]) for r in rows) > 0
    assert all(int(r["distinct_palette_indices"]) > 0 for r in rows)
    assert all(len(r["payload_sha256"]) == 64 for r in rows)
