import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "research/build273_selector_dataflow_trace.py"
spec = importlib.util.spec_from_file_location("build273", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_all_90_cells_and_six_selectors_are_traced():
    rows = mod.read_rows()
    result = mod.build(rows)
    assert sum(int(r["room_cell_count"]) for r in result) == 90
    assert [int(r["raw_bj_selector"]) for r in result] == [3, 4, 5, 6, 7, 8]
    assert all(r["status"] == "BYTECODE_DATAFLOW_TRACED_RUNTIME_VALUES_NOT_EXECUTED" for r in result)


def test_dynamic_helper_mapping_is_exact_for_relevant_selectors():
    result = {int(r["raw_bj_selector"]): r for r in mod.build(mod.read_rows())}
    assert result[4]["dynamic_helper_f_slot"] == "43"
    assert result[7]["dynamic_helper_f_slot"] == "56"
    assert result[8]["dynamic_helper_f_slot"] == "45"
    assert result[3]["dynamic_helper_status"] == "RESOLVES_TO_MINUS_ONE"
    assert result[6]["dynamic_helper_status"] == "RESOLVES_TO_MINUS_ONE"


def test_selector_7_preserves_two_distinct_f56_paths():
    result = {int(r["raw_bj_selector"]): r for r in mod.build(mod.read_rows())}
    assert result[7]["direct_f_slot_call"] == "56"
    assert "left-neighbor" in result[7]["direct_call_guard"]
    assert result[7]["dynamic_helper_f_slot"] == "56"


def test_resource_identity_and_runtime_values_are_not_invented():
    for row in mod.build(mod.read_rows()):
        assert row["resource_bundle_identity"] == "UNRESOLVED"
        assert row["runtime_predicate_values"] == "UNKNOWN"


def test_candidate_families_are_not_reused_as_exact_selector_results():
    result = {int(r["raw_bj_selector"]): r for r in mod.build(mod.read_rows())}
    for selector in (3, 4, 5, 6, 7, 8):
        assert result[selector]["dynamic_helper_f_slot"] not in {"27", "30"}
        assert result[selector]["direct_f_slot_call"] != "27"
        assert result[selector]["direct_f_slot_call"] != "30"
