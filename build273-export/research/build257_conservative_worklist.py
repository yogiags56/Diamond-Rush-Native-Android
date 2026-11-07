from pathlib import Path
import csv,re,collections
R=Path(__file__).resolve().parents[1]/"research"
def read(n): return list(csv.DictReader((R/n).open()))
ins=read("build255_renderer_instructions.csv"); blocks=read("build255_renderer_basic_blocks.csv")
edges=read("build255_renderer_cfg_edges.csv"); calls=read("build255_callsite_basic_block_map.csv")
byoff={int(x["offset"]):x["instruction"] for x in ins}
bm={int(b["block_start"]):b for b in blocks}
members={int(b["block_start"]):[(o,t) for o,t in sorted(byoff.items()) if int(b["block_start"])<=o<=int(b["block_end"])] for b in blocks}
succ=collections.defaultdict(set); pred=collections.defaultdict(set)
for e in edges:
 s,t=int(e["source_block"]),int(e["target_block"]); succ[s].add(t); pred[t].add(s)
U="UNKNOWN"; CONFLICT="STACK_SHAPE_CONFLICT"
def desc_slots(d):
 m=re.search(r":(\(.*\))(.+)$",d)
 if not m:return None
 a=m.group(1)[1:-1]; i=n=0
 while i<len(a):
  c=a[i]
  if c=="[": 
   while i<len(a) and a[i]=="[": i+=1
   if i<len(a) and a[i]=="L": i=a.index(";",i)+1
   else:i+=1
   n+=1
  elif c=="L": i=a.index(";",i)+1;n+=1
  else:n+=2 if c in "JD" else 1;i+=1
 ret=m.group(2); return n+(0 if ret=="V" else 2 if ret in ("J","D") else 1)
def locidx(op,txt):
 m=re.search(r"\b(?:aload|iload|astore|istore)\s+(\d+)",txt)
 if m:return int(m.group(1))
 m=re.search(r"\b(?:aload|iload|astore|istore)_(\d+)",op)
 return int(m.group(1)) if m else None
def transfer(stack,loc,txt):
 op=txt.split()[0]; flags=[]
 def pop(n=1):
  vals=[]
  for _ in range(n): vals.append(stack.pop() if stack else U)
  return vals
 def push(x):stack.append(x)
 if op.startswith("iconst_"): push("C:"+("-1" if op=="iconst_m1" else op.rsplit("_",1)[1]))
 elif op in ("bipush","sipush"):
  m=re.search(r"(-?\d+)$",txt);push("C:"+m.group(1) if m else U)
 elif op=="aconst_null":push("NULL")
 elif op=="ldc":push(U)
 elif op.startswith(("aload","iload")):
  i=locidx(op,txt);push(loc.get(i,U) if i is not None else U)
 elif op.startswith(("astore","istore")):
  i=locidx(op,txt);v=pop()[0]
  if i is not None:loc[i]=v
 elif op=="iinc":
  m=re.search(r"iinc\s+(\d+)\s+(-?\d+)",txt)
  if m:
   i,n=int(m.group(1)),int(m.group(2));v=loc.get(i,U)
   loc[i]="C:"+str(int(v[2:])+n) if v.startswith("C:") else U
 elif op in ("getfield","getstatic"):
  if op=="getfield":pop()
  push(U)
 elif op=="putfield":pop(2)
 elif op=="putstatic":pop()
 elif op in ("aaload","baload","iaload","saload"):pop(2);push(U)
 elif op=="aastore":pop(3)
 elif op in ("iadd","isub","imul","idiv","irem","iand","ior","ixor","ishl","ishr","iushr"):
  a,b=pop(2);v=U
  if a.startswith("C:") and b.startswith("C:"):
   x,y=int(a[2:]),int(b[2:])
   try:
    z={"iadd":x+y,"isub":x-y,"imul":x*y,"idiv":int(x/y),"irem":x%y,"iand":x&y,"ior":x|y,"ixor":x^y,"ishl":x<<y,"ishr":x>>y,"iushr":(x%(1<<32))>>y}[op];v="C:"+str(z)
   except Exception:pass
  push(v)
 elif op in ("ineg","i2b","i2s","i2c"):
  a=pop()[0];push(a if a==U else "C:"+str(-int(a[2:]) if op=="ineg" else int(a[2:])))
 elif op=="dup":
  a=pop()[0];push(a);push(a)
 elif op=="swap":
  a,b=pop(2);push(a);push(b)
 elif op=="dup_x1":
  a,b=pop(2);push(a);push(b);push(a)
 elif op in ("ifeq","ifne","iflt","ifle","ifgt","ifge","ifnull","ifnonnull"):pop()
 elif op.startswith("if_icmp"):pop(2)
 elif op in ("tableswitch","lookupswitch"):pop()
 elif op.startswith("invoke"):
  m=re.search(r"// Method (.+)$",txt); d=m.group(1).split(":")[-1] if m and ":" in m.group(1) else ""
  n=desc_slots("x:"+d) if d.startswith("(") else None
  if n is None:flags.append("INVOKE_DESCRIPTOR_UNKNOWN");stack.clear();push(U)
  else:
   # return value count is handled by descriptor's return suffix
   ret=d[d.index(")")+1:]; consumed=n+(0 if op=="invokestatic" else 1);pop(consumed)
   if ret!="V":push(U)
 elif op in ("goto","goto_w","return"):pass
 else:flags.append("UNSUPPORTED:"+op);stack.clear();push(U)
 return flags
