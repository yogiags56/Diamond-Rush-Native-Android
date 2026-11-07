from pathlib import Path
import csv
R=Path(__file__).resolve().parents[1]/"research"
def rows(n): return list(csv.DictReader((R/n).open()))
def test_worklist_covers_cfg_reachability():
 b=rows("build257_block_entry_abstract_states.csv")
 assert len(b)==322 and sum(x["reachable"]=="TRUE" for x in b)==247
def test_worklist_marks_stack_shape_conflicts_explicitly():
 b=rows("build257_block_entry_abstract_states.csv")
 assert sum(x["stack_shape_conflict"]=="TRUE" for x in b)==20
def test_callsite_audit_is_fail_closed():
 c=rows("build257_callsite_abstract_stack_audit.csv")
 assert len(c)==25
 assert sum(x["stack_depth_before_invoke"]!="UNKNOWN" for x in c)==13
 assert sum(x["sufficient_depth"]=="TRUE" for x in c)==13
 assert all(x["argument_values"]=="UNKNOWN" and x["promotion"]=="NOT_PROMOTED" for x in c)
