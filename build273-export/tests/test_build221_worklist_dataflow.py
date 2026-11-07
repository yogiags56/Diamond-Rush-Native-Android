import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"research"
def read(n):
    with (R/n).open(newline="") as f:return list(csv.DictReader(f))
def test_five_priority_methods_have_dataflow_summaries():
    rows=read("build221_method_dataflow_summary.csv")
    assert {r["method"] for r in rows}=={"aj","as","W","aa","j"}
def test_store_sites_unique_by_method_and_offset():
    rows=read("build221_worklist_stack_store_attribution.csv")
    keys=[(r["method"],r["offset"]) for r in rows]
    assert len(keys)==len(set(keys))
def test_unknowns_are_preserved():
    rows=read("build221_worklist_stack_store_attribution.csv")
    assert rows and all(r["target_plane"] in {"a:[[B","b:[[B","c:[[B","a:[[I","b:[[I","UNKNOWN"} for r in rows)
def test_every_store_keeps_dispatch_relation_unproven():
    rows=read("build221_dispatch_value_link_audit.csv")
    assert rows and all(r["dispatch_domain_relation"]=="NOT_PROVEN_IN_THIS_MILESTONE" for r in rows)
def test_worklist_states_are_offset_indexed():
    rows=read("build221_instruction_entry_stack_states.csv")
    assert rows and all(int(r["offset"])>=0 for r in rows)
def test_method_store_totals_match_site_table():
    summaries=read("build221_method_dataflow_summary.csv")
    stores=read("build221_worklist_stack_store_attribution.csv")
    for r in summaries:
        assert int(r["array_store_sites"])==sum(1 for s in stores if s["method"]==r["method"])
