"""Audit CFG/callsite method identity before attempting block-state propagation."""
from pathlib import Path
import csv
R=Path(__file__).resolve().parents[1]
calls=list(csv.DictReader((R/"research/build248_caller_argument_provenance.csv").open()))
blocks=list(csv.DictReader((R/"research/build220_basic_blocks.csv").open()))
methods=sorted({x["method"] for x in blocks})
rows=[]
for c in calls:
 rows.append({"caller_method":c["method"],"callsite_offset":c["bytecode_offset"],"descriptor":c["descriptor"],"cfg_method_candidates":";".join(methods),"exact_method_identity_match":str(c["method"] in methods).upper(),"matching_cfg_block_count":0,"block_start":"UNKNOWN","block_end":"UNKNOWN","predecessor_block_count":"UNKNOWN","entry_stack_state":"NOT_JOINED","reason":"CALLER_METHOD_IDENTITY_NOT_RECONCILED"})
with (R/"research/build254_cfg_method_identity_audit.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print("callsite_count",len(rows),"cfg_methods",methods,"exact_identity_matches",sum(x["exact_method_identity_match"]=="TRUE" for x in rows))
