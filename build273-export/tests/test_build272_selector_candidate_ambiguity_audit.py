import importlib.util
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "research" / "build272_selector_candidate_ambiguity_audit.py"
spec = importlib.util.spec_from_file_location("build272", P)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)


def sample():
    return [
        {"map_selector_bj":"3","row":"0","column":"0","branch_target":"1890","global_f_slot_candidate":"27","resource_path":"/gen3.f","record_index":"34","composite_group_candidate":"0"},
        {"map_selector_bj":"3","row":"0","column":"0","branch_target":"1890","global_f_slot_candidate":"30","resource_path":"/gen2.f","record_index":"23","composite_group_candidate":"1"},
        {"map_selector_bj":"4","row":"0","column":"1","branch_target":"1549","global_f_slot_candidate":"27","resource_path":"/gen3.f","record_index":"34","composite_group_candidate":"0"},
    ]


def test_selector_keeps_multiple_resources():
    selectors, _ = mod.audit(sample())
    assert selectors[0]["candidate_resource_count"] == 2
    assert selectors[0]["selection_status"].startswith("AMBIGUOUS")


def test_cell_keeps_multiple_resource_alternatives():
    _, cells = mod.audit(sample())
    assert cells[0]["candidate_resource_count"] == 2
    assert cells[0]["candidate_resource_group_pair_count"] == 2


def test_distinct_cells_are_not_merged():
    _, cells = mod.audit(sample())
    assert len(cells) == 2


def test_selector_branch_target_is_preserved():
    selectors, _ = mod.audit(sample())
    assert selectors[0]["branch_targets"] == "1890"


def test_no_runtime_binding_is_claimed():
    selectors, cells = mod.audit(sample())
    assert all("NOT_RUNTIME_SELECTION" in x["selection_status"] for x in selectors + cells)
