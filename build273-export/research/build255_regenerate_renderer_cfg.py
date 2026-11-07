from pathlib import Path
import csv,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
jar=ROOT/"original.jar"
out=subprocess.run(["javap","-classpath",str(jar),"-p","-c","-s","i"],capture_output=True,text=True,check=True).stdout
lines=out.splitlines(); start=next(i for i,x in enumerate(lines) if re.match(r"\s*private void D\(\);",x)); end=next((i for i in range(start+1,len(lines)) if re.match(r"\s*(private|public|protected|static).*\);",lines[i])),len(lines)); sec=lines[start:end]
ins=[]
for x in sec:
 m=re.match(r"\s*(\d+):\s+(.+)$",x)
 if m and not re.fullmatch(r"-?\\d+",m.group(2).strip()): ins.append((int(m.group(1)),m.group(2).strip()))
by=dict(ins); offs=[x[0] for x in ins]; nxt={offs[i]:offs[i+1] for i in range(len(offs)-1)}; sw={}
for i,x in enumerate(sec):
 m=re.match(r"\s*(\d+):\s+(tableswitch|lookupswitch)",x)
 if not m: continue
 ts=[]; j=i+1
 while j<len(sec) and "}" not in sec[j]:
  q=re.match(r"\s*(?:-?\d+|default):\s+(-?\d+)\s*$",sec[j])
  if q: ts.append(int(q.group(1)))
  j+=1
 sw[int(m.group(1))]=ts
leaders={offs[0]}; br={}
for o,t in ins:
 op=t.split()[0]
 if o in sw:
  br[o]=(op,sw[o]); leaders.update(x for x in sw[o] if x in by)
  if o in nxt: leaders.add(nxt[o])
 else:
  q=re.search(r"\b(?:goto(?:_w)?|if_[a-z0-9_]+|jsr(?:_w)?)\s+(-?\d+)",t)
  if q:
   target=int(q.group(1)); br[o]=(op,[target]);
   if target in by: leaders.add(target)
   if not op.startswith("goto") and o in nxt: leaders.add(nxt[o])
  elif op in ("return","ireturn","areturn","lreturn","freturn","dreturn","athrow") and o in nxt: leaders.add(nxt[o])
ordered=sorted(leaders,key=lambda x: offs.index(x))
blocks=[]
for i,st in enumerate(ordered):
 i0=offs.index(st); i1=offs.index(ordered[i+1]) if i+1<len(ordered) else len(ins)
 arr=offs[i0:i1]
 if arr: blocks.append((arr[0],arr[-1],arr))
owner={o:(s,e) for s,e,arr in blocks for o in arr}; edges=[]
for s,e,arr in blocks:
 o=arr[-1]; op=by[o].split()[0]
 if o in br:
  for t in br[o][1]:
   if t in owner: edges.append((s,owner[t][0],"switch" if o in sw else "branch"))
  if (o in sw or not op.startswith("goto")) and o in nxt and nxt[o] in owner: edges.append((s,owner[nxt[o]][0],"fallthrough"))
 elif op not in ("return","ireturn","areturn","lreturn","freturn","dreturn","athrow") and o in nxt and nxt[o] in owner: edges.append((s,owner[nxt[o]][0],"fallthrough"))
R=ROOT/"research"
for name,header,data in [("build255_renderer_instructions.csv",["method","offset","instruction"],[("i.D()V",o,t) for o,t in ins]),("build255_renderer_basic_blocks.csv",["method","block_start","block_end","instruction_count","first_instruction","last_instruction"],[("i.D()V",s,e,len(a),by[a[0]],by[a[-1]]) for s,e,a in blocks]),("build255_renderer_cfg_edges.csv",["method","source_block","target_block","edge_type"],[("i.D()V",*x) for x in edges])]:
 with (R/name).open("w",newline="") as f: w=csv.writer(f);w.writerow(header);w.writerows(data)
calls=list(csv.DictReader((R/"build248_caller_argument_provenance.csv").open())); rows=[]
for c in calls:
 o=int(c["bytecode_offset"]); b=owner.get(o); ps=sorted({a for a,t,k in edges if b and t==b[0]}); rows.append({"method":c["method"],"callsite_offset":o,"descriptor":c["descriptor"],"cfg_method":"i.D()V","block_start":b[0] if b else "UNKNOWN","block_end":b[1] if b else "UNKNOWN","predecessor_block_count":len(ps),"predecessor_block_starts":";".join(map(str,ps)),"instruction_is_renderer_invoke":str(by.get(o,"").startswith("invokevirtual") and "Method f.a:" in by.get(o,"")).upper(),"mapping":"EXACT" if b else "UNMAPPED"})
with (R/"build255_callsite_basic_block_map.csv").open("w",newline="") as f: w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print("instructions",len(ins),"blocks",len(blocks),"edges",len(edges),"switches",len(sw),"callsites",len(rows),"exact",sum(x["mapping"]=="EXACT" and x["instruction_is_renderer_invoke"]=="TRUE" for x in rows))
