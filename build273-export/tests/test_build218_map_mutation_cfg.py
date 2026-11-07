from pathlib import Path
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"

def rows(name):
    with (RESEARCH / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def test_map_related_method_inventory_has_66_methods():
    assert len(rows("build218_map_mutation_method_summary.csv")) == 66

def test_map_related_methods_contain_552_array_store_instructions():
    data = rows("build218_map_mutation_method_summary.csv")
    assert sum(int(x["store_instruction_count"]) for x in data) == 552

def test_candidate_plane_attribution_count_is_458():
    data = rows("build218_map_mutation_site_candidates.csv")
    assert sum(x["candidate_plane"] != "UNRESOLVED" for x in data) == 458

def test_unresolved_store_inventory_has_94_entries():
    data = rows("build218_unresolved_store_sites.csv")
    assert len(data) == 94

def test_cfg_contains_7143_branch_edges():
    data = rows("build218_map_mutation_cfg_edges.csv")
    assert len(data) == 7143

def test_all_cfg_branch_targets_resolve_to_instructions():
    edges = rows("build218_map_mutation_cfg_edges.csv")
    summary = rows("build218_map_mutation_method_summary.csv")
    source = (RESEARCH / "build214_bytecode" / "i_build214_full.javap.txt").read_text(errors="replace")
    # Confirm each target offset appears as an instruction in the named method.
    for method in {e["method"] for e in edges}:
        start = source.index(method)
        nxt = re.search(r"\n  (?:public|private|protected) ", source[start + len(method):])
        end = start + len(method) + nxt.start() if nxt else len(source)
        block = source[start:end]
        offsets = {int(x) for x in re.findall(r"(?m)^\s*(\d+):\s+[a-z][a-z0-9_]*", block)}
        for e in (x for x in edges if x["method"] == method):
            assert int(e["target_offset"]) in offsets

def test_highest_activity_method_is_aj():
    data = rows("build218_map_mutation_method_summary.csv")
    top = max(data, key=lambda x: int(x["store_instruction_count"]))
    assert top["method"] == "private void aj();"
    assert int(top["store_instruction_count"]) == 112

def test_plane_candidate_counts_sum_to_458():
    data = rows("build218_map_plane_candidate_summary.csv")
    assert sum(int(x["candidate_store_count"]) for x in data) == 458
