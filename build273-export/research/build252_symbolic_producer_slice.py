"""Conservative symbolic replay of the linear producer slices at renderer callsites.
This is deliberately not a whole-method JVM verifier: control-flow edges are barriers.
"""
from pathlib import Path
import csv,re
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'research/build248_caller_argument_provenance.csv'
OUT=ROOT/'research/build252_symbolic_producer_slice.csv'
rows=list(csv.DictReader(SRC.open()))
inst_re=re.compile(r'(\d+):\s+([a-z][a-z0-9_]*)(?:\s+(-?\d+))?(?:\s+//\s+(.*))?')
branch={'goto','ifeq','ifne','iflt','ifle','ifgt','ifge','ifnull','ifnonnull','if_icmpeq','if_icmpne','if_icmplt','if_icmple','if_icmpgt','if_icmpge','tableswitch','lookupswitch'}
def parse(text):
 out=[]
 for part in text.split('|'):
  m=inst_re.search(part.strip())
  if m: out.append((int(m.group(1)),m.group(2),m.group(3),m.group(4) or ''))
 return out

def replay(inst):
 stack=[]; locals={}; supported=0; barriers=[]; under=0; ops=[]
 def pop():
  nonlocal under
  if stack:return stack.pop()
  under+=1;return 'UNKNOWN_ENTRY_STACK'
 for off,op,arg,comment in inst:
  if op in branch:
   barriers.append(f'{off}:{op}'); stack=[]; continue
  n=int(arg) if arg is not None else None
  if op.startswith('iconst_'):
   v={'iconst_m1':-1}.get(op, int(op[-1]) if op[-1].isdigit() else None);stack.append(f'CONST({v})');supported+=1
  elif op in ('bipush','sipush'):stack.append(f'CONST({n})');supported+=1
  elif op=='ldc' or op=='ldc_w':stack.append('CONSTANT_POOL_VALUE');supported+=1
  elif op.startswith(('aload','iload')):
   idx=n if n is not None else (int(op.split('_')[-1]) if '_' in op and op.split('_')[-1].isdigit() else None)
   stack.append(locals.get(idx,f'LOCAL({idx})'));supported+=1
  elif op in ('getstatic','getfield'):
   if op=='getfield': pop()
   field=comment.split('Field ',1)[-1] if 'Field ' in comment else 'FIELD_UNKNOWN'
   stack.append(f'{op.upper()}({field})');supported+=1
  elif op=='aaload':idx=pop();arr=pop();stack.append(f'AALOAD({arr},{idx})');supported+=1
  elif op in ('baload','iaload'):idx=pop();arr=pop();stack.append(f'{op.upper()}({arr},{idx})');supported+=1
  elif op in ('iadd','isub','imul','idiv','irem','iand','ior','ishr','iushr','ixor'):
   b=pop();a=pop();stack.append(f'{op.upper()}({a},{b})');supported+=1
  elif op in ('i2b','i2s','i2c'):
   a=pop();stack.append(f'{op.upper()}({a})');supported+=1
  elif op=='dup':a=pop();stack.extend([a,a]);supported+=1
  elif op=='swap':a=pop();b=pop();stack.extend([a,b]);supported+=1
  elif op=='pop':pop();supported+=1
  elif op.startswith('istore') or op.startswith('astore'):
   idx=n if n is not None else (int(op.split('_')[-1]) if '_' in op and op.split('_')[-1].isdigit() else None);locals[idx]=pop();supported+=1
  elif op.startswith('invoke'):
   barriers.append(f'{off}:{op}:nested-call');stack=[]
  else: barriers.append(f'{off}:{op}:unsupported');stack=[]
  if stack: ops.append(f'{off}:{op}=>{stack[-1]}')
 return stack,locals,supported,barriers,under,ops
out=[]
for r in rows:
 inst=parse(r['raw_argument_slice']); stack,loc,sup,bar,under,ops=replay(inst)
 out.append({'method':r['method'],'bytecode_offset':r['bytecode_offset'],'descriptor':r['descriptor'],'receiver_slot':r['receiver_slot'],'instruction_count':len(inst),'supported_instruction_count':sup,'stack_underflow_count':under,'control_flow_or_unsupported_barriers':';'.join(bar),'linear_stack_depth_after_last_barrier':len(stack),'linear_stack_top':' | '.join(stack[-9:]),'tracked_local_count':len(loc),'symbolic_trace':' || '.join(ops),'status':'PARTIAL_LINEAR_SLICE_NOT_FULL_INVOCATION_PROOF'})
with OUT.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=out[0].keys());w.writeheader();w.writerows(out)
print(f'callsites={len(out)} parsed_instructions={sum(x["instruction_count"] for x in out)} supported_ops={sum(x["supported_instruction_count"] for x in out)} underflows={sum(x["stack_underflow_count"] for x in out)}')