def merge(old,new):
 if old is None:return new,False
 a,la=old;b,lb=new
 if len(a)!=len(b):return ([CONFLICT],{}),True
 s=[x if x==y else U for x,y in zip(a,b)]
 l={k:(la.get(k,U) if la.get(k,U)==lb.get(k,U) else U) for k in set(la)|set(lb)}
 return (s,l),False
entry=min(bm); states={entry:([],{0:"THIS"})}; q=collections.deque([entry]); queued={entry}
visits=collections.Counter(); conflicts=set(); unsupported=collections.Counter(); snapshots={}
while q:
 s=q.popleft();queued.discard(s);visits[s]+=1
 st,lo=states[s];stack=list(st);loc=dict(lo)
 for off,txt in members[s]:
  if off in {int(c["callsite_offset"]) for c in calls}:snapshots[off]=(list(stack),txt)
  for flag in transfer(stack,loc,txt):unsupported[flag]+=1
 out=(stack,loc)
 for t in succ[s]:
  merged,conf=merge(states.get(t),out)
  if conf:conflicts.add(t)
  if t not in states or merged!=states[t]:
   states[t]=merged
   if t not in queued:q.append(t);queued.add(t)
block_rows=[]
for s,b in sorted(bm.items()):
 state=states.get(s)
 block_rows.append({"block_start":s,"block_end":b["block_end"],"reachable":str(state is not None).upper(),"entry_stack_depth":len(state[0]) if state else "UNKNOWN","entry_stack":"|".join(state[0]) if state else "UNKNOWN","local_count":len(state[1]) if state else 0,"worklist_visits":visits[s],"stack_shape_conflict":str(s in conflicts).upper()})
with (R/"build257_block_entry_abstract_states.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=block_rows[0]);w.writeheader();w.writerows(block_rows)
call_rows=[]
for c in calls:
 off=int(c["callsite_offset"]);snap=snapshots.get(off);expected=desc_slots("x:"+c["descriptor"].split(":")[-1])
 call_rows.append({"callsite_offset":off,"descriptor":c["descriptor"],"invoke_instruction":snap[1] if snap else "MISSING","stack_depth_before_invoke":len(snap[0]) if snap else "UNKNOWN","descriptor_consumed_slots_including_receiver":expected,"sufficient_depth":str(snap is not None and len(snap[0])>=expected).upper(),"argument_values":"UNKNOWN","composite_group":"UNKNOWN","promotion":"NOT_PROMOTED"})
with (R/"build257_callsite_abstract_stack_audit.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=call_rows[0]);w.writeheader();w.writerows(call_rows)
print("blocks",len(bm),"reachable",len(states),"worklist_visits",sum(visits.values()),"shape_conflicts",len(conflicts),"unsupported",dict(unsupported),"callsite snapshots",len(snapshots),"depth sufficient",sum(x["sufficient_depth"]=="TRUE" for x in call_rows))
