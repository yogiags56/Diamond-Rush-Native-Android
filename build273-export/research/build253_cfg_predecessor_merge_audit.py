from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]
states=list(csv.DictReader((ROOT/"research/build221_instruction_entry_stack_states.csv").open()))
edges=list(csv.DictReader((ROOT/"research/build220_cfg_edges.csv").open()))
calls=list(csv.DictReader((ROOT/"research/build248_caller_argument_provenance.csv").open()))
preds={}
for e in edges:
 if e["method"]=="as": preds.setdefault(int(e["target"]),set()).add(int(e["source"]))
by={(r["method"],int(r["offset"])):r for r in states}; rows=[]
for c in calls:
 off=int(c["bytecode_offset"]); ps=sorted(preds.get(off,set())); got=[by.get(("as",p)) for p in ps]; have=[x for x in got if x]; depths={x["stack_depth"] for x in have}; entry=by.get(("as",off))
 status=("NO_PREDECESSOR_EDGE" if not ps else "MISSING_PREDECESSOR_STATE" if len(have)!=len(ps) else "DEPTH_CONSISTENT" if len(depths)==1 else "DEPTH_CONFLICT")
 rows.append({"method":c["method"],"callsite_offset":off,"descriptor":c["descriptor"],"receiver_slot":c["receiver_slot"],"cfg_predecessor_count":len(ps),"cfg_predecessor_offsets":";".join(map(str,ps)),"predecessor_states_available":len(have),"predecessor_stack_depths":";".join(sorted(depths)),"merge_status":status,"callsite_entry_state_available":str(entry is not None).upper(),"callsite_entry_stack_depth":entry["stack_depth"] if entry else "UNKNOWN","argument_values":"UNKNOWN","composite_group":"UNKNOWN","promotion":"NOT_PROMOTED"})
with (ROOT/"research/build253_cfg_predecessor_merge_audit.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print("callsite_count",len(rows),"depth_consistent",sum(x["merge_status"]=="DEPTH_CONSISTENT" for x in rows))
