import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"

def rows(name):
    with (RESEARCH / name).open(newline="") as f:
        return list(csv.DictReader(f))

def test_all_five_target_methods_are_covered():
    data = rows("build219_method_operand_attribution_summary.csv")
    assert {r["method"] for r in data} == {"j", "W", "aa", "aj", "as"}

def test_store_offsets_are_unique_per_method():
    data = rows("build219_store_operand_provenance.csv")
    keys = [(r["method"], r["bytecode_offset"]) for r in data]
    assert len(keys) == len(set(keys))

def test_direct_attributions_only_use_known_map_planes():
    data = rows("build219_store_operand_provenance.csv")
    allowed = {"a:[[B", "b:[[B", "c:[[B", "a:[[I", "b:[[I"}
    for row in data:
        if row["attribution_status"] == "DIRECT_GETSTATIC_AALOAD_WINDOW":
            assert row["candidate_field"] in allowed

def test_unresolved_sites_are_not_silently_promoted():
    data = rows("build219_store_operand_provenance.csv")
    assert any(r["attribution_status"] == "UNRESOLVED_STACK_PROVENANCE" for r in data)
    assert all(r["candidate_field"] != "" for r in data)

def test_cell_binding_candidates_preserve_unknown_values():
    data = rows("build219_cell_object_binding_candidates.csv")
    assert data
    assert all(r["stored_value"] == "OPAQUE_RUNTIME_VALUE" for r in data)
    assert all(r["dispatch_domain_relation"] == "NOT_PROVEN" for r in data)

def test_dispatch_excerpt_documents_nested_branch_caveat():
    excerpt = (RESEARCH / "build219_j_state_dispatch_excerpt.txt").read_text()
    assert "not treated as exclusive linear ranges" in excerpt
    assert "tableswitch" in excerpt
