import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"research"
def read(n):
    with (R/n).open(newline="") as f:return list(csv.DictReader(f))
def test_exception_table_inventory_and_valid_targets():
    rows=read("build222_exception_handler_edges.csv")
    assert rows and all(r["range_order_valid"]=="True" for r in rows)
    assert all(r["handler_valid"]=="True" for r in rows)
def test_both_dispatch_domains_remain_separate():
    rows=read("build222_render_dispatch_cases.csv")
    p1=[r for r in rows if r["dispatch_pass"]=="PASS_1"]
    p2=[r for r in rows if r["dispatch_pass"]=="PASS_2"]
    assert len(p1)==35 and len(p2)==50
    assert {r["dispatch_field"] for r in p1}=={"bJ:I"}
    assert {r["dispatch_field"] for r in p2}=={"bI:I"}
def test_dispatch_targets_are_valid():
    rows=read("build222_render_dispatch_cases.csv")
    assert all(r["case_target_valid"]=="True" for r in rows)
def test_map_reads_do_not_claim_semantics():
    rows=read("build222_map_read_sites_D.csv")
    assert rows and all(r["interpretation"]=="MAP_READ_SITE; ROLE_NOT_INFERRED" for r in rows)
def test_phase_classification_preserves_uncertainty():
    rows=read("build222_initialization_runtime_evidence.csv")
    assert any(r["phase_class"]=="UNCLASSIFIED_MIXED" for r in rows)
