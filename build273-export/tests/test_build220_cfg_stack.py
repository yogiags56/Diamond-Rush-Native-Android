import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "research"

def read(name):
    with (R / name).open(newline="") as f:
        return list(csv.DictReader(f))

def test_priority_methods_present():
    rows = read("build220_method_cfg_stack_summary.csv")
    assert {r["method"] for r in rows} == {"aj", "as", "W", "aa", "j"}

def test_cfg_edges_targets_are_valid_or_explicitly_marked():
    rows = read("build220_cfg_edges.csv")
    assert rows
    assert all(r["target_valid"] in ("True", "False") for r in rows)

def test_basic_blocks_have_positive_instruction_count():
    rows = read("build220_basic_blocks.csv")
    assert rows
    assert all(int(r["instruction_count"]) > 0 for r in rows)

def test_store_trace_preserves_unknowns():
    rows = read("build220_linear_stack_store_trace.csv")
    assert rows
    assert all(r["target_plane"] in {"a:[[B","b:[[B","c:[[B","a:[[I","b:[[I","UNKNOWN"} for r in rows)
    assert all(r["analysis_scope"] == "LINEAR_LOCAL_STACK_NO_BRANCH_MERGE" for r in rows)

def test_method_summary_store_counts_match_trace():
    summary = read("build220_method_cfg_stack_summary.csv")
    stores = read("build220_linear_stack_store_trace.csv")
    for row in summary:
        n = sum(1 for s in stores if s["method"] == row["method"])
        assert n == int(row["linear_stack_store_rows"])
