import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_all_25_callsite_descriptors_have_valid_receiver_contracts():
 rows=list(csv.DictReader((ROOT/"research/build250_render_invocation_descriptor_contracts.csv").open()))
 assert len(rows)==25
 assert all(int(r["receiver_plus_parameter_slots"]) in (8,9) for r in rows)
 assert all(r["composite_group"]=="UNKNOWN" for r in rows)
 assert all(r["validation"]=="DESCRIPTOR_CONTRACT_ONLY_NOT_RUNTIME_STACK_PROOF" for r in rows)
def test_six_and_seven_integer_overloads_are_distinguished():
 rows=list(csv.DictReader((ROOT/"research/build250_render_invocation_descriptor_contracts.csv").open()))
 counts={r["descriptor"]:int(r["parameter_count"]) for r in rows}
 assert sorted(counts.values())==[7,8]
