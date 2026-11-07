"""Build251: conservative JVM invocation stack-contract verifier.
Only descriptor/slot arithmetic and explicitly supported straight-line stack ops are interpreted.
"""
import csv,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'research/build250_render_invocation_descriptor_contracts.csv'
OUT=ROOT/'research/build251_descriptor_stack_contracts.csv'

def parse_method(desc):
    assert desc.startswith('(') and ')' in desc
    i=1; args=[]
    while desc[i]!=')':
        start=i
        while desc[i]=='[': i+=1
        if desc[i]=='L': i=desc.index(';',i)+1
        else: i+=1
        args.append(desc[start:i])
    ret=desc[i+1:]
    return args,ret

def slots(t): return 2 if t in ('J','D') else 1

def stack_contract(desc, has_receiver=True):
    args,ret=parse_method(desc)
    consumed=sum(slots(x) for x in args)+(1 if has_receiver else 0)
    produced=0 if ret=='V' else slots(ret)
    return consumed,produced,args,ret

rows=[]
for r in csv.DictReader(SRC.open()):
    desc=r['descriptor'].split(':',1)[1] if ':' in r['descriptor'] else r['descriptor']
    consumed,produced,args,ret=stack_contract(desc,True)
    expected=int(r['receiver_plus_parameter_slots'])
    ok=consumed==expected and produced==0
    rows.append({**{k:r[k] for k in ('method','bytecode_offset','descriptor','receiver_slot')},
      'descriptor_argument_count':len(args),'descriptor_consumed_slots':consumed,
      'descriptor_produced_slots':produced,'expected_consumed_slots':expected,
      'contract_valid':str(ok).upper(),
      'runtime_stack_proven':'FALSE','composite_group':'UNKNOWN'})
assert len(rows)==25 and all(x['contract_valid']=='TRUE' for x in rows)
with OUT.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print(f'callsite_contracts={len(rows)} valid={sum(x["contract_valid"]=="TRUE" for x in rows)} runtime_stack_proven=0')
