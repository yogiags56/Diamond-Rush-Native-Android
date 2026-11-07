from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/"research/build248_caller_argument_provenance.csv"
out=ROOT/"research/build250_render_invocation_descriptor_contracts.csv"
def parse(desc):
 args=desc.split("(",1)[1].split(")",1)[0]; i=slots=0; types=[]
 while i<len(args):
  c=args[i]
  if c in "ZBCSIF": types.append(c); slots+=1; i+=1
  elif c in "JD": types.append(c); slots+=2; i+=1
  elif c=="L":
   j=args.index(";",i); types.append(args[i:j+1]); slots+=1; i=j+1
  elif c=="[":
   j=i
   while args[j]=="[": j+=1
   if args[j]=="L": j=args.index(";",j)+1
   else: j+=1
   types.append(args[i:j]); slots+=1; i=j
  else: raise ValueError(f"Unsupported descriptor {desc} at {i}")
 return types,slots
calls=list(csv.DictReader(source.open())); rows=[]
for c in calls:
 types,slots=parse(c["descriptor"])
 rows.append({"method":c["method"],"bytecode_offset":c["bytecode_offset"],"descriptor":c["descriptor"],"receiver_slot":c["receiver_slot"],"parameter_types":" ; ".join(types),"parameter_count":len(types),"parameter_slots":slots,"receiver_plus_parameter_slots":slots+1,"expected_stack_shape":"receiver, "+", ".join(types),"validation":"DESCRIPTOR_CONTRACT_ONLY_NOT_RUNTIME_STACK_PROOF","composite_group":"UNKNOWN"})
with out.open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
assert len(rows)==25
assert {r["receiver_plus_parameter_slots"] for r in rows}=={8,9}
print("BUILD250_DESCRIPTOR_CONTRACTS_PASS",len(rows))
