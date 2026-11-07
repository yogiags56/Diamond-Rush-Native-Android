import csv
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "research/build271_room_candidate_draw_plan.py"
spec = importlib.util.spec_from_file_location("build271", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_candidate_plan_has_expected_scope():
    rows = mod.build_rows()
    assert len(rows) == 4110
    assert len({(r["room_row"], r["room_column"]) for r in rows}) == 90
    assert len({(r["global_f_slot_candidate"], r["composite_group_candidate"]) for r in rows}) == 21


def test_candidate_destinations_are_anchor_plus_component_offsets():
    for row in mod.build_rows():
        assert int(row["candidate_destination_x"]) == int(row["anchor_screen_x"]) + int(row["offset_x_signed"])
        assert int(row["candidate_destination_y"]) == int(row["anchor_screen_y"]) + int(row["offset_y_signed"])


def test_no_candidate_is_misrepresented_as_runtime_selection():
    rows = mod.build_rows()
    assert {r["selection_status"] for r in rows} == {"CANDIDATE_ONLY_NO_RUNTIME_SELECTION_PROOF"}
    assert {r["transform_status"] for r in rows} == {"NOT_RESOLVED_FROM_THIS_JOIN"}


def test_component_records_are_leaf_sprite_records():
    rows = mod.build_rows()
    assert {r["record_kind"] for r in rows} == {"leaf-sprite"}
    assert all(r["sprite_or_nested_group_index"] != "" for r in rows)


def test_generated_csv_matches_reproducible_plan():
    path = ROOT / "research/build271_w0_room0_candidate_draw_plan.csv"
    with path.open(newline="", encoding="utf-8") as f:
        persisted = list(csv.DictReader(f))
    expected = [{k: str(v) for k, v in row.items()} for row in mod.build_rows()]
    assert len(persisted) == len(expected)
    assert persisted[0] == expected[0]
    assert persisted[-1] == expected[-1]
