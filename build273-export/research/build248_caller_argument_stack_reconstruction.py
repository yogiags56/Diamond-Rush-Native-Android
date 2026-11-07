"""Build248: classify caller-side integer argument producer evidence at sprite callsites."""
from pathlib import Path
import csv, re
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'research/build246_render_argument_provenance.csv'
out=ROOT/'research/build248_caller_argument_provenance.csv'
rows=list(csv.DictReader(src.open()))
assert len(rows)==25

def classify(s):
    # Preserve bytecode snippets verbatim; classify only directly visible producer forms.
    tokens=[]
    for m in re.finditer(r'(?:iconst_[m0-5]|bipush\s+-?\d+|sipush\s+-?\d+|iload\s+\d+|getfield\s+#\d+\s+// Field [\w$]+:[BCSI]|getstatic\s+#\d+\s+// Field [\w$]+:[BCSI]|iadd|isub|imul|ishr|iushr|iand|irem|baload|iaload|invokestatic\s+#\d+)',s):
        tokens.append(m.group(0).replace('\n',' ').strip())
    return tokens
outrows=[]
for r in rows:
    s=r['argument_producer_slice']
    producers=classify(s)
    known=r['receiver_slot']!='UNRESOLVED'
    # A callsite's raw excerpt ends immediately before invoke; do not claim stack order
    # unless the receiver is explicit and every argument source is fully represented.
    constants=re.findall(r'(?:iconst_[m0-5]|bipush\s+-?\d+|sipush\s+-?\d+)',s)
    fields=re.findall(r'get(?:static|field).*?// Field ([\w$]+):([BCSI])',s)
    derived=[x for x in producers if x in ('iadd','isub','imul','ishr','iushr','iand','irem','baload','iaload')]
    outrows.append({
      'method':r['method'],'bytecode_offset':r['bytecode_offset'],'descriptor':r['descriptor'],
      'receiver_slot':r['receiver_slot'],'receiver_status':'EXPLICIT' if known else 'UNRESOLVED',
      'constant_producer_count':len(constants),'constant_producers':' ; '.join(constants),
      'field_producer_count':len(fields),'field_producers':' ; '.join(f'{a}:{b}' for a,b in fields),
      'derived_operation_count':len(derived),'derived_operations':' ; '.join(derived),
      'raw_argument_slice':s,
      'argument_resolution':'PARTIAL_PRODUCER_EVIDENCE_NOT_FULL_STACK_PROOF',
      'composite_group':'UNKNOWN'
    })
with out.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=outrows[0].keys());w.writeheader();w.writerows(outrows)
known=sum(x['receiver_status']=='EXPLICIT' for x in outrows)
print(f'callsites={len(outrows)} explicit_receivers={known} unresolved_receivers={len(outrows)-known}')
print(f'constant_producer_records={sum(x["constant_producer_count"]>0 for x in outrows)}')
print(f'field_producer_records={sum(x["field_producer_count"]>0 for x in outrows)}')
print(f'derived_operation_records={sum(x["derived_operation_count"]>0 for x in outrows)}')
