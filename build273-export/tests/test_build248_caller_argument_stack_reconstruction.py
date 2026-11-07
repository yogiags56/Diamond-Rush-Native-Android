import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_build248_has_all_sprite_callsites():
    rows=list(csv.DictReader((ROOT/'research/build248_caller_argument_provenance.csv').open()))
    assert len(rows)==25
    assert len({r['bytecode_offset'] for r in rows})==25
def test_build248_keeps_unknowns_explicit():
    rows=list(csv.DictReader((ROOT/'research/build248_caller_argument_provenance.csv').open()))
    assert all(r['composite_group']=='UNKNOWN' for r in rows)
    assert all(r['argument_resolution']=='PARTIAL_PRODUCER_EVIDENCE_NOT_FULL_STACK_PROOF' for r in rows)
def test_build248_receiver_counts_match_prior_audit():
    rows=list(csv.DictReader((ROOT/'research/build248_caller_argument_provenance.csv').open()))
    assert sum(r['receiver_status']=='EXPLICIT' for r in rows)==13
    assert sum(r['receiver_status']=='UNRESOLVED' for r in rows)==12
