from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]
states=list(csv.DictReader((ROOT/"research/build221_instruction_entry_stack_states.csv").open()))
calls=list(csv.DictReader((ROOT/"research/build248_caller_argument_provenance.csv").open()))
by={(r["method"],int(r["offset"])):r for r in states}
rows=[]
for c in calls:
 off=int(c["bytecode_offset"]); s=by.get(("as",off))
 rows.append({"method":c["method"],"bytecode_offset":off,"descriptor":c["descriptor"],"receiver_slot":c["receiver_slot"],"entry_stack_state_available":str(s is not None).upper(),"entry_stack_depth":s["stack_depth"] if s else "UNKNOWN","entry_stack_values":s["stack_values"] if s else "UNKNOWN","tracked_locals":s["locals_tracked"] if s else "UNKNOWN","interpretation":"ENTRY_STATE_ONLY_NOT_ARGUMENT_STACK" if s else "NO_MATCHING_PRIOR_WORKLIST_STATE","composite_group":"UNKNOWN"})
out=ROOT/"research/build249_callsite_worklist_state_join.csv"
with out.open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print(f"callsites={len(rows)} matched={sum(x['entry_stack_state_available']=='TRUE' for x in rows)} unmatched={sum(x['entry_stack_state_available']=='FALSE' for x in rows)} composite_groups_resolved=0")
